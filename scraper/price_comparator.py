import sqlite3
from datetime import datetime, timedelta


def compare_prices():
    conn = sqlite3.connect('C:/Users/Kahla/OneDrive/Documents/amazon_scraper_project/db/amazon_prices.db')
    cursor = conn.cursor()

    today = str(datetime.now().date())
    yesterday = str((datetime.now() - timedelta(days=1)).date())

    query = '''
        SELECT p1.name, p1.category, p1.price AS today_price, p2.price AS yesterday_price
        FROM products p1
        JOIN products p2 ON p1.name = p2.name AND p1.category = p2.category
        WHERE p1.created_at = ? AND p2.created_at = ?
    '''

    cursor.execute(query, (today, yesterday))
    rows = cursor.fetchall()

    changes = []
    for row in rows:
        if row[2] != row[3]:
            changes.append({
                'name': row[0],
                'category': row[1],
                'today_price': row[2],
                'yesterday_price': row[3]
            })

    conn.close()
    return changes

def print_duplicate_products():
    conn = sqlite3.connect('C:/Users/Kahla/OneDrive/Documents/amazon_scraper_project/db/amazon_prices.db')
    cursor = conn.cursor()

    query = '''
        SELECT name, COUNT(*)
        FROM products
        GROUP BY name
        HAVING COUNT(*) > 1
    '''

    cursor.execute(query)
    rows = cursor.fetchall()

    for row in rows:
        print(f"Product: {row[0]} - Occurrences: {row[1]}")

    conn.close()


if __name__ == '__main__':
    print(compare_prices())
    print_duplicate_products()
