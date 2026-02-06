import os
import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INGESTION_ROOT = os.path.join(PROJECT_ROOT, "ingestion")
sys.path.insert(0, INGESTION_ROOT)


os.environ.setdefault(
    "SCRAPY_SETTINGS_MODULE",
    "daiict_faculty.settings"
)

from daiict_faculty.spiders.daufaculty import DaiictFacultySpider


def run_scraping_pipeline():
    # Ensure output directory exists
    os.makedirs("data/raw", exist_ok=True)

    settings = get_project_settings()
    process = CrawlerProcess(settings)

    process.crawl(DaiictFacultySpider)
    process.start()
    print("Scraping complete. Data saved to data/raw/Faculty_DAIICT.csv")

run_scraping_pipeline()