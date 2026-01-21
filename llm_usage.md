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

Option 1: During Ingestion (Scraping Layer)
📍 Where: Web scraper (Scrapy / Requests / BeautifulSoup)

    raw_text = response.css("div.bio").get()
    clean_text = clean_html_text(raw_text)

