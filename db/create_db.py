import sqlite3


def create_db():
    conn = sqlite3.connect('db/amazon_prices.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            url TEXT,
            price REAL,
            created_at TEXT 
        )
    ''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_db()
