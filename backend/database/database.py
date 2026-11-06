import os
import sqlite3
from dotenv import load_dotenv
import psycopg

class Database:
    db_path = "database/dataset.db"

    @staticmethod
    def getCompanies():
        #https://docs.python.org/3/library/sqlite3.html?utm used this link as insperation
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL")
        con = psycopg.connect(DATABASE_URL)
        cur = con.cursor()
        #"https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/" to know how to get things from sql db
        res = cur.execute('SELECT company FROM "routInfo"')
        companies_db = res.fetchall()
        con.close()
        companies = set()
        for companie in companies_db:
            companies.add(companie[0])
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
    
if __name__ == "__main__":
    database = Database()
    ids = database.getIdFromCompanyName("NONAME")
    print(ids)
