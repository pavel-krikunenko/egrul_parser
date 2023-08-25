import os
import sqlite3
import zipfile
import json
from db import write_company, get_connection, migrate

def main():
    migrate()
    f = get_file("egrul.json.zip")
    conn = get_connection("companies.db")
    for i in f.namelist():
        print(f"Parse file {i}")
        parse_file(f,conn, i)

def parse_file(archive: zipfile.ZipFile, db_conn: sqlite3.Connection, filename: str):
    with archive.open(filename) as jsonfile:
            for j in json.loads(jsonfile.read()):
                get_needs(db_conn,j, filename=filename)
            

def get_needs(db_conn: sqlite3.Connection,item: dict, filename: str):
    if filter_by_okved("62", get_okved(item)) and get_city(item).lower() == "хабаровск":   
        print(f"FOUND!!!!!!!!! filename: {filename}, item_name: {item.get('name')}")
        
        
        write_company(
            db_conn, 
            name=item.get('name'),
            inn=item.get("data").get("ИНН"),
            kpp=item.get("data").get("КПП"),
            okved=get_code_okved(get_okved(item)),
            city=get_city(item)
        )

def get_file(filepath: str = os.getenv("ZIP_FILE_NAME")):
    return zipfile.ZipFile(filepath, "r")

def get_city(item: dict) -> str:
    return item.get('data').get("СвАдресЮЛ").get("АдресРФ", {}).get("Город", {}).get("НаимГород", "")
    
def get_okved(item: dict) -> list[dict] | dict:
    return item.get("data").get("СвОКВЭД", {}).get("СвОКВЭДДоп", [])

def filter_by_okved(need_code: str, current_data: list[dict]| dict) -> bool:
    if isinstance(current_data, list):
        return any([need_code in item.get("КодОКВЭД") for item in current_data])
    return need_code in current_data.get("КодОКВЭД")

def get_code_okved(current_data: list[dict]| dict) -> bool:
    if isinstance(current_data, list):
        return [item.get("КодОКВЭД") for item in current_data]
    return current_data.get("КодОКВЭД")


if __name__ == "__main__":
    main()
        
