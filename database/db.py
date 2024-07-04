import sqlite3
import os
from logger import logger


def create_database(db_name='image_hashes.db'):
    """
    Creates a SQLite database to store image hash data.

    Parameters:
    db_name (str): The name of the SQLite database file. Default is 'image_hashes.db'.

    Returns:
    None

    The function creates a table named 'image_data' with the following columns:
    - id (INTEGER PRIMARY KEY): Unique identifier for each image.
    - path (TEXT): The path of the image file.
    - a_hash (TEXT): The average hash of the image.
    - p_hash (TEXT): The perceptual hash of the image.
    - g_hash (TEXT): The global hash of the image.
    - d_hash (TEXT): The difference hash of the image.
    """
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
    """
    Deletes the SQLite database file.

    Parameters:
    db_name (str): The name of the SQLite database file. Default is 'image_hashes.db'.

    Returns:
    None

    This function checks if the database file exists. If it does, the file is deleted.
    If the database file does not exist, a warning message is logged.

    Note:
    This function does not return any additional code beyond its immediate scope.
    """
    logger.info("Deleting database")
    if os.path.exists(db_name):
        os.remove(db_name)
    else:
        logger.warning("Database does not exist.")


def add_image_data(path, a_hash=None, p_hash=None, g_hash=None, d_hash=None, db_name='image_hashes.db'):
    """
    Adds image data to the SQLite database.

    Parameters:
    path (str): The path of the image file.
    a_hash (str, optional): The average hash of the image. Default is None.
    p_hash (str, optional): The perceptual hash of the image. Default is None.
    g_hash (str, optional): The global hash of the image. Default is None.
    d_hash (str, optional): The difference hash of the image. Default is None.
    db_name (str, optional): The name of the SQLite database file. Default is 'image_hashes.db'.

    Returns:
    None

    This function connects to the SQLite database specified by `db_name`,
    creates a cursor, and inserts a new row into the 'image_data' table.
    The row contains the provided image data.
    After inserting the data, the changes are committed and the database connection is closed.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO image_data (path, a_hash, p_hash, g_hash, d_hash)
        VALUES (?, ?, ?, ?, ?)
    ''', (path, str(a_hash), str(p_hash), str(g_hash), str(d_hash)))
    conn.commit()
    conn.close()


def get_image_data(path, db_name='image_hashes.db'):
    """
    Retrieves image data from the SQLite database based on the provided path.

    Parameters:
    path (str): The path of the image file for which data needs to be retrieved.
    db_name (str, optional): The name of the SQLite database file. Default is 'image_hashes.db'.

    Returns:
    tuple: A tuple containing the data retrieved from the database.
           The tuple contains the following elements:
           - id (int): Unique identifier for the image.
           - path (str): The path of the image file.
           - a_hash (str): The average hash of the image.
           - p_hash (str): The perceptual hash of the image.
           - g_hash (str): The global hash of the image.
           - d_hash (str): The difference hash of the image.
           If no data is found for the provided path, the function returns None.

    This function connects to the SQLite database specified by `db_name`,
    creates a cursor, and executes a SELECT query to retrieve the data for the given path.
    The retrieved data is then returned as a tuple.
    After retrieving the data, the database connection is closed.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM image_data WHERE path = ?', (path,))
    data = cursor.fetchone()
    conn.close()
    return data


def clear_database(db_name='image_hashes.db'):
    """
    Clears all image data from the SQLite database.

    Parameters:
    db_name (str, optional): The name of the SQLite database file. Default is 'image_hashes.db'.

    Returns:
    None

    This function connects to the SQLite database specified by `db_name`,
    creates a cursor, and executes a DELETE query to remove all rows from the 'image_data' table.
    After clearing the data, the changes are committed and the database connection is closed.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM image_data')
    conn.commit()
    conn.close()
