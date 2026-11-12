import os

from dotenv import load_dotenv
import psycopg


class LoggerDatabase:
    @staticmethod
    def emptyLogDB():
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL")
        con = psycopg.connect(DATABASE_URL)
        cur = con.cursor()
        cur.execute("""
            TRUNCATE TABLE "logs" RESTART IDENTITY
        """)
        con.commit()

    @staticmethod
    def logMessageToDB(value):
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL")
        con = psycopg.connect(DATABASE_URL)
        cur = con.cursor()
        cur.execute("""
            INSERT INTO "logs" 
            (
            logmessage 
            ) VALUES (%s)""",
            (value,)
        )
        con.commit()
        con.close()

    @staticmethod
    def getWholeLog():
        #https://docs.python.org/3/library/sqlite3.html?utm used this link as insperation
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL")
        con = psycopg.connect(DATABASE_URL)
        cur = con.cursor()
        res = cur.execute("""
            SELECT * 
            FROM "logs"
            """
        )
        routs = res.fetchall()
        con.close()
        return routs