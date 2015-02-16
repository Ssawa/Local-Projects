import psycopg2 # Handles our postgres connection
import os
import urlparse

def getDbConnection():
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    return psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port)


def getTokens():
    tokens = None
    with getDbConnection() as conn:
        with conn.cursor() as curs:
            SQL = "SELECT * FROM TOKENS;"
            curs.execute(SQL)
            tokens = curs.fetchall()
    return tokens
