'''
Module defining API routes for faculty data retrieval.
'''

import sqlite3
from fastapi import APIRouter, HTTPException,Query
from typing import List, Optional
from storage.db_connection import SqlConnectionManager
from config.settings import DATABASE_PATH

router =APIRouter()

DB_PATH=DATABASE_PATH

@router.get("/faculty")# to get all faculty records
def get_all_faculty_details():
  db=SqlConnectionManager(DB_PATH)
  conn=None
  try:
    conn=db.connection()
    cursor=conn.cursor()
    cursor.execute(
      """SELECT
                faculty_id,
                name,
                mail,
                phd_field,
                specialization,
                bio,
                research,
                publications
         FROM faculty
            """
    )
    output_resultset=cursor.fetchall()
    results=[
      {
        "faculty_id":row[0],
        "name":row[1],
        "mail":row[2],
        "phd_field":row[3],
        "specialization":row[4],
        "bio":row[5],
        "research":row[6],
        "publications":row[7]
      }for row in output_resultset
    ]
    return {
      "count":len(results),
      "results":results
    }
  except Exception as e:
    raise HTTPException(status_code=500,detail=str(e))
  finally:
    if conn:
      conn.close()

@router.get("/faculty/{faculty_id}")## to get by faculty id
def get_faculty_by_id(faculty_id:str):
  db=SqlConnectionManager(DB_PATH)
  conn=None
  try:
    conn=db.connection()
    cursor=conn.cursor()
    cursor.execute(
      """SELECT
                faculty_id,
                name,
                mail,
                phd_field,
                specialization,
                bio,
                research,
                publications
         FROM faculty
         WHERE faculty_id = ?
            """,(faculty_id,)
    )
    output_resultset=cursor.fetchone()
    if not output_resultset:
      raise HTTPException(status_code=404,detail="Faculty not found")

    return {
        "faculty_id":output_resultset[0],
        "name":output_resultset[1],
        "mail":output_resultset[2],
        "phd_field":output_resultset[3],
        "specialization":output_resultset[4],
        "bio":output_resultset[5],
        "research":output_resultset[6],
        "publications":output_resultset[7]
      }
  except HTTPException:
    raise
  except Exception as e:
    raise HTTPException(status_code=500,detail=str(e))
  finally:
    if conn:
      conn.close()
