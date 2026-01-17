# scripts/run_pipeline.py

import logging
from pathlib import Path
import sys
from storage.database_insertion import Data_insertion 

# -----------------------------
# LOGGING CONFIG
# -----------------------------
logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)



# -----------------------------
# PIPELINE
# -----------------------------
def run_pipeline():
    """
    End-to-end faculty finder pipeline:
    Raw CSV -> Transform -> Cleaned CSV -> SQLite DB
    """
    print("Pipeline started")

    try:
        # -----------------------------
        # 1. Validate input paths
        # # -----------------------------
        # raw_path = Path(RAW_DATA_PATH)
        # if not raw_path.exists():
        #     raise FileNotFoundError(f"Raw data not found: {raw_path}")

        # Path(CLEANED_DATA_PATH).parent.mkdir(parents=True, exist_ok=True)
        Path("data/database/faculty.db").parent.mkdir(parents=True, exist_ok=True)

        # # -----------------------------
        # # 2. Transformation step
        # # -----------------------------
        # print("Running transformation pipeline")

        # run_transformation_pipeline(
        #     input_csv=RAW_DATA_PATH,
        #     output_csv=CLEANED_DATA_PATH
        # )

        # print("Transformation completed successfully")

        # -----------------------------
        # 3. Load into SQLite
        # -----------------------------
        print("inserting to the database from cleaned data")

        seeder = Data_insertion(db_path="data/database/faculty.db")
        seeder.insert_data("data/cleaned/dau_faculty_final.csv")

        print("Database seeding completed successfully")

    except Exception as e:
        print("Pipeline failed",e)
        sys.exit(1)

    print("Pipeline finished successfully")

run_pipeline()
