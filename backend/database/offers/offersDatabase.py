import os
import sqlite3
from dotenv import load_dotenv
import psycopg

class OfferDatabase:
    @staticmethod
    def emptyOffersDB():
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL")
        con = psycopg.connect(DATABASE_URL)
        cur = con.cursor()
        cur.execute("""
            TRUNCATE TABLE "routInfo" RESTART IDENTITY
        """)
        con.commit()
        con.close()

    @staticmethod
    def getCompanies():
        #https://docs.python.org/3/library/sqlite3.html?utm used this link as insperation
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL")
        con = psycopg.connect(DATABASE_URL)
        cur = con.cursor()
        #"https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/" to know how to get things from sql db
        res = cur.execute("""
            SELECT company FROM "routInfo"
            """)
        companies_db = res.fetchall()
        con.close()
        companies = set()
        for companie in companies_db:
            companies.add(companie[0])

        if not companies:
            raise ValueError("No companies found in the database")
                
        return companies

    @staticmethod
    def getIdFromCompanyName(companyName):
        #https://docs.python.org/3/library/sqlite3.html?utm used this link as insperation
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL")
        con = psycopg.connect(DATABASE_URL)
        cur = con.cursor()
        res = cur.execute("""
            SELECT id 
            FROM "routInfo" 
            WHERE company = %s"""
            , (companyName,)
        )
        companies_db = res.fetchall()
        con.close()
        id = []
        for companie in companies_db:
            id.append(companie[0])
        return id

    @staticmethod
    def getCompanyRouts(companyName, destination):
        #https://docs.python.org/3/library/sqlite3.html?utm used this link as insperation
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL")
        con = psycopg.connect(DATABASE_URL)
        cur = con.cursor()
        res = cur.execute("""
            SELECT * 
            FROM "routInfo" 
            WHERE company = %s
            AND destination = %s"""
            , (companyName, destination)
        )
        routs = res.fetchall()
        con.close()
        return routs

    @staticmethod
    def getEveryLineInDb():
        #https://docs.python.org/3/library/sqlite3.html?utm used this link as insperation
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL")
        con = psycopg.connect(DATABASE_URL)
        cur = con.cursor()
        res = cur.execute("""
            SELECT * 
            FROM "routInfo"
            """
        )
        routs = res.fetchall()
        con.close()
        return routs

    @staticmethod
    def getLineFromId(id):
        #https://docs.python.org/3/library/sqlite3.html?utm used this link as insperation
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL")
        con = psycopg.connect(DATABASE_URL)
        cur = con.cursor()
        res = cur.execute("""
            SELECT * 
            FROM "routInfo" 
            WHERE id = %s"""
            , (id,)
        )
        route = res.fetchall()
        con.close()
        return route

    @staticmethod
    def reduceSeatFromId(id):
        #https://docs.python.org/3/library/sqlite3.html?utm used this link as insperation
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL")
        con = psycopg.connect(DATABASE_URL)
        cur = con.cursor()
        cur.execute("""
            UPDATE "routInfo"
            SET available_seats = available_seats - 1
            WHERE id = %s"""
            , (id,)
        )
        con.commit()
        con.close()

    @staticmethod
    def increaseSeatFromId(id):
        #https://docs.python.org/3/library/sqlite3.html?utm used this link as insperation
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL")
        con = psycopg.connect(DATABASE_URL)
        cur = con.cursor()
        cur.execute("""
            UPDATE "routInfo"
            SET available_seats = available_seats + 1
            WHERE id = %s"""
            , (id,)
        )
        con.commit()
        con.close()
    
if __name__ == "__main__":
    database = OfferDatabase()
    ids = database.getIdFromCompanyName("NONAME")