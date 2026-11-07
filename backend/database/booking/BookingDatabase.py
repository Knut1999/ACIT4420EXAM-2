import os

from dotenv import load_dotenv
import psycopg


class BookingDatabase:
    
    @staticmethod
    def user_exists(firstName:str, lastName:str):
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL")
        con = psycopg.connect(DATABASE_URL)
        cur = con.cursor()
        res = cur.execute("""
            SELECT 1 
            FROM "bookings" 
            WHERE first_name = %s
            AND last_name = %s"""
            , (firstName,lastName)
        )
        routs = res.fetchall()
        if routs: 
            return True
        return False

    @staticmethod
    def user_to_db(firstName:str, lastName:str):
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL")
        con = psycopg.connect(DATABASE_URL)
        cur = con.cursor()
        cur.execute("""
            INSERT INTO "bookings" 
            (
            first_name, last_name 
            ) VALUES (%s, %s)""",
            (firstName, lastName)
        )
        con.commit()
        con.close()

    @staticmethod
    def bookSeat(offerId:int, firstName:str, lastName:str):
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL")
        con = psycopg.connect(DATABASE_URL)
        cur = con.cursor()
        cur.execute("""
            UPDATE "bookings"
            SET offer_ids = array_append(offer_ids, %s)
            WHERE first_name = %s
            and last_name = %s
            """,
            (offerId, firstName, lastName)
        )

        con.commit()
        con.close()

    @staticmethod
    def getBookingFromId(id):
        #https://docs.python.org/3/library/sqlite3.html?utm used this link as insperation
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL")
        con = psycopg.connect(DATABASE_URL)
        cur = con.cursor()
        res = cur.execute("""
            SELECT offer_ids 
            FROM "bookings" 
            WHERE id = %s"""
            , (id,)
        )
        route = res.fetchall()[0]
        con.close()
        return route

    @staticmethod
    def getIdFromName(first_name,last_name):
        #https://docs.python.org/3/library/sqlite3.html?utm used this link as insperation
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL")
        con = psycopg.connect(DATABASE_URL)
        cur = con.cursor()
        res = cur.execute("""
            SELECT id 
            FROM "bookings" 
            WHERE first_name = %s
            AND last_name = %s"""
            , (first_name,last_name)
        )
        companies_db = res.fetchall()
        con.close()

        return res