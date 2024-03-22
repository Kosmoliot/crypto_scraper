import pyodbc, os
from dotenv import load_dotenv


load_dotenv()
connection_string = os.environ["AZURE_SQL_CONNECTIONSTRING"]

with pyodbc.connect(connection_string) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT TOP 3 name, collation_name FROM sys.databases")
        row = cursor.fetchone()
        while row:
            print (str(row[0]) + " " + str(row[1]))
            row = cursor.fetchone()