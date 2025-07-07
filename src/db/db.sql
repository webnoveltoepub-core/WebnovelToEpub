CREATE TABLE IF NOT EXISTS config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain TEXT NOT NULL, -- needs to be the same as requested
    config BLOB NOT NULL, -- complex JSON stored as BLOB
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);

CREATE TABLE IF NOT EXISTS webnovel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    config_id INTEGER,
    url TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    author TEXT,
    summary TEXT,
    image BLOB, -- binary file
    epub BLOB,  -- epub file
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    FOREIGN KEY (config_id) REFERENCES config(id) ON DELETE SET NULL
);