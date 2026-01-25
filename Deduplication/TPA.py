import pymysql

def verifyIntegrity(username, filename, proof_signature):
    status = False
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'auditing',charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("select file_integrity from tpa where username='"+username+"' and file_name='"+filename+"'")
        rows = cur.fetchall()
        for row in rows:
            if row[0] == proof_signature:
                status = True
                break
    return status        
