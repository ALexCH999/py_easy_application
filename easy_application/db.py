import sqlite3

def create_db(con):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS reg_users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        lname VARCHAR(20),
                        fname VARCHAR(20),
                        email VARCHAR(50) UNIQUE,
                        password VARCHAR(256));
    """)
    conn.commit()
    conn.close()

def insert(con, lname, fname, email, password):
    cur = con.cursor()
    cur.execute("""INSERT INTO reg_users (lname, fname, email, password) VALUES (?, ?, ?, ?)""", (lname, fname, email, password))
    con.commit()

def select(con, email, password):
    cur = con.cursor()
    cur.execute("""SELECT * FROM reg_users WHERE email=? AND password=?""", (email, password))
    return cur.fetchone()

def find_user_email(con, email):
    cur = con.cursor()
    cur.execute("""SELECT * FROM reg_users WHERE email=?""", (email,))
    return cur.fetchone()