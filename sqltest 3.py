import pyodbc
server = 'scrappersqlserver.database.windows.net'
database = 'scrapperdatabase'
username = 'scrapper'
password = 'e4syp4ssword5!'
driver= '{ODBC Driver 18 for SQL Server}'

with pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=tcp:scrappersqlserver.database.windows.net;PORT=1433;DATABASE=scrapperdatabase;UID=scrapper;PWD=e4syp4ssword5!') as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT TOP 3 name, collation_name FROM sys.databases")
        row = cursor.fetchone()
        while row:
            print (str(row[0]) + " " + str(row[1]))
            row = cursor.fetchone()