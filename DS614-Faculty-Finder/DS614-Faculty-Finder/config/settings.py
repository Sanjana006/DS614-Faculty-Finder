import os
BASE_DIRECTORY=os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

RAW_DATA_PATH=os.path.join(BASE_DIRECTORY,"data","raw","Faculty_DAIICT.csv")
CLEANED_DATA_PATH=os.path.join(BASE_DIRECTORY,"data","cleaned","transformed_faculty_data.csv")
DATABASE_PATH=os.path.join(BASE_DIRECTORY,"data","database","faculty.db")

LOG_DIR=os.path.join(BASE_DIRECTORY,"logs")
PIPELINE_LOG_PATH=os.path.join(LOG_DIR,"pipeline.log")

ENABLE_SCRAPING=True
ENABLE_TRANSFORMATION=True
ENABLE_DATABASE_INSERTION=True