import sqlite3
from pathlib import Path

class SQLLiteDB:
    def __init__(self):
        self.__db_path: str = "webnoveltoepub.db" # located at current dir
        self.__schema: str = "src/db/db.sql"
        self.__conn: sqlite3 = sqlite3.connect(self.__db_path)
        self.__conn.execute("PRAGMA foreign_keys = ON")
    
    # load sql; if tables can't be found -> CREATE
    def __load_schema(self):
        if not Path(self.__schema).is_file():
            raise FileNotFoundError(f"Database file not found - '{self.__schema}'")
        with open(self.__schema, "r", encoding = "utf-8") as f:
            sql_script = f.read()
        self.__conn.executescript(sql_script)
        self.__conn.commit()
        print("[SQLiteDB] Schema loaded successfully.")

s = SQLLiteDB()