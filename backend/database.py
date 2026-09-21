import sqlite3
import json
import os
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "products.db")

def get_db_connection():
    """Establishes and returns a SQLite database connection with row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database table and populates initial seed products if empty."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT NOT NULL,
            features TEXT NOT NULL,
            availability TEXT NOT NULL,
            stock_quantity INTEGER NOT NULL DEFAULT 0,
            discount_percentage REAL NOT NULL DEFAULT 0.0
        )
    """)
    conn.commit()

    # Seed initial products if table is empty
    cursor.execute("SELECT COUNT(*) as count FROM products")
    row = cursor.fetchone()
    if row and row["count"] == 0:
        from seed_data import SAMPLE_PRODUCTS
        for prod in SAMPLE_PRODUCTS:
            cursor.execute("""
                INSERT INTO products (id, name, category, price, description, features, availability, stock_quantity, discount_percentage)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                prod["id"],
                prod["name"],
                prod["category"],
                prod["price"],
                prod["description"],
                prod["features"],
                prod["availability"],
                prod["stock_quantity"],
                prod["discount_percentage"]
            ))
        conn.commit()
    
    conn.close()

def parse_product_row(row: sqlite3.Row) -> Dict[str, Any]:
    """Converts SQLite Row to a dictionary and parses features JSON string into list."""
    if not row:
        return None
    d = dict(row)
    try:
        d["features"] = json.loads(d["features"])
    except Exception:
        d["features"] = [d["features"]]
    
    # Calculate discounted price
    discount = d.get("discount_percentage", 0.0)
    d["discounted_price"] = round(d["price"] * (1 - discount / 100.0), 2)
    d["is_in_stock"] = d["stock_quantity"] > 0 and d["availability"].lower() != "out of stock"
    return d

def search_products_db(
    query: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock_only: bool = False
) -> List[Dict[str, Any]]:
    """Searches products based on keyword, category, price range, and availability."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    sql = "SELECT * FROM products WHERE 1=1"
    params = []

    if query:
        q_wildcard = f"%{query.strip()}%"
        sql += " AND (name LIKE ? OR description LIKE ? OR category LIKE ? OR features LIKE ?)"
        params.extend([q_wildcard, q_wildcard, q_wildcard, q_wildcard])
        
    if category:
        sql += " AND category LIKE ?"
        params.append(f"%{category.strip()}%")

    if min_price is not None:
        sql += " AND price >= ?"
        params.append(min_price)

    if max_price is not None:
        sql += " AND price <= ?"
        params.append(max_price)

    if in_stock_only:
        sql += " AND stock_quantity > 0 AND LOWER(availability) != 'out of stock'"

    sql += " ORDER BY id ASC"

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()

    return [parse_product_row(r) for r in rows]

def get_product_by_id_db(product_id: int) -> Optional[Dict[str, Any]]:
    """Retrieves a single product by its primary key ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    conn.close()
    return parse_product_row(row)

def get_product_by_name_db(name: str) -> Optional[Dict[str, Any]]:
    """Finds the best matching product by name or keyword."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Exact match first
    cursor.execute("SELECT * FROM products WHERE LOWER(name) = LOWER(?)", (name.strip(),))
    row = cursor.fetchone()
    
    # Partial match if exact match fails
    if not row:
        cursor.execute("SELECT * FROM products WHERE LOWER(name) LIKE LOWER(?) OR LOWER(category) LIKE LOWER(?)", (f"%{name.strip()}%", f"%{name.strip()}%"))
        row = cursor.fetchone()
        
    conn.close()
    return parse_product_row(row)

def get_categories_db() -> List[str]:
    """Returns a list of distinct product categories."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM products ORDER BY category ASC")
    rows = cursor.fetchall()
    conn.close()
    return [r["category"] for r in rows]
