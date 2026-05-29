import mysql.connector
from mysql.connector import MySQLConnection

DB_CONFIG = {
    'host': 'localhost',
    'user': 'admin',
    'password': 'admin123',
    'database': 'fagulhas',
    'port': '5467'
}

def create_connection() -> MySQLConnection:
    return mysql.connector.connect(**DB_CONFIG)