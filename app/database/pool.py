from mysql.connector.pooling import MySQLConnectionPool

POOL = MySQLConnectionPool(
    pool_name='fastapi_pool',
    pool_size=10,
    pool_reset_session=True,

    host='localhost',
    port=5467,
    user='admin',
    password='admin123',
    database='fagulhas'
)