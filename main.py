from flask import Flask 
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'test'

mysql = MySQL(app)


@app.route("/savedRecords")
def insertedRecords():
    conn = mysql.connection
    cursor = conn.cursor()

    # Drop previous table of same name if one exists
    cursor.execute("DROP TABLE IF EXISTS items;")
    print("Finished dropping table (if existed).")

    # Created table
    cursor.execute("CREATE TABLE items (id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER);")
    print("Finished creating table.")

    # Inserted data into table
    cursor.execute("INSERT INTO items (name, quantity) VALUES (%s, %s);", ("banana", 60))
    cursor.execute("INSERT INTO items (name, quantity) VALUES (%s, %s);", ("apple", 160))
    cursor.execute("INSERT INTO items (name, quantity) VALUES (%s, %s);", ("mango", 120))
    conn.commit()
    #savedRecordsCount = cursor.rowcount
    return "items saved "



@app.route("/fetchAllRecords")
def fetchAllRecords():
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    return str(cursor.fetchall())


if __name__ == "__main__":
   app.run(host="localhost", port=8080)
