# DS614 - Big Data Engineering Project: Faculty Finder & Recommender

**Live Deployment:** [https://ds614-faculty-finder-production.up.railway.app](https://ds614-faculty-finder-production.up.railway.app)

---

## Project Overview

This repository houses the complete end-to-end solution for the **DS614 Big Data Engineering** project. It consists of two main components working in tandem:

1.  **Faculty Finder (Data Pipeline)**: A robust ETL pipeline that scrapes, cleans, and stores faculty data from the university website.
2.  **Faculty Recommender (Application)**: An intelligent search engine that allows users to find faculty members based on research interests using a custom Vector Space Model.

---

## Repository Modules

The project is structured into two distinct modules, each responsible for a specific part of the system:

| Module | Description | Key Technologies |
| :--- | :--- | :--- |
| **[`DS614-Faculty-Finder`](./DS614-Faculty-Finder)** | **The Backend / Data Pipeline**. Handles data scraping (Ingestion), cleaning (Transformation), and storage (SQLite). | Python, Scrapy, Pandas, SQLite, FastAPI |
| **[`DS614-Faculty-Recommender`](./DS614-Faculty-Recommender)** | **The Frontend / Search Engine**. Implements the recommendation logic and user interface. | Python, Streamlit, Scikit-learn (custom implementation), Docker |

---

## Documentation & Setup

Each module handles its own dependencies and execution instructions. Please refer to the specific README files for detailed setup guides.

### 1. Data Pipeline Setup
For instructions on running the scraper, cleaning data, and querying the database, refer to:
👉 **[Faculty Finder Documentation](./DS614-Faculty-Finder/README.md)**

### 2. Search Application Setup
For instructions on running the recommendation engine, building the search index, and starting the web UI, refer to:
👉 **[Faculty Recommender Documentation](./DS614-Faculty-Recommender/README.md)**

**Quick Start (Docker):**
The search application is containerized and can be run immediately with Docker:
```bash
cd DS614-Faculty-Recommender
docker build -t faculty-app .
docker run -p 8080:8080 faculty-app
```
Click on the link: 
```bash
Local URL: [http://localhost:8080]
```
---

## Recommendation Algorithm

The search engine moves beyond simple keyword matching by implementing a **Vector Space Model (VSM)** from scratch:

- **Preprocessing**: Handles raw text by tokenizing, removing stopwords, and merging domain-specific phrases (e.g., "Deep Learning" becomes `deep_learning`).
- **Weighting (TF-IDF)**: Uses Term Frequency-Inverse Document Frequency to prioritize unique and meaningful terms over common words.
- **Ranking (Cosine Similarity)**: Results are ranked based on the cosine similarity between the user's query vector and the faculty profile vectors.
- **Field Boosting**: Different sections of a profile are weighted differently; for example, a match in "Research Interests" (3x weight) is considered more relevant than a match in the "Bio".

---

## Deployment

The application is deployed on Railway and is accessible publicly for demonstration:
👉 **[Faculty Finder Production App](https://ds614-faculty-finder-production.up.railway.app)**

---

## Application Screenshots

The following screenshots demonstrate the Faculty Finder application in action:

### 🏠 Home Page - Search Interface
![Home page showing the DAIICT Faculty Finder search interface with display settings and smart search tips](./Screenshots/SS%201.png)

### 🔍 Search Example: Speech Recognition
![Search results for "speech recognition" query showing 3 matching faculty members with match scores](./Screenshots/SS%202.png)

### 📊 Faculty Results with Match Scores
![Detailed faculty profiles showing research interests, courses, and relevance scores](./Screenshots/SS%203.png)

### 💡 Search Example: NLP
![Search results for "NLP" showing 5 matching faculty members with their expertise areas](./Screenshots/SS%204.png)

### 🎯 Ranked Results Display
![Faculty search results ranked by cosine similarity scores with detailed research interests](./Screenshots/SS%205.png)

---

## Team

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

---
*This recommender system is part of the larger DS614 Faculty Finder project, demonstrating the end-to-end application of Big Data Engineering principles.*
