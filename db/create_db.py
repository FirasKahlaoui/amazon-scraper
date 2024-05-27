import sqlite3

def create_db():
    conn = sqlite3.connect('db/amazon_prices.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            url TEXT NOT NULL,
            price REAL NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_db()
