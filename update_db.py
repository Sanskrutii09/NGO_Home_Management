import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS our_story (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS core_values (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS programs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS team_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    designation TEXT,
    image TEXT
)
""")

conn.commit()
conn.close()

print("Database updated successfully!")