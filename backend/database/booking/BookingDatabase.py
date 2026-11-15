import os

from dotenv import load_dotenv
import psycopg


class BookingDatabase:
    @staticmethod
    def emptyBookingsDB():
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL")
        con = psycopg.connect(DATABASE_URL)
        cur = con.cursor()
        cur.execute("""
            TRUNCATE TABLE "bookings" RESTART IDENTITY
        """)
        con.commit()

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
    def bookSeat(offerId:int, firstName:str, lastName:str, bookingRef:str):
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL")
        con = psycopg.connect(DATABASE_URL)
        cur = con.cursor()
        cur.execute("""
            INSERT INTO "bookings" 
            (
            offer_id, first_name, last_name, booking_ref
            ) VALUES (%s, %s, %s, %s)""",
            (offerId, firstName, lastName, bookingRef)
        )

        con.commit()
        con.close()

    @staticmethod
    def unBookSeat(offerId:int, firstName:str, lastName:str):
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL")
        con = psycopg.connect(DATABASE_URL)
        cur = con.cursor()
        cur.execute("""
            DELETE FROM bookings
            WHERE user_id = (
                SELECT user_id
                FROM bookings
                WHERE offer_id = %s
                AND first_name = %s
                AND last_name = %s
                LIMIT 1
            )""",
            (offerId, firstName, lastName)
        )

        con.commit()
        con.close()

    @staticmethod
    def getBookingsFromName(firstName, lastName):
        #https://docs.python.org/3/library/sqlite3.html?utm used this link as insperation
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL")
        con = psycopg.connect(DATABASE_URL)
        cur = con.cursor()
        res = cur.execute("""
            SELECT * 
            FROM "bookings" 
            WHERE first_name = %s
            AND last_name = %s"""
            , (firstName,lastName)
        )
        route = res.fetchall()
        con.close()

        #had to do this to not get [(141,), (141,), (141,)] syntax
        routelist = []
        for r in route:
            routelist.append(r)
        
        return routelist

    @staticmethod
    def getIdFromName(first_name,last_name):
        #https://docs.python.org/3/library/sqlite3.html?utm used this link as insperation
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL")
        con = psycopg.connect(DATABASE_URL)
        cur = con.cursor()
        res = cur.execute("""
            SELECT user_id 
            FROM "bookings" 
            WHERE first_name = %s
            AND last_name = %s"""
            , (first_name,last_name)
        )
        user_id = res.fetchall()[0][0]
        con.close()

        return user_id