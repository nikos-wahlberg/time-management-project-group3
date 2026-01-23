# ☁️ Azure Time Management & Reporting System
### Data & AI Engineer Spring ‘26 – Group 3 Project

![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)

## 📖 Project Overview
This project is a Proof of Concept (POC) solution designed for a consultancy company to manage employee time tracking and automated cloud reporting. The system was developed to deepen knowledge of **Azure Cloud Computing**, **Python**, and **Database Management**.

The solution allows consultants to log working hours via a local GUI application, stores data securely in an **Azure PostgreSQL** database, and automates reporting via an **Azure Virtual Machine** that uploads results to **Blob Storage**.

### 🔄 Project Evolution (Scenarios)
The project was built in three agile stages:
1.  **Scenario 1:** Manual reporting via Command Line Interface.
2.  **Scenario 2:** Integration of REST APIs.
3.  **Scenario 3:** Full automation running on an Azure Virtual Machine via X2Go.

---

## 🏗 Architecture & Features

The project consists of two main applications communicating with Azure services:

### 1. Time Management App (Client-Side)
* **Local GUI:** Built with Python.
* **Functionality:** Allows users to add/delete consultants and customers, and input daily work logs (Start Time, End Time, Lunch Break).
* **Security:** Uses **Azure Key Vault** to retrieve database connection secrets securely (replacing local `database.ini` files).
* **Data Storage:** Writes all inputs directly to **Azure Database for PostgreSQL**.

### 2. Reporting Software (Server-Side / VM)
* **Environment:** Runs on an Azure Virtual Machine (Ubuntu) accessed via **X2Go**.
* **Logic:** Fetches daily/weekly data from the database.
* **Output:** Generates a text report containing:
    * Total working hours by consultant and customer.
    * Cumulative working hours grouped by customer.
    * Average working hours per day.
* **Cloud Integration:** Automatically uploads the generated report to an **Azure Storage Account (Blob)**.

---

## 🛠 Tech Stack

| Component | Technology |
| :--- | :--- |
| **Language** | Python 3.x (Tkinter, Flask, Azure SDK) |
| **Cloud Provider** | Microsoft Azure |
| **Database** | Azure Database for PostgreSQL |
| **Storage** | Azure Blob Storage |
| **Security** | Azure Key Vault |
| **Infrastructure** | Resource Groups, Virtual Machines (Linux) |
| **Tools** | Git, Jira, X2Go, Postman |

---

## 🧠 Challenges & Learnings

### 🚧 Key Challenges
* **VM Configuration:** Setting up the Virtual Machine and managing the remote desktop connection via **X2Go** was the most significant technical hurdle.
* **Team Coordination:** Dividing tasks among 4 people proved difficult initially. We shifted to a collaborative "mob programming" approach which improved code quality and understanding.

### ✅ Successes
* **Secure Credentials:** Successfully implemented **Azure Key Vault** for secure credential management.
* **Full Pipeline:** Built a fully functional pipeline from Local GUI -> Cloud DB -> VM Processing -> Blob Storage.
* **Project Management:** Effective use of **Jira** for tracking progress.

---

## 📂 Repository Structure

```text
time-management-project-group3/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── .gitignore                # Ignored files (secrets, venv, .pem)
├── src/
│   ├── client/               # Frontend Application
│   │   ├── __init__.py       # Makes client a Python package
│   │   ├── api_service.py    # API communication (safe_request, etc.)
│   │   ├── main_window.py    # UI Logic (PyQt/Tkinter window)
│   │   └── main.py           # App Entry point (starts server & GUI)
│   │
│   ├── data/                 # Shared Data & Cloud Utility Logic
│   │   ├── blobs/            # Folder for local report staging
│   │   ├── __init__.py       # Makes data a Python package
│   │   ├── dummydata.sql     # Sample data for testing
│   │   ├── reporting.py      # Report generation logic
│   │   ├── schema.sql        # Database table structure
│   │
│   └── server/               # RESTful Flask Backend
│       ├── __init__.py       # Makes server a Python package
│       ├── app.py            # Flask API routes & app.run()
│       ├── database.py       # Server-side DB pool initialization
│       ├── key_vault.py      # Server-side secret retrieval
│       └── queries.py        # SQL query execution (insert/delete)
