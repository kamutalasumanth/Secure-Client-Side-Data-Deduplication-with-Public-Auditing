🔐 Secure Client-Side Deduplication
An academic prototype that demonstrates secure client-side deduplication of encrypted cloud data with public integrity auditing using a Third Party Auditor (TPA).

This project is implemented as a Django-based web application (templates + server-side views) and is intended for learning, research, and academic evaluation, not production use.

📖 Project Overview
This project demonstrates an academic approach to:

Client-side file chunking and encryption
Secure deduplication of encrypted data
Public integrity auditing using a Third Party Auditor (TPA)
🧩 Architecture Summary
Frontend:

Django templates (HTML/CSS)
Backend:

Python (Django view functions)
Direct database access using pymysql
Cryptographic operations using Paillier homomorphic encryption
Storage:

Simulated cloud storage using local filesystem / FTP-style storage
Uploaded files are stored under:

AuditingApp/static/files/
✨ Main Features & Components
🔐 User Authentication

Manual user registration and login logic
📤 File Upload & Deduplication

Client-side file reading
Duplicate detection before storage
Base64 encoding of unique files
Reduced storage footprint through deduplication
🧾 Integrity Verification (TPA)

SHA-256 hash generation
Public integrity verification via Third Party Auditor
Hash comparison against stored metadata
📥 File Download

Users can download original or deduplicated files
Logical mapping between user uploads and stored data
📊 Storage Comparison Graphs

Visual comparison of:

Normal storage
Deduplicated storage
Generated using matplotlib and embedded as base64 images

🔐 Cryptography

Paillier homomorphic encryption (phe library)
Demonstrates secure operations on encrypted data
🛠️ Requirements
Ensure the following are installed:

🐍 Python 3.8+
🌐 Django (2.x / 3.x recommended)
🗄️ MySQL / MariaDB
📦 pip & virtualenv
Python Libraries
django
pymysql
phe
numpy
matplotlib
🚀 Quick Start (Development)
1️⃣ Clone the Repository
git clone https://github.com/Sid445/secure-client-side-deduplication.git
cd secure-client-side-deduplication
2️⃣ Create & Activate Virtual Environment
python -m venv .venv
Linux / macOS

source .venv/bin/activate
Windows

.venv\Scripts\activate
3️⃣ Install Dependencies
pip install django pymysql phe numpy matplotlib
📌 Recommendation: After verification, generate a requirements.txt:

pip freeze > requirements.txt
4️⃣ Database Setup
Start MySQL / MariaDB
Create a database named auditing
Use the schema below (or adapt to match the code)
5️⃣ Prepare Static Storage
mkdir -p AuditingApp/static/files
Ensure write permissions are enabled.

6️⃣ Run the Django Server
python manage.py runserver
🌐 Open in browser:

http://127.0.0.1:8000/AuditingApp/index.html
📬 Contact
Maintainer: kamutalasumanth 📌 Use GitHub Issues for bugs, questions, and improvements.

