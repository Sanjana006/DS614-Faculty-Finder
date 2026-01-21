# DS614 (Big Data Engineering) – Faculty Finder Project

---

## 📌 Project Overview

Faculty Finder is a data engineering project that automates the entire process of collecting, cleaning, storing, and serving faculty information from the DA-IICT website. Instead of manually browsing multiple pages, the system converts scattered and unstructured faculty details such as bio, research interests, and publications into a clean, structured, and searchable format.

The project implements a complete data pipeline that includes web scraping, data transformation, database storage, and API-based data access. The processed data is stored in a SQLite database and exposed through a FastAPI REST API in JSON format, making it easy to use for analytics, machine learning, or future semantic search applications. The focus of this project is on building a reliable, modular, and real-world data pipeline that reflects how data engineering systems are designed in practice.

---

## 🎯 Problem Statement

Faculty information on university websites is often spread across multiple pages and presented in inconsistent formats, which makes it difficult to search, analyze, or reuse the data effectively. Basic keyword searches are limited and do not capture the actual research expertise or interests of faculty members.

The goal of this project is to build a system that can automatically extract faculty data, clean and standardize it, and store it in a structured form that supports efficient querying and future intelligent search. The system is designed to handle common real-world challenges such as missing information, noisy text, and inconsistent web structures, while providing easy access to the data through a RESTful API for researchers and data-driven applications.

---

## 🛠️ Tech Stack

Programming Language  
- Python – Core language for pipeline, transformation, and API

Data Ingestion  
- Scrapy – Web scraping and crawling faculty profile pages

Data Transformation  
- Pandas – Data cleaning and normalization  
- Regular Expressions (re) – Text cleaning and validation

Data Storage  
- SQLite3 – Lightweight relational database

API & Serving  
- FastAPI – REST API framework  
- Uvicorn – ASGI server

Utilities  
- Python Logging – Execution and error tracking  
- OS / Pathlib – Path and file handling

---

## 🗂️ Project Structure

DS614-Faculty-Finder  
│  
├── api  
│   ├── main.py  
│   └── routes.py  
│  
├── config  
│   └── settings.py  
│  
├── data  
│   ├── raw  
│   │   └── Faculty_DAIICT.csv  
│   ├── cleaned  
│   │   └── transformed_faculty_data.csv  
│   └── database  
│       └── faculty.db  
│  
├── ingestion  
│   └── daiict_faculty  
│       └── spiders  
│           └── daufaculty.py  
│  
├── transformation  
│   ├── normalize_text.py  
│   └── transform_pipeline.py  
│  
├── storage  
│   ├── db_connection.py  
│   └── database_insertion.py  
│  
├── scripts  
│   └── __main__.py  
│  
├── logs  
│   ├── pipeline.log  
│   ├── scraper.log  
│   └── llm_usage.md  
│  
├── requirements.txt  
├── README.md  
└── LICENSE  

---

## 🔄 Data Pipeline Description

The project follows a modular pipeline where each stage prepares data for the next.

Ingestion  
- Scrapes faculty profiles from DA-IICT website  
- Extracts name, bio, research interests, specialization, publications  
- Output stored as raw CSV  
Output: data/raw/Faculty_DAIICT.csv  

Transformation  
- Cleans HTML and encoding noise  
- Normalizes text, emails, and names  
- Generates faculty IDs  
- Creates combined_text for NLP  
Output: data/cleaned/transformed_faculty_data.csv  

Storage  
- Inserts cleaned data into SQLite  
- Auto-creates tables if missing  
- Ensures transactional safety  
Database: data/database/faculty.db  

Serving (API)  
- Exposes data via FastAPI  
- Supports /faculty and /faculty/{faculty_id} endpoints  
- Returns JSON responses  

---

## 🗄️ Database Schema

Table: faculty  

- faculty_id (TEXT, Primary Key)  
- name (TEXT)  
- mail (TEXT)  
- phd_field (TEXT)  
- specialization (TEXT)  
- bio (TEXT)  
- research (TEXT)  
- publications (TEXT)  
- combined_text (TEXT)

The combined_text field merges bio, research, specialization, and PhD field for NLP and semantic search readiness.

---

## ▶️ How the Project Works (Execution Flow)

1. Clone the repository and install dependencies from requirements.txt  
2. Review configuration in config/settings.py  
3. Scraping logic runs from ingestion/daiict_faculty/spiders/daufaculty.py  
4. Transformation runs from transformation/transform_pipeline.py  
5. Database insertion runs using storage/database_insertion.py  
6. Final unified pipeline is executed via scripts/__main__.py  
7. Logs are generated in the logs directory  
8. API is started independently from api/main.py  
9. Access all data via /faculty and individual data via /faculty/DAU001  

---

## 🛡️ Error Handling and Logging

The pipeline is designed to continue execution even when partial failures occur.

- Scraping errors are logged and skipped  
- Profiles missing mandatory fields are ignored  
- Invalid values are validated during transformation  
- Failed database rows are skipped without stopping insertion  
- Critical database errors trigger rollback  

Logs provide full transparency into pipeline execution.

---

## ⚠️ Limitations

- Scraper depends on current DA-IICT website structure  
- SQLite is not suitable for large-scale or concurrent workloads  
- API lacks pagination, filtering, and authentication  

---

## 🚀 Future Enhancements

- Semantic search using vector embeddings  
- API pagination and filtering  
- Docker-based deployment  
- Migration to PostgreSQL  
- Scheduled automated pipeline runs  

---

## 👥 Team Members

Team Name: The Data Engineers  

Sanjana Nathani  
- Student ID: 202518002  
- Program: M.Sc. Data Science  
- Institution: Dhirubhai Ambani University, Gandhinagar  
- Role: Data Engineer  

Aksh Patel  
- Student ID: 202518046  
- Program: M.Sc. Data Science  
- Institution: Dhirubhai Ambani University, Gandhinagar  
- Role: Data Engineer  

---

## 📄 License

This project is developed for academic purposes as part of the DS614 (Big Data Engineering) course.
