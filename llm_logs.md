# LLM Interaction Logs

This document contains realistic questions asked to LLMs during Faculty Finder development, including debugging scenarios, deployment issues, and complex integration problems.

---

## Question 1: scrapy spider runs but saves empty csv file, the items are being yielded i can see them in logs but csv has only headers???

**Context:** Scraping faculty data from university website using Scrapy

**LLM Generated Output:**

This is a classic Scrapy pipeline issue. The items are being created but not reaching the export pipeline. Here are the most likely causes:

**1. Items Not Being Returned Properly:**
```python
# ❌ WRONG - Using print instead of yield
def parse(self, response):
    for faculty in response.css('.faculty-card'):
        item = {
            'name': faculty.css('.name::text').get(),
            'email': faculty.css('.email::text').get()
        }
        print(item)  # This won't export to CSV!

# ✅ CORRECT - Must use yield or return
def parse(self, response):
    for faculty in response.css('.faculty-card'):
        item = {
            'name': faculty.css('.name::text').get(),
            'email': faculty.css('.email::text').get()
        }
        yield item  # This exports to CSV
```

**2. FEED_EXPORT Settings Not Configured:**
```python
# In settings.py or custom_settings
FEEDS = {
    'faculty_data.csv': {
        'format': 'csv',
        'encoding': 'utf8',
        'store_empty': False,  # Don't create file if no items
        'overwrite': True,
    }
}

# Or use command line
# scrapy crawl faculty_spider -o faculty_data.csv
```

**3. Item Pipeline Dropping Items:**
```python
# Check your pipelines.py
class FacultyPipeline:
    def process_item(self, item, spider):
        # ❌ WRONG - Forgot to return item
        if item.get('name'):
            item['name'] = item['name'].strip()
        # Missing return statement!

# ✅ CORRECT - Must return item
class FacultyPipeline:
    def process_item(self, item, spider):
        if item.get('name'):
            item['name'] = item['name'].strip()
        return item  # Critical!
```

**Debugging Steps:**
1. Check spider logs for "Scraped from" messages - if missing, items aren't yielded
2. Add logging to pipeline: `logger.info(f"Processing item: {item}")`
3. Verify CSV file permissions and path
4. Run with verbose logging: `scrapy crawl faculty_spider -L DEBUG`
5. Check if `DropItem` exception is being raised in pipelines

---

## Question 2: railway deployment failing with "Script start.sh not found" and "Railpack could not determine how to build the app" even though i have Dockerfile???

**Context:** Deploying Faculty Finder Streamlit app to Railway.app

**LLM Generated Output:**

This is the **exact error** you'll see when Railway ignores your Dockerfile and tries to use Railpack auto-detection instead. Here's what's happening and how to fix it:

**The Error:**
```
⚠ Script start.sh not found
✖ Railpack could not determine how to build the app.

The following languages are supported:
Php
Golang
Java
Rust
Ruby
Elixir
Python
Deno
Dotnet
```

**Root Cause:**
Railway's auto-detection (Railpack) is running instead of using your Dockerfile. This happens when:
1. `railway.toml` is missing from the repository root
2. `railway.toml` exists but has incorrect configuration
3. Root Directory setting in Railway dashboard points to wrong folder
4. Case sensitivity issues in `railway.toml` values

**Solution 1: Create railway.toml in Repository Root (BEST FIX)**

If your project structure is:
```
DS614-Faculty-Finder/          # Repository root
├── DS614-Faculty-Finder/      # Backend module
├── DS614-Faculty-Recommender/ # Frontend module (has Dockerfile)
│   ├── Dockerfile
│   ├── requirements.txt
│   └── UI/streamlit_app.py
└── railway.toml               # CREATE THIS HERE
```

Create `railway.toml` at repository root:
```toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "DS614-Faculty-Recommender/Dockerfile"

[deploy]
restartPolicyType = "ON_FAILURE"
```

**CRITICAL: Case Sensitivity!**
- ✅ `builder = "DOCKERFILE"` (uppercase)
- ❌ `builder = "dockerfile"` (lowercase won't work)
- ✅ `restartPolicyType = "ON_FAILURE"` (uppercase with underscores)
- ❌ `restartPolicyType = "on_failure"` (lowercase won't work)

**Solution 2: Set Root Directory in Railway Dashboard**

If you don't want to modify the repo structure:
1. Go to Railway dashboard
2. Click on your service (e.g., "overflowing-rebirth")
3. Go to **Settings** → **Root Directory**
4. Set to: `DS614-Faculty-Recommender`
5. Save and redeploy

This tells Railway to look inside the subdirectory where your `railway.toml` and `Dockerfile` exist.

**Solution 3: Verify Dockerfile Uses Railway's PORT Variable**

Ensure your Dockerfile uses the `$PORT` environment variable:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Railway provides PORT dynamically
EXPOSE 8080

# Use $PORT variable (Railway will inject this)
CMD ["sh", "-c", "streamlit run UI/streamlit_app.py --server.port=${PORT:-8080} --server.address=0.0.0.0"]
```

**Common Mistakes:**
- ❌ Hardcoding port 8501 instead of using `$PORT`
- ❌ Using lowercase in `railway.toml` (`builder = "dockerfile"`)
- ❌ Missing `railway.toml` in repository root
- ❌ Wrong `dockerfilePath` (doesn't match actual Dockerfile location)
- ❌ Dockerfile not in the configured directory

**Debugging Steps:**
1. Check Railway build logs for "Railpack" messages
2. Verify `railway.toml` exists: `git ls-files | grep railway.toml`
3. Check case sensitivity in `railway.toml`
4. Test Dockerfile locally: `docker build -t test -f DS614-Faculty-Recommender/Dockerfile .`
5. Verify Root Directory setting in Railway dashboard
6. Check that Dockerfile path in `railway.toml` matches actual location

**After Fix:**
Railway will:
1. Read `railway.toml` from repository root
2. Use Docker builder instead of Railpack
3. Build using the specified Dockerfile
4. Deploy successfully ✅

**Real Example from Faculty Finder:**
```bash
# Before fix - Railway logs showed:
⚠ Script start.sh not found
✖ Railpack could not determine how to build the app.

# After creating railway.toml with correct config:
✓ Using Dockerfile builder
✓ Building Docker image
✓ Deployment successful
```

---

## Question 3: sqlite3.OperationalError: database is locked when trying to insert faculty data from multiple scrapy requests

**Context:** Storing scraped faculty data in SQLite database

**LLM Generated Output:**

SQLite doesn't handle concurrent writes well. This is a common issue when Scrapy's concurrent requests try to write simultaneously.

**Problem:** SQLite locks the entire database file during writes, causing conflicts.

**Solution 1: Use Connection Pooling with Timeouts**
```python
import sqlite3
from pathlib import Path

class SqlConnectionManager:
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
    
    def connection(self):
        try:
            # Add timeout and isolation level
            conn = sqlite3.connect(
                self.db_path,
                timeout=30.0,  # Wait up to 30 seconds for lock
                isolation_level='DEFERRED',  # More permissive locking
                check_same_thread=False
            )
            conn.execute("PRAGMA journal_mode=WAL;")  # Write-Ahead Logging
            conn.execute("PRAGMA busy_timeout=30000;")  # 30 second timeout
            return conn
        except sqlite3.DatabaseError as e:
            raise RuntimeError(f"Database connection error: {e}")
```

**Solution 2: Limit Scrapy Concurrency**
```python
# In settings.py
CONCURRENT_REQUESTS = 1  # Only 1 request at a time
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 0.5  # Half second between requests

# Or use AutoThrottle
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 3
```

**Solution 3: Use WAL Mode (Write-Ahead Logging)**
```python
# Enable WAL mode for better concurrency
conn = sqlite3.connect('faculty.db')
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA synchronous=NORMAL;")  # Faster writes
conn.close()

# WAL allows multiple readers + 1 writer simultaneously
```

---

## Question 4: fastapi cors error when calling from streamlit app, added CORSMiddleware but still getting blocked by cors policy

**Context:** Streamlit frontend calling FastAPI backend on different ports/domains

**LLM Generated Output:**

CORS issues with FastAPI usually involve incorrect middleware configuration or origin mismatches.

**Solution: Proper CORS Configuration**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Faculty Finder API",
    description="API to fetch faculty details",
    version="1.0.0"
)

# ✅ CORRECT - Middleware BEFORE routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",  # Streamlit default port
        "http://localhost:8080",
        "https://your-app.railway.app",
        "https://ds614-faculty-finder-production.up.railway.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)  # Routes added after middleware
```

---

## Question 5: tf-idf cosine similarity returning same scores for all faculty, search results are not ranked properly

**Context:** Implementing custom Vector Space Model for faculty search

**LLM Generated Output:**

This usually means your TF-IDF vectors are not being calculated correctly, or all documents have identical vectors.

**Common Issues:**

**1. IDF Not Calculated (All Terms Have Same Weight):**
```python
# ❌ WRONG - Only using term frequency, no IDF
def calculate_tfidf(term, doc, all_docs):
    tf = doc.count(term) / len(doc)
    return tf  # Missing IDF!

# ✅ CORRECT - Include IDF calculation
import math

def calculate_tfidf(term, doc, all_docs):
    tf = doc.count(term) / len(doc) if len(doc) > 0 else 0
    docs_with_term = sum(1 for d in all_docs if term in d)
    idf = math.log(len(all_docs) / (1 + docs_with_term))
    return tf * idf
```

**2. Not Normalizing Vectors:**
```python
# ❌ WRONG - Vectors not normalized
def cosine_similarity(vec1, vec2):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    return dot_product  # Missing normalization!

# ✅ CORRECT - Normalize vectors
import math

def cosine_similarity(vec1, vec2):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)
```

---

## Question 6: sqlite query returns None when faculty exists, checked with DB Browser and data is there

**Context:** Querying faculty database from FastAPI endpoint

**LLM Generated Output:**

This is usually a case sensitivity issue or not fetching results properly.

**Common Issues:**

**1. Case-Sensitive LIKE Queries:**
```python
# ❌ WRONG - SQLite LIKE is case-sensitive by default
cursor.execute("""
    SELECT * FROM faculty 
    WHERE name LIKE ?
""", (f"%{search_term}%",))

# ✅ CORRECT - Use COLLATE NOCASE
cursor.execute("""
    SELECT * FROM faculty 
    WHERE name LIKE ? COLLATE NOCASE
""", (f"%{search_term}%",))
```

**2. Not Fetching Results:**
```python
# ❌ WRONG - Execute but don't fetch
cursor.execute("SELECT * FROM faculty WHERE faculty_id = ?", (id,))
return cursor  # Returns cursor object, not data!

# ✅ CORRECT - Fetch results
cursor.execute("SELECT * FROM faculty WHERE faculty_id = ?", (id,))
result = cursor.fetchone()
return result
```

**3. Row Factory Not Set:**
```python
# ✅ CORRECT - Use Row factory for dict-like access
import sqlite3

conn = sqlite3.connect('faculty.db')
conn.row_factory = sqlite3.Row  # Enable dict-like access
cursor = conn.cursor()
cursor.execute("SELECT * FROM faculty")
row = cursor.fetchone()
print(row['name'])  # Works!
```

---

## Question 7: pandas read_csv works locally but fails on railway with "FileNotFoundError" even though file is in repo

**Context:** Loading cleaned faculty data CSV in data pipeline

**LLM Generated Output:**

This is a path issue - relative paths work locally but break in production.

**Solution: Use Absolute Paths Relative to Script**
```python
# ❌ WRONG - Relative to current working directory
df = pd.read_csv('data/cleaned/faculty_cleaned.csv')

# ✅ CORRECT - Relative to script location
from pathlib import Path

BASE_DIR = Path(__file__).parent
CSV_PATH = BASE_DIR / 'data' / 'cleaned' / 'faculty_cleaned.csv'
df = pd.read_csv(CSV_PATH)
```

**Check File Exists:**
```python
from pathlib import Path

def load_faculty_data():
    base_dir = Path(__file__).parent
    csv_path = base_dir / 'data' / 'cleaned' / 'faculty_cleaned.csv'
    
    if not csv_path.exists():
        raise FileNotFoundError(f"Faculty data not found at {csv_path}")
    
    return pd.read_csv(csv_path)
```

---

## Question 8: streamlit app works locally but crashes on railway with "ModuleNotFoundError" even though requirements.txt has all packages

**Context:** Deploying Streamlit Faculty Recommender to Railway

**LLM Generated Output:**

This is usually a path issue or missing dependencies.

**1. Relative Import Issues:**
```python
# ❌ WRONG - Relative imports break in production
from utils.search import search_faculty

# ✅ CORRECT - Absolute imports
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from faculty_recommender.utils.search import search_faculty
```

**2. Missing requirements.txt Entries:**
```txt
# Make sure ALL dependencies are listed
streamlit>=1.28.0
pandas>=2.0.0
scikit-learn>=1.3.0
numpy>=1.24.0
altair>=5.0.0  # Streamlit dependency
```

**3. Missing Data Files:**
```python
# ✅ CORRECT - Relative to script location
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "data" / "database" / "faculty.db"
```

---

## Notes

- These are real debugging scenarios from Faculty Finder development
- Tech stack: SQLite, Scrapy, FastAPI, Streamlit, Railway, custom TF-IDF/VSM
- Focus on production deployment issues, database queries, and search algorithm bugs
- Date: February 2026