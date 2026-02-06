"""
This script runs the complete data engineering pipeline:
1. Ingestion (Web Scraping using Scrapy)
2. Transformation (Data Cleaning and Normalization)
3. Storage (SQLite Database Insertion)

Each stage can be enabled or disabled using flags in config/settings.py.
"""

import sys
import os
import logging
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.settings import (
    RAW_DATA_PATH,
    CLEANED_DATA_PATH,
    DATABASE_PATH,
    ENABLE_SCRAPING,
    ENABLE_TRANSFORMATION,
    ENABLE_DATABASE_INSERTION,
)

from transformation.transform_pipeline import transform_file
from storage.database_insertion import DataInsertion

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

def run_pipeline():
    logger.info("Pipeline started")

    try:
        # ------------------ INGESTION ------------------
        if ENABLE_SCRAPING:
            logger.info("Starting ingestion (Scrapy) step")

            # Run Scrapy in a separate process to avoid Twisted reactor issues
            subprocess.run(
                [sys.executable, "ingestion/run_scrapper.py"],
                check=True,
                cwd=project_root
            )

            logger.info("Ingestion completed successfully")

        # ------------------ TRANSFORMATION ------------------
        if ENABLE_TRANSFORMATION:
            logger.info("Starting transformation step")

            transform_file(
                input_csv=RAW_DATA_PATH,
                output_csv=CLEANED_DATA_PATH,
            )

            logger.info("Transformation completed successfully")

        # ------------------ DATABASE INSERTION ------------------
        if ENABLE_DATABASE_INSERTION:
            logger.info("Starting database insertion step")

            inserter = DataInsertion(db_path=DATABASE_PATH)
            inserter.insert_data(CLEANED_DATA_PATH)

            logger.info("Database insertion completed successfully")

        logger.info("Pipeline completed successfully")

    except Exception as e:
        logger.exception("Pipeline failed: %s", e)
        raise RuntimeError(f"Pipeline error: {e}")

if __name__ == "__main__":
    run_pipeline()
    print("Pipeline execution finished.")