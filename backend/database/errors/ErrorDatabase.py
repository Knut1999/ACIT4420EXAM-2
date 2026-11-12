import os

from dotenv import load_dotenv
import psycopg


class ErrorDatabase:
    @staticmethod
    def emptyErrorMessageDB():
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL")
        con = psycopg.connect(DATABASE_URL)
        cur = con.cursor()
        cur.execute("""
            TRUNCATE TABLE "errors" RESTART IDENTITY
        """)
        con.commit()

    @staticmethod
    def errorMessageToDB(offer_id, errortype, error):
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL")
        con = psycopg.connect(DATABASE_URL)
        cur = con.cursor()
        cur.execute("""
            INSERT INTO "errors" 
            (
            offer_id, error_type, error 
            ) VALUES (%s,%s, %s)""",
            (offer_id, errortype, error)
        )
        con.commit()
        con.close()