import sqlite3

db = sqlite3.connect('test.db')
cur = db.cursor()

cur.execute(
    """CREATE TABLE answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    upper TEXT,
    lower TEXT,
    whatisbefore TEXT,
    whatisafter TEXT ) 
    """)

cur.execute(
    """CREATE TABLE person ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gender TEXT,
    age INTEGER,
    education TEXT )
    """)

db.commit()
