import sqlite3
from pathlib import Path

class SQLLiteDB:
    def __init__(self):
        self.__db_path: str = "webnoveltoepub.db" # located at current dir
        self.__schema_path: str = "src/db/db.sql"
        self.__conn: sqlite3 = sqlite3.connect(self.__db_path)
        self.__conn.execute("PRAGMA foreign_keys = ON")
        # check db file
        if not Path(self.__db_path).is_file():
            self.__load_schema()

    # load schema if db file doesnt exists
    def __load_schema(self):
        if not Path(self.__schema_path).is_file():
            raise FileNotFoundError(f"Database file not found - '{self.__schema_path}'")
        with open(self.__schema, "r", encoding = "utf-8") as f:
            sql_script = f.read()
        self.__conn.executescript(sql_script)
        self.__conn.commit()
        print("[SQLite] Schema loaded successfully.")