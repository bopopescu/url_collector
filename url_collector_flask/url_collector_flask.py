from flask import Flask, render_template
import mysql.connector
import config

# create our little application :)
app = Flask(__name__)

@app.route('/')
def show_entries():
    cnx = mysql.connector.connect(**config.db_info)
    cursor = cnx.cursor()
    cursor.execute("SELECT * from urls")
    entries = cursor.fetchall()
    print entries
    cursor.close()
    return render_template('home.html', entries=entries)


if __name__ == "__main__":
    app.run()
