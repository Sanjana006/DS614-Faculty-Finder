# DS614 (Big Data Engineering) 

---

# Project Overview

**Faculty Finder** is a data engineering project that automates the process of collecting, cleaning, storing, and serving faculty information from the DA-IICT website, transforming scattered and unstructured details such as bio, research interests, and publications into a clean and searchable dataset. The project follows a complete data pipeline from web scraping and data transformation to database storage and API-based access, where the processed data is stored in a SQLite database and exposed through a FastAPI REST API in JSON format, making it suitable for analytics, machine learning, and future semantic search applications.

---

# Problem Statement

Faculty information on university websites is often scattered across multiple pages and presented in inconsistent formats, making it difficult to search, analyze, or reuse effectively. This project aims to solve that problem by automatically extracting faculty data, cleaning and standardizing it, and storing it in a structured format that supports efficient querying and future intelligent search, while handling real-world issues such as missing information, noisy text, and inconsistent web structures, and providing easy access through a RESTful API.

---

# Tech Stack
| Category | Tools / Technologies | Purpose |
|--------|---------------------|---------|
| Programming Language | Python | Core language for pipeline, transformations, and API |
| Data Ingestion | Scrapy | Web scraping and crawling faculty profiles |
| Data Transformation | Pandas, Regular Expressions (re) | Data cleaning, normalization, and text processing |
| Data Storage | SQLite3 | Lightweight relational database for persistence |
| API & Serving | FastAPI, Uvicorn | Serving faculty data as JSON via REST API |
| Configuration & Utilities | Python Logging, Pathlib / OS | Logging, error handling, and path management |

---

# Project Structure

The project follows a modular and layered structure, where each directory is responsible for a specific stage of the data engineering workflow. This separation improves readability, scalability, and maintainability.

```text
DS614-Faculty-Finder/
│
├── api/                         # FastAPI application for serving data
│   ├── main.py                  # API entry point
│   └── routes.py                # API route definitions
│
├── config/                      # Configuration and pipeline flags
│   └── settings.py
│
├── data/
│   ├── raw/                   # Raw scraped CSV files
│       └── Faculty_DAIICT.csv
│   ├── cleaned/                 # Transformed and cleaned CSV files
│       └── transformed_faculty_data.csv
│   └── database/                # SQLite database files
│       └── faculty.db
│
├── ingestion/                   # Web scraping pipeline
│   └── daiict_faculty/
│       └── spiders/
│           └── daufaculty.py    # Scrapy spider for faculty profiles
│
├── transformation/              # Data cleaning and normalization
│   ├── normalize_text.py        # Text cleaning utilities
│   └── transform_pipeline.py    # Transformation pipeline
│
├── storage/                     # Database connection and insertion logic
│   ├── db_connection.py
│   └── database_insertion.py
│
├── scripts/                     # Optional helper scripts
│   └── __main__.py
├── logs/                        # Runtime and error logs
│   └── pipeline.log
│   └── scraper.log
│   └── llm_usage.md
│
├── requirements.txt             # Project dependencies
├── README.md                    # Project documentation
└── LICENSE
```

---

# Data Pipeline Description

The project implements a complete and automated data pipeline that processes faculty information from raw web pages to a structured and queryable format. Each stage of the pipeline is modular, allowing individual components to be executed, tested, and extended independently.

### 1. Ingestion

The ingestion stage collects raw faculty data from the official DA-IICT website using **Scrapy**. It crawls faculty and adjunct faculty pages, extracts profile-level details such as name, bio, research interests, and publications, handles missing fields and malformed HTML safely, and stores the scraped data as a raw CSV file. 

**Output:** `data/raw/Faculty_DAIICT.csv`



### 2. Transformation

The transformation stage cleans and standardizes the raw scraped data to ensure consistency and usability. It removes noise, normalizes text fields, and prepares the data for storage and downstream analysis by cleaning HTML tags and unwanted characters, normalizing faculty names and email addresses, standardizing research and specialization fields, generating unique faculty identifiers, and creating a `combined_text` field for NLP and semantic search use cases.  

**Output:** `data/cleaned/transformed_faculty_data.csv`



### 3. Storage

The storage stage persists the cleaned data in a relational database for efficient querying and long-term storage. A **SQLite** database is used due to its simplicity and suitability for lightweight data engineering workflows. This stage creates database tables if they do not exist, validates required fields before insertion, inserts cleaned faculty records into the database, and ensures transactional safety with rollback on failure.  

**Database:** `data/database/faculty.db`



### 4. Serving (API)

The serving stage exposes the stored faculty data through a **FastAPI-based REST API**, allowing external applications, data scientists, or search systems to access the data in a structured and scalable manner. It provides REST endpoints to fetch all faculty records or retrieve individual faculty records by ID, returns responses in JSON format, and enables easy integration with analytics workflows, machine learning models, and frontend systems.

---

# Database Schema

The project uses a **SQLite** relational database to store cleaned and structured faculty information. The schema is designed to be lightweight, easy to query, and suitable for academic as well as development-oriented use cases.

### Table: `faculty`

| Column Name     | Data Type | Description |
|-----------------|-----------|-------------|
| faculty_id      | TEXT      | Unique identifier for each faculty member (Primary Key) |
| name            | TEXT      | Faculty member’s full name |
| mail            | TEXT      | Official email address |
| phd_field       | TEXT      | Educational background / PhD field |
| specialization  | TEXT      | Areas of specialization (comma-separated) |
| bio             | TEXT      | Faculty biography |
| research        | TEXT      | Research interests and focus areas |
| publications    | TEXT      | List of publications (stored as text) |
| combined_text   | TEXT      | Combined textual representation for search and NLP |

The `faculty_id` column serves as the primary key to ensure uniqueness across records. Text-based fields are used to accommodate variable-length content such as biographies, research descriptions, and publication details.

The `combined_text` field is generated by combining the faculty biography (`bio`), research interests (`research`), areas of specialization (`specialization`), and educational background (`phd_field`) into a single, rich text representation. This field is specifically designed to support downstream NLP tasks and future semantic or vector-based search functionality.

---

# How to run the pipeline (Step-by-Step Execution Flow)

This project is organized as a modular data engineering system where each component has a clear responsibility. The workflow is designed so that a reviewer can either inspect individual modules or run the complete pipeline end-to-end without confusion.

### Step 1: Clone the Repository and Prepare the Environment
After cloning the repository, the reviewer installs the required dependencies listed in `requirements.txt`. All configurable parameters such as file paths, database location, and pipeline control flags are defined in `config/settings.py`. These settings decide whether the ingestion, transformation, and database stages should run, without requiring any changes to the core code.



### Step 2: Understanding the Modular Pipeline Design
The project is divided into four logical modules:
- **Ingestion**: Scrapes raw faculty data from the DA-IICT website  
- **Transformation**: Cleans and normalizes the scraped data  
- **Storage**: Stores cleaned data into a SQLite database  
- **Serving (API)**: Exposes stored data through a FastAPI application  

Each module can be understood independently, but they are also connected through a final unified pipeline.



### Step 3: Ingestion Module (Web Scraping)
The ingestion logic is implemented using Scrapy in the file:

`ingestion/daiict_faculty/spiders/daufaculty.py`

This spider crawls official DAU (formerly DA-IICT) faculty pages and extracts information such as faculty name, bio, research interests, specialization, and publications. The scraped output is stored exactly as collected in:

`data/raw/Faculty_DAIICT.csv`

This raw file is intentionally preserved so that the original data source can always be inspected or reprocessed if needed.



### Step 4: Transformation Module (Data Cleaning)
The transformation logic is implemented in:

`transformation/transform_pipeline.py`

This module reads the raw CSV file from `data/raw/Faculty_DAIICT.csv` and performs cleaning and normalization steps such as removing HTML noise, fixing encoding issues, validating emails, normalizing text fields, and generating unique faculty IDs. Multiple descriptive fields (bio, research, specialization, and PhD field) are merged into a single `combined_text` column for future NLP use.

The cleaned output is written to:

`data/cleaned/transformed_faculty_data.csv`



### Step 5: Storage Module (SQLite Database)
The storage layer is responsible for persisting the cleaned data. Database connection and schema creation are handled in:

`storage/db_connection.py`

Data insertion logic is implemented in:

`storage/database_insertion.py`

If the database or required tables do not exist, they are created automatically. The cleaned data from `data/cleaned/transformed_faculty_data.csv` is inserted into the SQLite database located at:

`data/database/faculty.db`

Each record is inserted safely, and any problematic rows are logged without stopping the entire insertion process.



### Step 6: Running the Final Unified Pipeline
Instead of manually running each module, the project provides a final pipeline runner located at:

`scripts/__main__.py`

When this file is executed, it sequentially runs:
1. The ingestion module (scraping)
2. The transformation module (cleaning)
3. The storage module (database insertion)

This ensures a clean and reproducible execution flow. Logs generated during execution are stored in the `logs/` directory for transparency and debugging.



### Step 7: Serving the Data Through the API
Once the database is populated, the API can be started independently. The FastAPI application entry point is:

`api/main.py`

To view all faculty records, the user can append `/faculty` to the base URL after starting the server. To retrieve details of a specific faculty member, the endpoint `/faculty/{faculty_id}` can be used, for example `/faculty/DAU001`. All responses are returned in JSON format, making the data easy to consume for evaluation, analytics, or future machine learning and semantic search applications.



### Step 8: Final Outcome
At the end of execution, the project delivers a complete and traceable data system: raw data is preserved, cleaned data is structured, the database ensures persistence, and the API provides controlled access. The modular design ensures that each step is transparent, testable, and easy to verify for anyone reviewing the project.

---

# Error Handling and Logging

To make the pipeline reliable and reviewer-proof, the project includes practical error handling at every critical stage. Instead of failing fast, the system is designed to **log issues, skip problematic data, and continue execution safely**.

**Scraping-Level Safety**  
Network issues and unreachable pages are handled using Scrapy’s error callback, ensuring the crawler continues even if some requests fail.

    def errback_http(self, failure):
        self.logger.error(f"HTTP error occurred: {repr(failure)}")

Profiles missing mandatory information (such as faculty name) are skipped explicitly to prevent corrupted records from entering the dataset.

    if not name:
        raise DropItem("Faculty name missing")

**Transformation-Level Validation**  
During data cleaning, invalid or malformed values are handled using validation logic instead of raising exceptions. This ensures noisy real-world data does not interrupt the pipeline.

    def validate_email(email):
        return email if isinstance(email, str) and "@" in email else None

**Database-Level Protection**  
Each faculty record is inserted individually. If a single record fails due to data inconsistency, it is logged and skipped without stopping the full insertion process.

    try:
        cursor.execute(insert_query, (...))
    except Exception as row_error:
        logger.warning("Failed to insert row: %s", row_error)

If a critical database error occurs, the transaction is rolled back to maintain data integrity.

    except Exception as e:
        conn.rollback()
        raise RuntimeError(f"Data insertion error: {e}")

**Logging Strategy**  
Across all stages, Python’s logging module records execution flow, warnings, and failures. This makes debugging straightforward and ensures anyone reviewing the project can clearly understand what happened, where, and why.

Overall, this approach makes the pipeline fault-tolerant, transparent, and suitable for real-world data engineering scenarios where imperfect data is common.

---

# Beneftis

The project is designed to be flexible and easy to adapt for different use cases. Configuration parameters such as file paths, database location, and pipeline execution flags can be modified through `config/settings.py` without changing the core code. The modular structure allows individual components—ingestion, transformation, storage, and API—to be run, tested, or extended independently. 

Raw and cleaned datasets are preserved at each stage, enabling reproducibility and easy debugging. Overall, this design makes the project simple to configure, maintain, and extend for future enhancements or similar data engineering tasks.

---

# Limitations

While the project provides a complete and functional data pipeline, it has certain limitations by design. The scraper is tailored specifically to the current structure of the DA-IICT website, and significant changes to the website layout may require updates to the scraping logic.

The project uses SQLite, which is suitable for lightweight storage and academic use but may not scale efficiently for very large datasets or high-concurrency environments. Additionally, the API currently supports basic retrieval operations and does not include advanced filtering, pagination, or authentication mechanisms.

---

# Future Enhancements

This project is designed with extensibility in mind, and several improvements can be added in future iterations. A natural next step is to implement semantic search by generating vector embeddings from the `combined_text` field, allowing users to search faculty profiles using natural language queries. The API can be enhanced with filtering, pagination, and authentication to support more advanced use cases. For improved scalability and deployment, the pipeline and API can be containerized using Docker, and the SQLite database can be replaced with a production-grade relational database such as PostgreSQL. Additionally, automated scheduling and monitoring can be introduced to enable periodic data updates and long-term maintenance.

---

# Team Members

### Team Name: The Data Engineers

👩‍💻 **Sanjana Nathani**  
- **Student ID:** 202518002  
- **Program:** M.Sc. Data Science  
- **Institution:** Dhirubhai Ambani University (DAU), Gandhinagar  
- **Role in Project:** Data Engineer  



👨‍💻 **Aksh Patel**  
- **Student ID:** 202518046  
- **Program:** M.Sc. Data Science  
- **Institution:** Dhirubhai Ambani University (DAU), Gandhinagar  
- **Role in Project:** Data Engineer  



Together, the team collaborated on designing a modular, reliable, and scalable data engineering solution, ensuring clarity, robustness, and ease of evaluation.
