import sqlite3

def setup_database():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS users")

    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        email TEXT
    )
    """)

    data = [
        (1, "Alice", 25, "alice@email.com"),
        (2, "Bob", None, "bobemail.com"),
        (3, None, 30, "charlie@email.com"),
        (4, "David", -5, "david@email.com"),
        (5, "Eve", 22, None),
    ]

    cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?)", data)

    conn.commit()
    conn.close()

    print("Database created with broken data.")

if __name__ == "__main__":
    setup_database()