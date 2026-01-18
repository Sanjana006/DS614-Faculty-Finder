import os
import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# --------------------------------------------------
# ✅ Fix Python path (project root)
# --------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

# --------------------------------------------------
# ✅ Tell Scrapy where settings.py is
# --------------------------------------------------
os.environ.setdefault(
    "SCRAPY_SETTINGS_MODULE",
    "ingestion.daiict_faculty.settings"
)

from ingestion.daiict_faculty.spiders.daufaculty import DaiictFacultySpider


def run():
    # Ensure output directory exists
    os.makedirs("data/raw", exist_ok=True)

    settings = get_project_settings()
    process = CrawlerProcess(settings)

    process.crawl(DaiictFacultySpider)
    process.start()


if __name__ == "__main__":
    run()
