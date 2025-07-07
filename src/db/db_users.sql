CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    username TEXT,
    mail TEXT,
    pass TEXT --hashed through python lib
);

CREATE TABLE IF NOT EXISTS webnovel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    title TEXT NOT NULL,
    author TEXT,
    summary TEXT,
    image BLOB,
    epub BLOB,
    update_date DATE
);



CREATE TABLE IF NOT EXISTS library (
    id INTEGER
);