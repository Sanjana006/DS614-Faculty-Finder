# LLM Usage in the project. 

---

## Prompt 1
I am using Scrapy to crawl a university website and extract faculty profile links. I want to understand how to safely fetch all anchor tag links from a page and iterate over them, while ignoring invalid or malformed href values that could break the crawler. How can this be done in Scrapy in a clean and reliable way?

## Output
To safely extract and iterate over links in Scrapy, the response object provides selector methods that allow access to HTML elements in a structured way. Anchor tag links can be collected by selecting all href attributes from <a> tags using CSS selectors. This returns a list of link values present on the page.
Before processing each link, it is important to validate the extracted values. Empty links, None values, or malformed strings (such as those containing raw HTML fragments) should be ignored to prevent runtime errors or unintended crawling behavior. Adding simple conditional checks while iterating over the links ensures that only valid URLs are processed further.
By combining structured link extraction with basic validation and filtering, a Scrapy crawler can remain stable and reliable even when dealing with imperfect or inconsistent HTML content commonly found on real-world websites.

✅ Scrapy Code Implementation (Matching the Explanation)

    links = response.css("a[href]::attr(href)").getall()

    for link in links:
        # Skip empty or malformed href values
        if not link or "<" in link:
            continue

        # Process only valid links
        yield response.follow(link, callback=self.parse_profile)

---

## Prompt 2
Give me a general scrapy code to parse the profile of each faculty with a brief explanation. Also with handling the errors.

## Output
✅ Example: Parsing Faculty Profile Pages in Scrapy

import scrapy
from scrapy.exceptions import DropItem

class FacultySpider(scrapy.Spider):
    name = "faculty_spider"
    allowed_domains = ["example-university.edu"]
    start_urls = ["https://example-university.edu/faculty"]

    def parse(self, response):
        """
        Extracts profile links from the listing page
        and schedules requests to individual profile pages.
        """
        profile_links = response.css("a[href*='faculty']::attr(href)").getall()

        for link in profile_links:
            if not link or "<" in link:
                continue
            yield response.follow(link, callback=self.parse_profile)

    def parse_profile(self, response):
        """
        Parses an individual faculty profile page
        and extracts structured faculty information.
        """
        try:
            name = response.css("h1::text").get()
            bio = " ".join(
                response.css("div.bio *::text").getall()
            ).strip()

            email = response.css("a[href^='mailto:']::attr(href)").get()
            email = email.replace("mailto:", "") if email else None

            # Mandatory field check
            if not name:
                raise DropItem("Faculty name missing")

            yield {
                "name": name.strip(),
                "email": email,
                "bio": bio if bio else None,
                "profile_url": response.url
            }

        except DropItem:
            # Skip incomplete profiles safely
            return

        except Exception as e:
            # Log unexpected parsing issues
            self.logger.error(
                f"Error parsing profile {response.url}: {str(e)}"
            )

**✅ Why this code is solid for evaluation**
- Modular (parse → parse_profile)
- Uses Scrapy best practices
- Handles missing fields gracefully
- Logs errors instead of crashing
- Easy to adapt to any university website

---

## Prompt 3
I am doing a project on Big Data Engineering, where I have a huge data of text filled with HTML tags. I have to create a pipeline which cleans it properly, give me a general code snippet, how can I clean it, also give me options where I can perform the cleaning.

## Output
**1️⃣ General Code Snippet: Cleaning HTML-Heavy Text**
This is a core text-cleaning function you can plug into any data pipeline (Scrapy, Pandas, Spark, etc.).

import re
import unicodedata
from html import unescape

def clean_html_text(text):
    if not isinstance(text, str):
        return None

    # Decode HTML entities (&amp;, &nbsp;, etc.)
    text = unescape(text)

    # Remove HTML tags
    text = re.sub(r"<.*?>", " ", text)

    # Normalize unicode characters
    text = unicodedata.normalize("NFKD", text)

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", " ", text)

    # Remove special characters except basic punctuation
    text = re.sub(r"[^a-zA-Z0-9.,;:()\- ]", " ", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text.lower()

**What this function does (briefly)**
- Removes HTML tags
- Fixes HTML entities
- Normalizes unicode noise
- Removes URLs and unwanted symbols
- Produces clean, lowercase text
- This is suitable for analytics, NLP, embeddings, and ML pipelines.

**2️⃣ Where Can This Cleaning Be Performed? (Very Important for Big Data)**
In a Big Data Engineering pipeline, cleaning does NOT have to happen in only one place.
Below are valid architectural options, each with its own purpose

- Option 1: During Ingestion (Scraping Layer)
📍 Where: Web scraper (Scrapy / Requests / BeautifulSoup)

    raw_text = response.css("div.bio").get()
    clean_text = clean_html_text(raw_text)

- Option 2: During Transformation (Recommended & Best Practice)
📍 Where: Pandas / Spark / DataFrame-based transformation layer

df["clean_bio"] = df["bio"].apply(clean_html_text)

- Option 3: During Storage (Pre-Insert Cleaning)
📍 Where: Right before inserting into database

record["bio"] = clean_html_text(record["bio"])
insert_into_db(record)

- Option 4: During Serving (API-Level Cleaning)
📍 Where: API response layer

return {
    "bio": clean_html_text(row["bio"])
}

- Option 5: Big Data / Distributed Processing (Spark)
📍 Where: Spark ETL layer

from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

clean_udf = udf(clean_html_text, StringType())
df = df.withColumn("clean_text", clean_udf(df["raw_text"]))

---

## Prompt 4
As a Data Engineer, which relational database would be suitable for efficiently storing data that needs to be served through an API for academic purpose?

## Output
For an academic-purpose data engineering project where data needs to be efficiently stored and served through an API, the most suitable relational databases are:

**✅ SQLite (Best for Academic & Small-Scale Projects)**

Why SQLite is ideal for your use case:
- Lightweight and serverless (no setup or admin overhead)
- Easy to integrate with FastAPI / Flask
- Supports standard SQL queries
- Perfect for single-user or low-concurrency academic projects
- Simple to distribute and evaluate (just a .db file)

When to choose SQLite:
- Course projects
- Prototypes
- Local testing
- Small to medium datasets
- When simplicity and clarity matter more than scalability
👉 This is why SQLite is commonly used in MS-level data engineering projects.

**🔄 PostgreSQL (If You Want a More Production-Oriented Choice)**

Why PostgreSQL is also a good option:
- Strong support for complex queries and indexing
- Handles concurrent API requests well
- Industry-standard relational database
- Easy migration path from SQLite

When to choose PostgreSQL:
- If you want to demonstrate industry readiness
- Multi-user access
- Larger datasets
- Advanced querying needs

**🆚 Quick Comparison**

| Database   | Best For                          | Complexity | Academic Suitability |
| ---------- | --------------------------------- | ---------- | -------------------- |
| SQLite     | Small-scale, academic projects    | Very Low   | ⭐⭐⭐⭐⭐                |
| PostgreSQL | Scalable, production-like systems | Medium     | ⭐⭐⭐⭐                 |

**🎓 Recommended Academic Answer (You can use this)**

For academic purposes, SQLite is a suitable relational database due to its simplicity, lightweight nature, and ease of integration with APIs, while still supporting structured queries and persistent storage.

---


## Prompt 5
How can I use FastAPI to connect to a database and show all the stored data through an API endpoint? Give me a code snippet for better understanding

## Output
Below is a simple, general FastAPI example that shows how to connect to a database and return all stored data through an API endpoint.
This is easy to understand, academically safe, and matches common data-engineering practice.

**General Idea (Short & Clear)**
FastAPI acts as the API layer that connects to a database, executes a query to fetch records, and returns the results in JSON format. The database connection is opened when a request is received and safely closed after the data is fetched.

### Example Code: FastAPI + SQLite (Fetch All Records)
import sqlite3
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Example Data API")

DB_PATH = "data/database/faculty.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/records")
def get_all_records():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM faculty")
        rows = cursor.fetchall()

        results = [dict(row) for row in rows]
        return {"count": len(results), "data": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        conn.close()

**Brief Explanation**
- A FastAPI app is created to handle incoming HTTP requests.
- A database connection function is used to connect to SQLite.
- The /records endpoint executes a SQL query to fetch all rows from the table.
- The result is converted into dictionaries and returned as JSON.
- Errors are handled gracefully without crashing the API.

**How to Access the Data**
After starting the API server, open:

http://127.0.0.1:8000/records

This endpoint will return all stored data from the database in JSON format.

## Prompt 6
Act as a senior backend/data engineer.
List the recommended production-grade exception handling pattern for SQLite in Python
and provide a concise checklist of best practices.
Focus only on transaction safety, rollback strategy, and error categorization.
Return clean, copy-paste-ready code and a short checklist.

Got it 
##  Recommended Exception Handling Pattern (BEST PRACTICE)

```python
import sqlite3
import logging

logger = logging.getLogger(__name__)

conn = None
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(SQL_QUERY)
    conn.commit()

except sqlite3.IntegrityError as e:
    if conn:
        conn.rollback()
    logger.warning("Integrity constraint violated: %s", e)

except sqlite3.OperationalError as e:
    if conn:
        conn.rollback()
    logger.error("Operational error: %s", e)
    raise

except sqlite3.DatabaseError as e:
    if conn:
        conn.rollback()
    logger.critical("Critical database error: %s", e)
    raise

except Exception as e:
    if conn:
        conn.rollback()
    logger.exception("Unexpected error")
    raise

finally:
    if conn:
        conn.close()
```

---

## Exception Handling Checklist (MEMORIZE)

* ✔ Always rollback on failure
* ✔ Always close the database connection
* ✔ Catch **specific SQLite exceptions first**
* ✔ Log errors before re-raising
* ✔ Never silently swallow database errors

---

###  One-line takeaway

**This pattern prevents data corruption, connection leaks, and silent failures in SQLite-based systems.**
