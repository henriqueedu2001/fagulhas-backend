import mysql.connector
from typing import *
from datetime import datetime
from collections.abc import Callable
from mysql.connector.cursor import MySQLCursor
from mysql.connector import MySQLConnection

DB_CONFIG = {
    'host': 'localhost',
    'user': 'admin',
    'password': 'admin123',
    'database': 'fagulhas',
    'port': '5467'
}

def main():
    """Runs the retrieval and storing routine with MySQL and external APIs.
    """
    log_message("Trying to connect to the MySQL Database...")
    try:
        with mysql.connector.connect(**DB_CONFIG) as conn:
            log_message('Connection with the MySQL Database was successful!')
            with conn.cursor() as cursor:
                create_work_table(cursor)
                create_edition_table(cursor)
                create_work_tags_table(cursor)
                create_auth_table(cursor)
                create_edition_files_table(cursor)
    except Exception as error:
        log_message(f'Error: {error}')
    finally:
        cursor.close()
        log_message('Connection closed')
    log_message('Application finished')
    return


def create_work_table(cursor: MySQLCursor):
    """Creates, if not exists, the table work

    Args:
        cursor (MySQLCursor): the MySQL cursor
    """
    create_my_texts_table_query = """
        CREATE TABLE IF NOT EXISTS work (
            work_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            date DATE NOT NULL
        );
    """
    try:
        log_message('Creating work table...')
        cursor.execute(create_my_texts_table_query)
        log_message('Table work created with success!')
    except Exception as error:
        log_message(f'Error: {error}')
    return


def create_edition_table(cursor: MySQLCursor):
    """Creates, if not exists, the table edition

    Args:
        cursor (MySQLCursor): the MySQL cursor
    """
    create_my_texts_table_query = """
        CREATE TABLE IF NOT EXISTS edition (
            edition_id INT AUTO_INCREMENT PRIMARY KEY,
            work_id INT,
            title VARCHAR(255) NOT NULL,
            date DATE NOT NULL,
            isbn VARCHAR(255) NULL,
            pages_num INT NOT NULL,
            views INT NOT NULL,
            likes INT NOT NULL,
            shares INT NOT NULL,
            FOREIGN KEY (work_id) REFERENCES work(work_id)
        );
    """
    try:
        log_message('Creating edition table...')
        cursor.execute(create_my_texts_table_query)
        log_message('Table edition created with success!')
    except Exception as error:
        log_message(f'Error: {error}')
    return


def create_work_tags_table(cursor: MySQLCursor):
    """Creates, if not exists, the table text_tags

    Args:
        cursor (MySQLCursor): the MySQL cursor
    """
    create_my_texts_table_query = """
        CREATE TABLE IF NOT EXISTS work_tags (
            work_id INT NOT NULL,
            tag_name VARCHAR(255) NULL,
            FOREIGN KEY (work_id) REFERENCES work(work_id)
        );
    """
    try:
        log_message('Creating work_tags table...')
        cursor.execute(create_my_texts_table_query)
        log_message('Table work_tags created with success!')
    except Exception as error:
        log_message(f'Error: {error}')
    return


def create_edition_files_table(cursor: MySQLCursor):
    """Creates, if not exists, the table text_tags

    Args:
        cursor (MySQLCursor): the MySQL cursor
    """
    create_edition_files_query = """
        CREATE TABLE IF NOT EXISTS edition_files (
            work_id INT NOT NULL,
            edition_id INT NOT NULL,
            filepath VARCHAR(255) NOT NULL,
            category ENUM('cover_img', 'raw_txt', 'json_text', 'pdf_text', 'audio_text') NOT NULL,
            FOREIGN KEY (work_id) REFERENCES work(work_id),
            FOREIGN KEY (edition_id) REFERENCES edition(edition_id)
        );
    """
    try:
        log_message('Creating editions_files table...')
        cursor.execute(create_edition_files_query)
        log_message('Table edition_files created with success!')
    except Exception as error:
        log_message(f'Error: {error}')
    return


def create_auth_table(cursor: MySQLCursor):
    """Creates, if not exists, the table text_tags

    Args:
        cursor (MySQLCursor): the MySQL cursor
    """
    create_my_texts_table_query = """
        CREATE TABLE IF NOT EXISTS auth (
            password_hash VARCHAR(255) NOT NULL,
            recover_email VARCHAR(255) NOT NULL
        );
    """
    try:
        log_message('Creating work_tags table...')
        cursor.execute(create_my_texts_table_query)
        log_message('Table work_tags created with success!')
    except Exception as error:
        log_message(f'Error: {error}')
    return


def drop_database(cursor: MySQLCursor):
    drop_table(cursor, 'edition_files')
    drop_table(cursor, 'work_tags')
    drop_table(cursor, 'edition')
    drop_table(cursor, 'work')
    drop_table(cursor, 'auth')


def drop_table(cursor: MySQLCursor, table_name: str):
    """Drops a specific table from the database.

    Args:
        cursor (MySQLCursor): the MySQL cursor
        table_name (str): the table name
    """
    drop_table = f'DROP TABLE {table_name};'
    cursor.execute(drop_table)
    return


def log_message(message: str):
    """Logs the message, by printing it with the current timestamp.

    Args:
        message (str): the log message
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")


if __name__ == "__main__":
    main()