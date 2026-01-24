"""
this module handles the insertion of faculty data into the database from a CSV file.
it validates the data and uses parameterized queries to prevent SQL injection.
"""
import pandas as pd
from pathlib import Path
import logging

from storage.db_connection import SqlConnectionManager

logger= logging.getLogger(__name__)

REQUIRED_COLUMNS = ['faculty_id','name', 'mail', 'phd_field', 'specialization', 'bio', 'research', 'publications', 'combined_text']

class Data_insertion:
  
  def __init__(self,db_path:str):
    self.db=SqlConnectionManager(db_path)

  # loads csv and validates required columns
  def load_csv(self,csv_path:str)->pd.DataFrame:
    path=Path(csv_path)

    if not path.exists():
      raise FileNotFoundError(f"CSV file not found at {csv_path}")
    df=pd.read_csv(path)
    missing_columns_name=set(REQUIRED_COLUMNS) - set(df.columns.str.lower())
    if missing_columns_name:
      raise ValueError(f"Missing required columns in CSV:{', '.join(missing_columns_name)}")
    return df
  # this function inserts data from csv into the database
  def insert_data(self,csv_path:str):
    logger.info("starting dat inseertion")

    self.db.create_tables()
    df=self.load_csv(csv_path)
    insert_query="""
    INSERT INTO faculty(
    faculty_id,
    name,
    mail,
    phd_field,
    specialization,
    bio,
    research,
    publications,
    combined_text
    )values(?,?,?,?,?,?,?,?,?)"""

    conn=None
    try:
      conn=self.db.connection()
      cursor=conn.cursor()
      inserted_count=0
      for _,row in df.iterrows():
        try:
          cursor.execute(insert_query,(
            row['faculty_id'],
            row['name'],
            row['mail'],
            row['phd_field'],
            ",".join(row['specialization']) if isinstance(row['specialization'],list) else row['specialization'],
            row['bio'],
            row['research'],
            ",".join(row['publications']) if isinstance(row['publications'],list) else row['publications'],
            row['combined_text']
          ))
          inserted_count+=1
        except Exception as row_error:
          logger.warning("Failed to insert row %s: %s",row,row_error)

      conn.commit()
      logger.info(f"Sucessfully Inserted {inserted_count} records into the database")

    except Exception as e:
      if conn:
        conn.rollback()
      logger.exception("Data insertion failed:%s",e)
      raise RuntimeError(f"Data insertion error:{e}")
   
   
    finally:
      if conn:
        conn.close()