import psycopg2 # Handles our postgres connection
import os
import urlparse

def getDbConnection():
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.getenv("DATABASE_URL"))
    return psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port)


def readTokens():
    tokens = None
    with getDbConnection() as conn:
        with conn.cursor() as curs:
            SQL = """SELECT * FROM TOKENS;"""
            curs.execute(SQL)
            tokens = curs.fetchall()
    return tokens

def readQuestions():
    questions = None
    with getDbConnection() as conn:
        with conn.cursor() as curs:
            SQL = """SELECT * FROM QUESTIONS;"""
            curs.execute(SQL)
            questions = curs.fetchall()
    return questions

def getQuestion(questionId):
    question = None
    tokens = None
    with getDbConnection() as conn:
        with conn.cursor() as curs:
            SQL = """SELECT QUESTION FROM QUESTIONS WHERE ID=%s"""
            curs.execute(SQL, questionId)
            question = curs.fetchone()

            # This is a bit of an ugly query and we should consider seeing if it can be refactored
            SQL = """SELECT TOKEN, COALESCE(YES_VALUE, 0), COALESCE(NO_VALUE,0) FROM TOKENS tk 
            LEFT JOIN TOKEN_QUESTION_MAP tq ON tk.ID = tq.TOKEN_ID 
            WHERE QUESTION_ID = %s OR QUESTION_ID IS NULL;"""
            curs.execute(SQL, questionId)
            tokens = curs.fetchall()
    return [question, tokens]

def createToken(name):
    with getDbConnection() as conn:
        with conn.cursor() as curs:
            SQL = """INSERT INTO TOKENS (TOKEN) VALUES (%s);"""
            curs.execute(SQL, [name])
            conn.commit

def deleteTokens(tokenIds):
    with getDbConnection() as conn:
        with conn.cursor() as curs:

            # Alternativly, instead of constructing the SQL delete string with a 
            # for loop we could have used psycopg2's "executemany" function
            # however this would have required reformatting our tokenIds list
            # and would have just done multiple deletes as oppossed to just one
            # with proper WHERE clauses

            SQL = """DELETE FROM TOKENS WHERE"""
            for tIds in tokenIds:
                if tokenIds.index(tIds) != 0:
                    SQL += " OR"
                SQL += " ID = %s"
            SQL += ';'

            curs.execute(SQL, tokenIds)
            conn.commit
