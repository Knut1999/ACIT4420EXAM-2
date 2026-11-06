from datetime import date
import psycopg
from database.generateData import generateCaminoExpress, generateCostaLink, generateNocheVia, generateSolRuta, generateVerdeBus, transferErrorRecordsToDatabase
from offer.standaloneFunctions import getDestinations, getTravelTimes, getTravelPrices
import os
import psycopg
from dotenv import load_dotenv



today = date.today()
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg.connect(DATABASE_URL)
cursor = conn.cursor()
def fill_db():
    #this open database and delete prev values
    cursor.execute("""
        TRUNCATE TABLE "routInfo" RESTART IDENTITY
    """)
    conn.commit()

    #logic for filling DB
    departureHub = "Madrid"
    destinations = getDestinations()
    for i in range(len(destinations)):
        #for longer db
        for j in range(3):
            solRutaDict = generateSolRuta(destinations[i])
            caminoExpress = generateCaminoExpress(destinations[i])
            costaLink = generateCostaLink(destinations[i])
            verdeBus = generateVerdeBus(destinations[i])
            nocheVia = generateNocheVia(destinations[i])
            sqlInsertion(solRutaDict)
            sqlInsertion(caminoExpress)
            sqlInsertion(costaLink)
            sqlInsertion(verdeBus)
            sqlInsertion(nocheVia)
    errors = transferErrorRecordsToDatabase()
    for error in errors:
        sqlInsertion(error)
    conn.commit()
    conn.close()

def sqlInsertion(dict):
    try:
        cursor.execute(
            """INSERT INTO "routInfo" (
                company, destination, travel_date, departure, duration,
                arrival_time, price, transfers, luggage_allowance,
                changeability, refundability, available_seats,
                customer_rating, environmental_measure
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (dict["company"], dict["destination"], dict["travel_date"],
            dict["departure_time"], dict["duration"], dict["arrival_time"],
            dict["price"], dict["transfers"], dict["luggage_allowance"],
            dict["changeability"], dict["refundability"], dict["available_seats"],
            dict["customer_rating"], dict["environmental_measure"])
        )
    except (ValueError, IndexError, KeyError) as e:
        print(f"Skipping offer: {e}")
    


if __name__ == "__main__":
    fill_db()
