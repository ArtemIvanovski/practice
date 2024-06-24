import sqlite3
import os
from logger import logger


def create_database(db_name='image_hashes.db'):
    logger.info("Creating database")
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS image_data (
            id INTEGER PRIMARY KEY,
            path TEXT,
            a_hash TEXT,
            p_hash TEXT,
            g_hash TEXT,
            d_hash TEXT
        )
    ''')
    conn.commit()
    conn.close()


def delete_database(db_name='image_hashes.db'):
    logger.info("Deleting database")
    if os.path.exists(db_name):
        os.remove(db_name)
    else:
        logger.warning("Database does not exist.")


def add_image_data(path, a_hash=None, p_hash=None, g_hash=None, d_hash=None, db_name='image_hashes.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO image_data (path, a_hash, p_hash, g_hash, d_hash)
        VALUES (?, ?, ?, ?, ?)
    ''', (path, str(a_hash), str(p_hash), str(g_hash), str(d_hash)))
    conn.commit()
    conn.close()


def get_image_data(image_id, db_name='image_hashes.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM image_data WHERE id=?', (image_id,))
    data = cursor.fetchone()
    conn.close()
    return data


def update_image_data(image_id, column, value, db_name='image_hashes.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f'UPDATE image_data SET {column}=? WHERE id=?', (value, image_id))
    conn.commit()
    conn.close()


def delete_image_data(image_id, db_name='image_hashes.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM image_data WHERE id=?', (image_id,))
    conn.commit()
    conn.close()


def clear_database(db_name='image_hashes.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM image_data')
    conn.commit()
    conn.close()
