import sqlite3
from pprint import pprint

if __name__ == "__main__":
    conn = sqlite3.connect("./companies.db")
    for i in conn.cursor().execute("SELECT * FROM companies").fetchall():
        pprint(i)