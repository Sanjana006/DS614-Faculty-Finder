''' this is the main script to run the entire data pipeline
it includes scraping, transformation, and database insertion steps.'''
import logging
import sys
import uvicorn
import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Ensure the config directory is correctly structured and accessible
from config.settings import RAW_DATA_PATH, CLEANED_DATA_PATH, DATABASE_PATH, ENABLE_SCRAPING, ENABLE_TRANSFORMATION, ENABLE_DATABASE_INSERTION
from ingestion.run_scrapper import run_scraping_pipeline  
from transformation.transform_pipeline import transform_file
from storage.database_insertion import Data_insertion
from fastapi import FastAPI
from ingestion.daiict_faculty.spiders.daufaculty import DaiictFacultySpider
#this function runs the entire pipeline based on enabled steps
def run_pipeline():
    loger=logging.getLogger(__name__)
    loger.info("Pipeline started")
    try:
          if ENABLE_SCRAPING:
              loger.info("Starting scraping step")
              run_scraping_pipeline()
              loger.info("Scraping completed successfully")
    
          if ENABLE_TRANSFORMATION:
              loger.info("Starting transformation step")
              transform_file(
                 input_csv=RAW_DATA_PATH,
                 output_csv=CLEANED_DATA_PATH
               )
              loger.info("Transformation completed successfully")
    
          if ENABLE_DATABASE_INSERTION:
               loger.info("Starting database insertion step")
               seeder = Data_insertion(db_path=DATABASE_PATH)
               seeder.insert_data(CLEANED_DATA_PATH)
               loger.info("Database insertion completed successfully")
    
               loger.info("Pipeline completed successfully")
    
    except Exception as e:
         loger.exception("Pipeline failed: %s", e)
         raise RuntimeError(f"Pipeline error: {e}")
   
run_pipeline()
print("Pipeline execution finished.")


