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

            SQL = """SELECT tk.ID, TOKEN, YES_VALUE, NO_VALUE FROM TOKENS tk 
            JOIN TOKEN_QUESTION_MAP tq ON tk.ID = tq.TOKEN_ID 
            WHERE QUESTION_ID = %s;"""
            curs.execute(SQL, questionId)
            tokens = curs.fetchall()
    return [question, tokens]

# Note that there are stored procedures and trigger within the database to make sure that
# TOKEN_QUESTION_MAP stays up to date whenever an INSERT happens in TOKENS.
#
# Here is an example of the stored procedure that gets triggered after TOKENS inserts:

##CREATE OR REPLACE FUNCTION add_new_token()
##RETURNS trigger AS $BODY$
##DECLARE
##    question record;
##BEGIN
##    FOR question in SELECT * FROM QUESTIONS
##    LOOP
##        INSERT INTO TOKEN_QUESTION_MAP (QUESTION_ID, TOKEN_ID, YES_VALUE, NO_VALUE) VALUES (question.ID, NEW.ID, 0, 0);
##    END LOOP;
##    RETURN NEW;
##END;
##$BODY$
##LANGUAGE 'plpgsql';

def createToken(token):
    with getDbConnection() as conn:
        with conn.cursor() as curs:
            SQL = """INSERT INTO TOKENS (TOKEN) VALUES (%s);"""
            curs.execute(SQL, [token])
            conn.commit

def createQuestion(question, yesList, noList, tokenIds):
    with getDbConnection() as conn:
        with conn.cursor() as curs:
            SQL = """INSERT INTO QUESTIONS (QUESTION) VALUES (%s);"""
            curs.execute(SQL, [question])

            SQL = """SELECT currval('questions_id_seq');"""
            curs.execute(SQL)
            questionId = curs.fetchone()

            for i in range(len(yesList)):
                SQL = """INSERT INTO TOKEN_QUESTION_MAP (QUESTION_ID, TOKEN_ID, YES_VALUE, NO_VALUE)
                        VALUES (%s, %s, %s, %s)"""
                curs.execute(SQL, [questionId, tokenIds[i], yesList[i], noList[i]])
            conn.commit

def updateQuestion(questionId, yesList, noList, tokenIds):
    with getDbConnection() as conn:
        with conn.cursor() as curs:
            for i in range(len(yesList)):
                SQL = """UPDATE TOKEN_QUESTION_MAP SET YES_VALUE=%s, NO_VALUE=%s WHERE QUESTION_ID = %s AND TOKEN_ID = %s"""
                curs.execute(SQL, [yesList[i], noList[i], questionId, tokenIds[i]])
            conn.commit


def deleteTokens(tokenIds):
    with getDbConnection() as conn:
        with conn.cursor() as curs:

            SQL = """DELETE FROM TOKEN_QUESTION_MAP WHERE"""
            for tId in tokenIds:
                if tokenIds.index(tId) != 0:
                    SQL += " OR"
                SQL += " TOKEN_ID = %s"
            SQL += ';'
            curs.execute(SQL, tokenIds)

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
