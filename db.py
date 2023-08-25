import sqlite3
import os

COMPANY_TABLE = "companies"

def get_connection(dbname: str):
    return sqlite3.connect(dbname)


def migrate():
    if os.path.exists(".lockfile"):
        print("LOCKFILE found, migrations will not be applied")
        return
    conn = get_connection(dbname="companies.db")

    cur = conn.cursor()

    cur.execute(f"CREATE TABLE {COMPANY_TABLE}(name, okved, inn, kpp, city)")
    file = open(".lockfile", "w")
    file.write("")
    file.close

def write_company(
        conn: sqlite3.Connection, 
        name: str, 
        okved: str, 
        inn: str, 
        kpp: str, 
        city: str
):
    cur = conn.cursor()
    cur.execute(f"INSERT INTO {COMPANY_TABLE} VALUES (?,?,?,?,?)", (name,str(okved),inn, kpp, city))
    conn.commit()