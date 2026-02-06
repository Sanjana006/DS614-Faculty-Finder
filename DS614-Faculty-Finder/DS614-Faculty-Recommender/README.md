# DS614 (Big Data Engineering) - Faculty Recommender System

---

# Project Overview

The **Faculty Recommender System** is an intelligent search engine designed to help students and researchers find relevant faculty members based on their research interests. Unlike simple keyword matching, this system uses a **Vector Space Model (VSM)** with **TF-IDF weighting** and **Cosine Similarity** to rank faculty profiles by relevance.

The system powers the search functionality for the Faculty Finder project, providing a semantic-aware mechanism to query faculty data scraped from the university website. It is deployed as a web application using **Streamlit** for the frontend and a custom-built Python engine for recommendation logic.

**Live Deployment:** [https://ds614-faculty-finder-production.up.railway.app](https://ds614-faculty-finder-production.up.railway.app)

---

# Tech Stack

| Category | Tools / Technologies | Purpose |
|--------|---------------------|---------|
| Programming Language | Python 3.10 | Core logic for preprocessing and recommendation |
| Frontend Framework | Streamlit | Interactive web UI for searching and displaying results |
| Algorithm | Custom TF-IDF & Cosine Similarity | Ranking faculty based on query relevance |
| Data Structure | In-Memory Inverted Index | Efficient retrieval of pre-computed vectors |
| Containerization | Docker | Containerizing the application for deployment |
| Deployment | Railway | Hosting the production application |

---

# Recommendation Algorithm

The core of this project is a custom implementation of an Information Retrieval (IR) system. It does not rely on "black box" libraries for the core logic but instead implements the mathematical foundations of text similarity from scratch.

### 1. Preprocessing (`recommender/preprocessing.py`)
Raw text from faculty profiles (bio, research interests, publications) is processed to normalize the input:
- **Case Normalization**: All text is converted to lowercase.
- **Phrase Merging**: Domain-specific terms like "computer vision" or "deep learning" are merged into single tokens (e.g., `computer_vision`) to preserve semantic meaning.
- **Cleaning**: Special characters and non-alphabetic tokens are removed.
- **Stopword Removal**: Common English words (and custom stopwords) are filtered out to focus on meaningful keywords.

### 2. Vectorization (TF-IDF) (`recommender/vectorizer.py`)
The system converts text into numerical vectors using **Term Frequency - Inverse Document Frequency (TF-IDF)**.

#### **Term Frequency (TF)**
Measures how frequently a term appears in a document relative to the document's length.

```
TF(t, d) = f(t,d) / |d|
```

**Where:**
- `t` = term (word/token)
- `d` = document (faculty profile)
- `f(t,d)` = frequency of term *t* in document *d*
- `|d|` = total number of terms in document *d*

#### **Inverse Document Frequency (IDF)**
Measures how unique a term is across all documents. Rare terms (like "Bioinformatics") receive higher weights than common terms (like "Professor").

```
IDF(t) = log((N + 1) / (DF(t) + 1)) + 1
```

**Where:**
- `N` = total number of documents (faculty profiles)
- `DF(t)` = document frequency (number of profiles containing term *t*)
- The `+1` terms provide smoothing to avoid division by zero

#### **TF-IDF Score**
The final weight for each term is computed as:

```
TF-IDF(t, d) = TF(t, d) × IDF(t)
```

### 3. Document Weighting (`recommender/index_builder.py`)
To improve relevance, different sections of a faculty profile are weighted differently before vectorization:
- **Name**: 4x weight
- **Research Interests**: 3x weight
- **Specialization**: 2x weight
- **Publications**: 2x weight
- **Bio**: 1x weight

This ensures that a match in a professor's "Research Interests" is more significant than a passing mention in their "Bio".

### 4. Similarity & Ranking (`recommender/similarity.py`)
When a user searches, their query is converted into a vector using the same TF-IDF model. The system then calculates the **Cosine Similarity** between the query vector and every faculty profile vector.

$$ \text{Cosine Similarity}(A, B) = \frac{A \cdot B}{||A|| \times ||B||} $$

**Where:**
- `A · B` = dot product of vectors A and B
- `||A||` = magnitude (Euclidean norm) of vector A
- `||B||` = magnitude (Euclidean norm) of vector B

The results are ranked by this similarity score (ranging from 0 to 1), returning the top matches.

---

# Project Structure

The project is organized to separate the core recommendation engine from the application logic and UI.

```text
DS614-Faculty-Recommender/
│
├── app/                         # Application logic
│   └── engine.py                # Search engine interface connecting UI to recommender backend
│
├── recommender/                 # Core Algorithm Implementation
│   ├── preprocessing.py         # Text cleaning and tokenization
│   ├── vectorizer.py            # Custom TF-IDF implementation
│   ├── similarity.py            # Cosine similarity and ranking logic
│   ├── index_builder.py         # Script to build and save the search index
│   └── query_parser.py          # Handles query processing
│
├── UI/                          # Frontend
│   └── streamlit_app.py         # Streamlit web interface
│
├── config/                      # Configuration files
│   └── settings.py
│
├── data/                        # Data storage
│   └── stopwords.txt            # List of stopwords to ignore
│
├── Dockerfile                   # Docker configuration for deployment
├── railway.toml                 # Railway deployment configuration
├── requirements.txt             # Project dependencies
├── start.sh                     # Startup script
└── README.md                    # Project documentation
```

---

# How to Run Manually (Local Setup)

Follow these steps to set up and run the application on your local machine.

### Prerequisites
- Python 3.8 or higher installed
- The `transformed_faculty_data.csv` file must exist in the correct data directory (checked by `config/settings.py`).

### Step 1: Create a Virtual Environment (Optional but Recommended)
It is best practice to use a virtual environment to manage dependencies.
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Build the Search Index
The recommendation engine needs a pre-computed index to work. Run this one-liner to generate it:
```bash
python -c "from recommender.index_builder import build_index; build_index()"
```
*This command reads the cleaned CSV data, computes TF-IDF vectors, and saves them to `storage/faculty_index.pkl`.*

### Step 4: Run the Streamlit App
Start the web interface:
```bash
streamlit run UI/streamlit_app.py
```
The application will open automatically in your browser at `http://localhost:8501`.

---

# How to Run with Docker

You can also run the application in a container without installing Python dependencies locally.

### Step 1: Build the Docker Image
Navigate to the `DS614-Faculty-Recommender` directory and run:
```bash
docker build -t faculty-recommender .
```

### Step 2: Run the Container
```bash
docker run -p 8080:8080 faculty-recommender
```
The app will be accessible at `http://localhost:8080`.

---

# How to Deploy

The application is designed to be deployed easily on cloud platforms like **Railway**.

### Option 1: Automatic Deployment (Recommended)
This project is configured for continuous deployment.
1. Fork this repository to your GitHub account.
2. Login to [Railway.app](https://railway.app/).
3. Click **"New Project"** -> **"Deploy from GitHub repo"**.
4. Select your forked repository.
5. Railway will automatically detect the `Dockerfile` and `railway.toml` config.
6. Click **Deploy**.

### Option 2: Manual Deployment via CLI
If you prefer identifying issues before pushing:
1. Install the Railway CLI: `npm i -g @railway/cli`
2. Login: `railway login`
3. Initialize project: `railway init`
4. Upload and deploy: `railway up`

**Production URL:** [https://ds614-faculty-finder-production.up.railway.app](https://ds614-faculty-finder-production.up.railway.app)

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

---
*This recommender system is part of the larger DS614 Faculty Finder project, demonstrating the end-to-end application of Big Data Engineering principles.*
