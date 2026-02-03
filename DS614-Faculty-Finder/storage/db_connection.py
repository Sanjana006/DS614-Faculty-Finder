'''
Module for managing SQLite database connections and schema setup.
'''

import sqlite3
from pathlib import Path
import logging

logger=logging.getLogger(__name__)
FACULTY_TABLE_DDL="""
CREATE TABLE IF NOT EXISTS faculty(
faculty_id TEXT PRIMARY KEY,
name TEXT NOT NULL,
mail TEXT,
phd_field TEXT,
specialization TEXT,
bio TEXT,
research TEXT,
publications TEXT,
combined_text TEXT
)"""
class SqlConnectionManager:
  def __init__(self,db_path:str):
    self.db_path=Path(db_path)

  #"""creates the connection to the sqllite database"""
  def connection(self):
    try:

      conn=sqlite3.connect(self.db_path)
      conn.execute("PRAGMA foreign_keys=ON;")
      return conn
    
    except sqlite3.DatabaseError as e:
      
      logger.exception("Fail to connect to database at %s: %s",self.db_path,e)
      raise RuntimeError(f"Database connection error: {e}")
    
  def create_tables(self):
    conn=None
    try:
      conn=self.connection()
      conn.execute(FACULTY_TABLE_DDL)
      conn.commit()
      logger.info("Faculty table created or already exists.")
    except Exception as e:
      if conn:
        conn.rollback()
      logger.exception("Error creating tables: %s",e)
      raise RuntimeError(f"Table creation error: {e}")
    
    finally:
      if conn:
        conn.close()