import requests
from parsel import Selector
import re

def clean(text):
    if not text:
        return None
    return re.sub(r"\s+", " ", text).replace("\xa0", " ").strip()

url = "https://www.daiict.ac.in/faculty/anil-roy"
response = requests.get(url)
sel = Selector(text=response.text)

print(f"Testing URL: {url}")
print(f"Status: {response.status_code}")

# Name
name_raw = sel.css("div.field--name-field-faculty-names::text").get()
print(f"Raw Name: '{name_raw}'")
print(f"Clean Name: '{clean(name_raw)}'")

# Check if name is found
if not clean(name_raw):
    print("FAIL: Name not found")
else:
    print("SUCCESS: Name found")

# Bio
bio_parts = sel.xpath("//div[contains(@class,'field--name-field-biography')]//text()").getall()
bio = clean(" ".join(bio_parts))
print(f"Bio length: {len(bio) if bio else 0}")
