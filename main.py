from flask import Flask
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)


def getConnection():
    try:
        conn = mysql.connector.connect(
            host="mysql-server-test.mysql.database.azure.com",
            user="sonpal",
            password="Sonpal@12345",
            port=3306,
            database="orders")
        print("Connection established")
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        raise RuntimeError("MySQL connection not working")


def insertedRecords():
    conn = getConnection()
    cursor = conn.cursor()

    # Drop previous table of same name if one exists
    cursor.execute("DROP TABLE IF EXISTS ITEMS;")
    print("Finished dropping table (if existed).")

    # Created table
    cursor.execute(
        "CREATE TABLE ITEMS (id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER);"
    )
    print("Finished creating table.")

    # Inserted data into table
    cursor.execute(
        "INSERT INTO ITEMS (name, quantity) VALUES (%s, %s);", ("banana", 150)
    )
    print("Inserted", cursor.rowcount, "row(s) of data.")
    cursor.execute(
        "INSERT INTO ITEMS (name, quantity) VALUES (%s, %s);", ("orange", 154)
    )
    print("Inserted", cursor.rowcount, "row(s) of data.")

    return cursor.rowcount


@app.route("/savedRecords")
def insertedRecords():
    savedRecordsCount = savedRecordsCount()
    return "items saved " + savedRecordsCount


@app.route("/fetchAllRecords")
def fetchAllRecords():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ITEMS")
    return cursor.fetchall()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
