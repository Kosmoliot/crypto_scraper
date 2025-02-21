import os
import pyodbc
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from transcript import fetch_video_data
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
connection_string = os.getenv("AZURE_SQL_CONNECTIONSTRING")
if not connection_string:
    raise ValueError("AZURE_SQL_CONNECTIONSTRING environment variable is not set.")

app = FastAPI()

# Database connection management
def get_conn():
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except pyodbc.Error as e:
        logger.error(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")

# API Endpoints

@app.get("/coins")
def get_coins():
    try:
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Coins")
            rows = cursor.fetchall()
            return [
                {"video_id": row.Video_Id, "published_date": row.Published_Date, "title": row.Title, "coins": row.Coins}
                for row in rows
            ]
    except pyodbc.Error as e:
        logger.error(f"Error fetching coins: {e}")
        raise HTTPException(status_code=500, detail="Error fetching coins")

@app.get("/coins/{id}")
def get_coins_by_id(id: int):
    try:
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Coins WHERE ID = ?", id)
            row = cursor.fetchone()
            if row:
                return {"video_id": row.Video_Id, "published_date": row.Published_Date, "title": row.Title, "coins": row.Coins}
            else:
                raise HTTPException(status_code=404, detail="Coin not found")
    except pyodbc.Error as e:
        logger.error(f"Error fetching coin by ID: {e}")
        raise HTTPException(status_code=500, detail="Error fetching coin by ID")

@app.post("/create_table")
def create_table():
    try:
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE Coins (
                    ID int NOT NULL PRIMARY KEY IDENTITY,
                    Video_Id varchar(255),
                    Published_Date varchar(255),
                    Title varchar(255),
                    Coins NVARCHAR(MAX)
                );
            """)
            conn.commit()
        return {"message": "Coins table created in the database"}
    except pyodbc.Error as e:
        logger.error(f"Error creating table: {e}")
        raise HTTPException(status_code=500, detail="Error creating table")
    except Exception as e:
        logger.error(f"Table may already exist: {e}")
        raise HTTPException(status_code=400, detail="Table may already exist")

@app.post("/delete_table")
def delete_table():
    try:
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE Coins;")
            conn.commit()
        return {"message": "Coins table deleted from the database"}
    except pyodbc.Error as e:
        logger.error(f"Error deleting table: {e}")
        raise HTTPException(status_code=500, detail="Error deleting table")
    except Exception as e:
        logger.error(f"Table may not exist: {e}")
        raise HTTPException(status_code=400, detail="Table may not exist")
    
