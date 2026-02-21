# 🔐 Secure Client-Side Deduplication with Public Auditing

An academic prototype demonstrating secure client-side deduplication of encrypted cloud data with public integrity auditing using a Third Party Auditor (TPA).

This project is implemented as a Django-based web application and is intended for academic learning, research, and evaluation purposes only.

---

## 📖 Project Overview
This system demonstrates a secure approach to cloud storage by performing deduplication at the client side before upload. Files are encrypted, checked for duplication, and securely stored while maintaining privacy. A Third Party Auditor (TPA) verifies integrity without accessing actual file contents.

---

## 🧩 Architecture Summary

### 🖥️ Frontend
- Django Templates (HTML, CSS)

### ⚙️ Backend
- Python (Django Framework)
- Server-side view logic
- Database connectivity using PyMySQL
- Cryptographic processing using Paillier Encryption

### ☁️ Storage
Simulated cloud storage using local filesystem:

---

## ✨ Main Features & Components

### 🔐 User Authentication
- Manual user registration and login
- Secure session handling

### 📤 File Upload & Deduplication
- Client-side file processing
- SHA-256 hash based duplicate detection
- Storage optimization by avoiding redundant uploads
- Base64 encoding for secure storage

### 🧾 Integrity Verification (TPA)
- Public auditing using Third Party Auditor
- Hash comparison with stored metadata
- Integrity validation without exposing file data

### 📥 File Download
- Secure file retrieval
- Logical mapping between uploaded and stored files

### 📊 Storage Comparison Graphs
Visual comparison between:
- Normal storage usage
- Deduplicated storage usage

Graphs generated using **Matplotlib** and embedded dynamically.

### 🔐 Cryptography
- Paillier Homomorphic Encryption (`phe` library)
- Demonstrates secure computation on encrypted data

---

## 🛠️ Requirements

Ensure the following are installed:

- 🐍 Python 3.8+
- 🌐 Django (2.x / 3.x recommended)
- 🗄️ MySQL / MariaDB
- 📦 pip & virtualenv

### Python Libraries
django
pymysql
phe
numpy
matplotlib

---

## 🚀 Quick Start (Development)

### 1️⃣ Clone the Repository
git clone <your-repository-link>
cd project-folder

### 2️⃣ Create & Activate Virtual Environment
python -m venv .venv

**Windows**
.venv\Scripts\activate

**Linux / macOS**
source .venv/bin/activate

### 3️⃣ Install Dependencies
pip install django pymysql phe numpy matplotlib

(Optional)
pip freeze > requirements.txt

### 4️⃣ Database Setup
- Start MySQL / MariaDB
- Create database named:
-auditing
- Update database credentials inside Django `settings.py`.

### 5️⃣ Prepare Storage Directory
mkdir -p AuditingApp/static/files
Ensure write permissions are enabled.

### 6️⃣ Run the Server
python manage.py runserver

Open in browser:
http://127.0.0.1:8000/

---

## 📌 Project Outcome
- Reduces redundant cloud storage usage
- Maintains confidentiality of encrypted data
- Enables trusted public auditing
- Demonstrates real-world cloud security concepts

---

## ⚠️ Disclaimer
This project is an academic implementation intended only for educational and research purposes and is not designed for production deployment.

---

## 📬 Maintainer
**kamutalasumanth**

For issues, improvements, or questions, please use GitHub Issues.
