from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import time


app = Flask(__name__)

# MySQL Config
app.config['MYSQL_HOST'] = 'mysql-service'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'testdb'

mysql = MySQL(app)

def wait_for_db():
    for i in range(10):
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT 1")
            cur.close()
            print("MySQL is ready")
            return
        except Exception as e:
            print(f"Waiting for DB... {e}")
            time.sleep(3)

    raise Exception("DB not ready")

# Create table
def create_table():
    print("creating table--------------------------------------------------")
    print("creating table--------------------------------------------------")
    print("creating table--------------------------------------------------")
    print("creating table--------------------------------------------------")
    cur = mysql.connection.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100),
            password VARCHAR(100)
        )
    """)
    mysql.connection.commit()
    cur.close()

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/add', methods=['POST'])
def add_user():
    username = request.form['username']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users(username, password) VALUES(%s, %s)", (username, password))
    mysql.connection.commit()
    cur.close()

    return "User added successfully!"

if __name__ == '__main__':
    with app.app_context():
        wait_for_db()
        create_table()   # CALL HERE instead of decorator

    app.run(host="0.0.0.0", port=5000, debug=True)
