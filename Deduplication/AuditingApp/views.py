from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
import os
from django.core.files.storage import FileSystemStorage
import pymysql
import phe
from phe import paillier
import pickle
import os
from datetime import date
import base64
import hashlib
from TPA import *
import ftplib
import io
import base64
import numpy as np
import matplotlib.pyplot as plt

global username, unique_storage, normal_storage

def generateKeys():
    if os.path.exists('keys/fhe.pckl'):
        f = open('keys/fhe.pckl', 'rb')
        keys = pickle.load(f)
        f.close()
        public_key, private_key = keys
    else:
        # Generate a key pair (in a real application, you would likely reuse keys)
        public_key, private_key = phe.paillier.generate_paillier_keypair()
        keys = [public_key, private_key]
        f = open('keys/fhe.pckl', 'wb')
        pickle.dump(keys, f)
        f.close()
    return public_key, private_key

public_key, private_key = generateKeys()

def encrypt_file_chunk(chunk, public_key):
    chunk_int = int.from_bytes(chunk, byteorder='big')
    encrypted_chunk = public_key.encrypt(chunk_int)
    return encrypted_chunk

def readFile(file_path, public_key, option):#function to read and encrypt video
    with open(file_path, "rb") as file:
        data = file.read() #read video
    file.close()
    if option == 0:
        data = base64.b64encode(data)
    data = data[0:300]
    chunks = encrypt_file_chunk(data, public_key)#encrypt and return video            
    return chunks

def checkDuplicate(file_path):
    global public_key, private_key
    status = ""
    filename = ""
    chunks = readFile(file_path, public_key, 0)#reading FHE encrypted source video using public key as chunks
    for root, dirs, directory in os.walk('AuditingApp/static/files'):
        for j in range(len(directory)):
            if status != "Duplicate":
                chunks1 = readFile(root+"/"+directory[j], public_key, 1) #getting database encrypted video as chunks
                difference = chunks - chunks1 #now applying mathematical computation on homomorphic encrypted video by calculating subtracion means difference
                decrypted_difference = private_key.decrypt(difference)
                if decrypted_difference > 0: #if differnec > 0 video is unique
                    status = "Unique"
                elif decrypted_difference < 0: #if differnec < 0 video is unique
                    status = "Unique"
                else: #if difference equals then video is duplicated
                    status = "Duplicate"
                    filename = directory[j]
                    break
        if status == "Duplicate":
            break
    if len(status) == 0:
        status = "Unique"        
    return status, filename

def DownloadFileAction(request):
    if request.method == 'GET':
        name = request.GET.get('name', False)
        with open("AuditingApp/static/files/"+name, "rb") as file:
            data = file.read()
        file.close()
        data = base64.b64decode(data)
        response = HttpResponse(data,content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename='+name
        return response

def VerifyIntegrityAction(request):
    if request.method == 'GET':
        global username
        name = request.GET.get('name', False)
        with open("AuditingApp/static/files/"+name, "rb") as file:
            data = file.read()
        file.close()
        integrity = hashlib.sha256(data).hexdigest()
        status = verifyIntegrity(username, name, integrity)
        output = "<font size=3 color=red>Selected "+name+" File Integrity Verification Failed</font>" 
        if status == True:
            output = "<font size=3 color=blue>Selected "+name+" File Integrity Verification Successfull</font>"
        context= {'data':output}
        return render(request, 'UserScreen.html', context)      

def VerifyIntegrity(request):
    if request.method == 'GET':
        global username
        output = ''
        output+='<table border=1 align=center width=100%><tr><th><font size="3" color="black">Username</th><th><font size="3" color="black">File Name</th>'
        output+='<th><font size="3" color="black">Upload Date</th><th><font size="3" color="black">File Status</th>'
        output+='<th><font size="3" color="black">Check POW Integrity</th></tr>'
        scores = []
        labels = []
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'auditing',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * from files where username='"+username+"'")
            rows = cur.fetchall()
            for row in rows:
                if row[3] == "Unique":
                    output+='<tr><td><font size="3" color="black">'+row[0]+'</td>'
                    output += '<td><font size="3" color="black">'+str(row[1])+'</td>'
                    output += '<td><font size="3" color="black">'+str(row[2])+'</td>'
                    output += '<td><font size="3" color="green">'+row[3]+'</td>'
                    output+='<td><a href=\'VerifyIntegrityAction?name='+str(row[1])+'\'><font size=3 color=blue>Verify Integrity</font></a></td></tr>'
        output+= "</table></br></br></br></br>" 
        context= {'data':output}
        return render(request, 'UserScreen.html', context)            

def Graph(request):
    if request.method == 'GET':
        global unique_storage, normal_storage
        size = [normal_storage, unique_storage]
        bars = ['Normal Storage Size', 'Deduplicate Storage Size']
        y_pos = np.arange(len(bars))
        plt.figure(figsize=(5, 3))
        plt.bar(y_pos, size)
        plt.xticks(y_pos, bars)
        plt.xlabel("Technique Name")
        plt.ylabel("Storage Size")
        plt.title("Storage Size Comparison Graph")
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        img_b64 = base64.b64encode(buf.getvalue()).decode()
        plt.clf()
        plt.cla()
        context= {'data':"Storage Size Comparison Graph", 'img': img_b64}
        return render(request, 'UserScreen.html', context)

def DownloadFile(request):
    if request.method == 'GET':
        global username, unique_storage, normal_storage
        unique_storage = 0
        normal_storage = 0
        output = ''
        output+='<table border=1 align=center width=100%><tr><th><font size="3" color="black">Username</th><th><font size="3" color="black">File Name</th>'
        output+='<th><font size="3" color="black">Upload Date</th><th><font size="3" color="black">File Status</th>'
        output+='<th><font size="3" color="black">Download File</th></tr>'
        scores = []
        labels = []
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'auditing',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * from files where username='"+username+"'")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size="3" color="black">'+row[0]+'</td>'
                output += '<td><font size="3" color="black">'+str(row[1])+'</td>'
                output += '<td><font size="3" color="black">'+str(row[2])+'</td>'
                if row[3] == "Unique":
                    storage = os.path.getsize("AuditingApp/static/files/"+row[1])
                    output += '<td><font size="3" color="green">'+row[3]+'</td>'
                    unique_storage += storage
                    normal_storage += storage
                else:
                    storage = os.path.getsize("AuditingApp/static/files/"+row[4])
                    output += '<td><font size="3" color="red">'+row[3]+'</td>'
                    normal_storage += storage
                output += '<td><font size="3" color="black">'+row[4]+'</td>'
                if row[3] == "Unique":
                    output+='<td><a href=\'DownloadFileAction?name='+str(row[1])+'\'><font size=3 color=blue>Download</font></a></td></tr>'
                else:
                    output+='<td><a href=\'DownloadFileAction?name='+str(row[4])+'\'><font size=3 color=blue>Download</font></a></td></tr>'
        output+= "</table></br>"
        output += "<font size=3 color=blue>Cloud Storage Size Before Deduplication : "+str(normal_storage)+"</font><br/>"
        output += "<font size=3 color=blue>Cloud Storage Size After Deduplication : "+str(unique_storage)+"</font><br/>"
        output +="</br></br></br></br></br>" 
        context= {'data':output}
        return render(request, 'UserScreen.html', context)    

def UploadFile(request):
    if request.method == 'GET':
        return render(request, 'UploadFile.html', {})

def UploadFileAction(request):
    if request.method == 'POST':
        global username
        myfile = request.FILES['t1'].read()
        fname = request.FILES['t1'].name
        if os.path.exists("AuditingApp/static/"+fname):
            os.remove("AuditingApp/static/"+fname)
        with open("AuditingApp/static/"+fname, "wb") as file:
            file.write(myfile)
        file.close()
        status, filename = checkDuplicate("AuditingApp/static/"+fname)
        output = ""
        dd = str(date.today())
        if status == "Unique":
            os.remove("AuditingApp/static/"+fname)
            myfile = base64.b64encode(myfile)
            with open("AuditingApp/static/files/"+fname, "wb") as file:
                file.write(myfile)
            file.close()
            integrity = hashlib.sha256(myfile).hexdigest()
            print(integrity)
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'auditing',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO tpa VALUES('"+username+"','"+fname+"','"+integrity+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'auditing',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO files VALUES('"+username+"','"+fname+"','"+dd+"','"+status+"','"+fname+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            output = "<font size=3 color=blue>Uploaded file "+fname+" detected as unique</font>"
            ftp = ftplib.FTP_TLS("ftp.drivehq.com")
            ftp.login("kaleempythongpu1@gmail.com", "Offenburg965#")
            ftp.prot_p()
            file = open("AuditingApp/static/files/"+fname, 'rb')
            ftp.storbinary('STOR '+fname, file)
        else:
            os.remove("AuditingApp/static/"+fname)
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'auditing',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO files VALUES('"+username+"','"+fname+"','"+dd+"','"+status+"','"+filename+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            output = "<font size=3 color=red>Uploaded file = "+fname+" found duplicate with existing cloud file = "+filename+"</font>" 
        context= {'data':output}
        return render(request, 'UserScreen.html', context)

def RegisterAction(request):
    if request.method == 'POST':
        global username
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)               
        output = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'auditing',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    output = username+" Username already exists"
                    break                
        if output == "none":
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'auditing',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO register VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                output = "Signup process completed. Login to perform file duplication detection activities"
        context= {'data':output}
        return render(request, 'Register.html', context)        

def UserLoginAction(request):
    global username
    if request.method == 'POST':
        global username
        status = "none"
        users = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'auditing',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username,password FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == users and row[1] == password:
                    username = users
                    status = "success"
                    break
        if status == 'success':
            context= {'data':'Welcome '+username}
            return render(request, "UserScreen.html", context)
        else:
            context= {'data':'Invalid username'}
            return render(request, 'UserLogin.html', context)

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})         

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

