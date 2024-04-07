import os
import pyodbc, struct
from transcript import get_video_data
from typing import Union

# FastAPI web framework for building APIs with Python. Uses Swagger UI to generate 
# interactive API documentation that lets your users try out the API calls directly 
# in the browser
from fastapi import FastAPI

#FastAPI uses Pydantic models for request and response validation. It automatically 
# validates request data against the defined data models and raises validation errors
# if data doesn't match the expected schema
from pydantic import BaseModel

# Uses load_dotenv to load a connection string from .env file
from dotenv import load_dotenv


load_dotenv()
connection_string = os.environ["AZURE_SQL_CONNECTIONSTRING"]

app = FastAPI()

@app.get("/")
def root():
    print("Root of Coins API")
    try:
        conn = get_conn()
        cursor = conn.cursor()

        # Table should be created ahead of time in production app.
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
    except Exception as e:
        # Table may already exist
        print(e)
    return "Coins API"

# Print all the videos and their data
@app.get("/all")
def get_coins():
    rows = []
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Coins")

        for row in cursor.fetchall():
            print(row.Title, row.Published_Date)
            rows.append(f"{row.Video_Id}, {row.Published_Date}, {row.Title}, {row.Coins}")
    return rows

# Fetch the video data by table ID
@app.get("/Coins/{ID}")
def get_person(ID: int):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Coins WHERE ID = ?", ID)

        row = cursor.fetchone()
        return f"{row.Video_Id}, {row.Published_Date}, {row.Coins}"

# Delete Coins table from the database
@app.get("/Delete table")
def delete_table():
    try:
        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            DROP TABLE Coins;
        """)

        conn.commit()
    except Exception as e:
        # Table doesn't exist
        print(e)
    return "Coins Table deleted from the database"

# Ingesting data into Azure database that was generated by "tanscript" module
@app.post("/Ingest data")
def ingest_data():
    # Retrieve video IDs and other data
    videos = get_video_data()

    try:
        # Establish connection to Azure SQL Database
        conn = get_conn()
        cursor = conn.cursor()

        # Loop through the list of class objects and insert data into the database
        for video in videos:
            cursor.execute(
                "INSERT INTO Coins (Video_Id, Published_Date, Title, Coins) VALUES (?, ?, ?, ?)",
                video['video_id'], video['video_date'], video['video_title'], video['video_coins']
            )

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return {"message": "Data successfully ingested into Azure SQL Database."}

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}


def get_conn():
    conn = pyodbc.connect(connection_string)
    return conn
