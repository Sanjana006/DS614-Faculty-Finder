"""
This module handles the insertion of faculty data into the SQLite database
from a cleaned CSV file. It validates the input data and uses parameterized
queries to ensure safe and reliable insertion.
"""

import sys
import os
import logging
import pandas as pd
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from storage.db_connection import SqlConnectionManager
from config.settings import DATABASE_PATH, CLEANED_DATA_PATH

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = [
    "faculty_id",
    "name",
    "mail",
    "phd_field",
    "specialization",
    "bio",
    "research",
    "publications",
    "combined_text"
]

class DataInsertion:
    def __init__(self, db_path: str):
        self.db = SqlConnectionManager(db_path)

    # Load CSV and validate required columns
    def load_csv(self, csv_path: str) -> pd.DataFrame:
        path = Path(csv_path)

        if not path.exists():
            raise FileNotFoundError(f"CSV file not found at {csv_path}")

        df = pd.read_csv(path)

        missing_columns = set(REQUIRED_COLUMNS) - set(df.columns.str.lower())
        if missing_columns:
            raise ValueError(
                f"Missing required columns in CSV: {', '.join(missing_columns)}"
            )

        return df

    # Insert data into database
    def insert_data(self, csv_path: str) -> None:
        logger.info("Starting database insertion")

        self.db.create_tables()
        df = self.load_csv(csv_path)

        insert_query = """
        INSERT INTO faculty (
            faculty_id,
            name,
            mail,
            phd_field,
            specialization,
            bio,
            research,
            publications,
            combined_text
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        conn = None
        try:
            conn = self.db.connection()
            cursor = conn.cursor()
            inserted_count = 0

            for _, row in df.iterrows():
                try:
                    cursor.execute(
                        insert_query,
                        (
                            row["faculty_id"],
                            row["name"],
                            row["mail"],
                            row["phd_field"],
                            ",".join(row["specialization"])
                            if isinstance(row["specialization"], list)
                            else row["specialization"],
                            row["bio"],
                            row["research"],
                            ",".join(row["publications"])
                            if isinstance(row["publications"], list)
                            else row["publications"],
                            row["combined_text"],
                        ),
                    )
                    inserted_count += 1
                except Exception as row_error:
                    logger.warning(
                        "Failed to insert row with faculty_id %s: %s",
                        row.get("faculty_id"),
                        row_error,
                    )

            conn.commit()
            logger.info(
                "Successfully inserted %d records into the database",
                inserted_count,
            )

        except Exception as e:
            if conn:
                conn.rollback()
            logger.exception("Data insertion failed: %s", e)
            raise RuntimeError(f"Data insertion error: {e}")

        finally:
            if conn:
                conn.close()

if __name__ == "__main__":
    inserter = DataInsertion(db_path=DATABASE_PATH)
    inserter.insert_data(CLEANED_DATA_PATH)
    print("Database insertion completed successfully.")
