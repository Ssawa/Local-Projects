from config import getConfig
import psycopg2 # Handles our postgres connection

def getDbConnection():
    return psycopg2.connect(
        database=getConfig().get('Database', 'Database'),
        user=getConfig().get('Database', 'User'),
        password=getConfig().get('Database', 'Password'),
        host=getConfig().get('Database', 'Host'),
        port=getConfig().get('Database', 'Port'))

def getTokens():
    tokens = None
    with getDbConnection() as conn:
        with conn.cursor() as curs:
            SQL = "SELECT * FROM TOKENS;"
            curs.execute(SQL)
            tokens = curs.fetchall()
    return tokens
