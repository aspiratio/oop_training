CREATE TABLE IF NOT EXISTS books (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    genre TEXT NOT NULL,
    is_checked_out INTEGER
)