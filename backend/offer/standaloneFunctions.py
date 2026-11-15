from datetime import datetime
from offer.offerClasses import Company, Offer
import csv
import sqlite3
import os
if os.name == "nt":
    csv_file_path = "tmp/invalid_records.csv"
else:
    csv_file_path = "/tmp/invalid_records.csv"

def createCompanyObjects(company_set):
    companies = []
    for company_name in company_set:
        company = Company(company_name)
        companies.append(company)
    return companies

def getOffers():
    #https://docs.python.org/3/library/sqlite3.html?utm used this link as insperation
    con = sqlite3.connect("dataset.db")
    cur = con.cursor()
    res = cur.execute("SELECT * FROM routInfo")
    offers_db = res.fetchall()
    offers = []
    for offer in offers_db:
        offers.append(offer)
    return offer

def readInvalidRecordsIds(id):
    try:
        with open(csv_file_path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if str(id) in row["ids"]:
                    return True
        return False
    except FileNotFoundError:
        return False

def getDestinations():
    return ["Barcelona", 
            "Valencia", 
            "Seville", 
            "Malaga", 
            "Granada", 
            "Cordoba", 
            "Bilbao", 
            "San Sebastian", 
            "Zaragoza", 
            "Alicante", 
            "Murcia", 
            "Salamanca", 
            "Toledo", 
            "Santiago de Compostela", 
            "Cadiz"]

def getTravelTime(destination):
    return getTravelTimes()[destination]

def getTravelTimes():
    return {
        "Barcelona": 7.0,
        "Cordoba": 4.5,
        "Murcia": 4.5,
        "Valencia": 4.0,
        "Bilbao": 5.0,
        "Salamanca": 2.5,
        "Seville": 6.0,
        "San Sebastian": 6.0,
        "Toledo": 1.5,
        "Malaga": 6.0,
        "Zaragoza": 4.0,
        "Santiago de Compostela": 7.0,
        "Granada": 5.0,
        "Alicante": 5.0,
        "Cadiz": 7.0
    }

def getTravelPrice(destination):
    return getTravelPrices()[destination]
def getTravelPrices():
    return {
        "Barcelona": 35.0,
        "Cordoba": 22.5,
        "Murcia": 22.5,
        "Valencia": 20.0,
        "Bilbao": 25.0,
        "Salamanca": 12.5,
        "Seville": 30.0,
        "San Sebastian": 30.0,
        "Toledo": 7.5,
        "Malaga": 30.0,
        "Zaragoza": 20.0,
        "Santiago de Compostela": 35.0,
        "Granada": 25.0,
        "Alicante": 25.0,
        "Cadiz": 35.0
    }

def getCompanies():
    return ["SolRuta","Camino Express","CostaLink","VerdeBus","NocheVia"]

def timeStrToHour(departureTime):
    return datetime.strptime(departureTime, "%H:%M")

def dateStrToDate(date):
    return datetime.strptime(date, "%Y-%m-%d")

def timeDelta(time1, time2):
    return abs(time1 - time2).total_seconds() / 3600

def findMinOrMaxPrice(validRankedOffersList:list[Offer], Max:bool):
    allPrices = []
    for offer in validRankedOffersList:
        allPrices.append(offer.price)
    if(Max == True):
        return max(allPrices)
    if(Max == False):
        return min(allPrices)
    return

def findMinOrMaxDuration(validRankedOffersList:list[Offer], Max:bool):
    allDurations = []
    for offer in validRankedOffersList:
        allDurations.append(offer.duration)
    if(Max == True):
        return max(allDurations)
    if(Max == False):
        return min(allDurations)
    return
def findMinOrMaxWait(validRankedOffersList:list[Offer],preferredDepartureTime, Max:bool):
    deltaList = []
    for offer in validRankedOffersList:
        offerDepartureTime = timeStrToHour(offer.departureTime)
        delta = timeDelta(offerDepartureTime, preferredDepartureTime)
        deltaList.append(delta)
    if(Max == True):
        return max(deltaList)
    if(Max == False):
        return min(deltaList)
    return
def findMinOrMaxRating(validRankedOffersList:list[Offer], Max:bool):
    allRatings = []
    for offer in validRankedOffersList:
        allRatings.append(offer.customerRating)
    if(Max == True):
        return max(allRatings)
    if(Max == False):
        return min(allRatings)
    return
def findMinOrMaxTransfers(validRankedOffersList:list[Offer], Max:bool):
    allTransfers = []
    for offer in validRankedOffersList:
        allTransfers.append(offer.transfers)
    if(Max == True):
        return max(allTransfers)
    if(Max == False):
        return min(allTransfers)
    return
def findMinOrMaxEnvironment(validRankedOffersList:list[Offer], Max:bool):
    allEnvironment = []
    for offer in validRankedOffersList:
        allEnvironment.append(offer.environmentalMeasure)
    if(Max == True):
        return max(allEnvironment)
    if(Max == False):
        return min(allEnvironment)
    return

def normalizeWeights(weights):
    total = sum(weights)
    #So we find the sum, then just divide each number at the sum
    #then every weight will be between 0 and 1
    if(total == 0):
        return [1/7,1/7,1/7,1/7,1/7,1/7,1/7]
    for i in range(7):
        weights[i] = weights[i] / total
    return weights

#very simple function, but gives good explenation
def explainValues(wP, wD, wT, wF, wR, wTR, wE, P, D, T, F, R, TR, E):
    explanation = ""

    if wP >= 0.2:
        explanation += "Price was an important factor in the ranking. "
    if wD >= 0.2:
        explanation += "Journey duration was an important factor in the ranking. "
    if wT >= 0.2:
        explanation += "Departure time was an important factor in the ranking. "
    if wF >= 0.2:
        explanation += "Ticket flexibility was an important factor in the ranking. "
    if wR >= 0.2:
        explanation += "Customer rating was an important factor in the ranking. "
    if wTR >= 0.2:
        explanation += "Number of transfers was an important factor in the ranking. "
    if wE >= 0.2:
        explanation += "Environmental performance was an important factor in the ranking. "

    if P < 0.3:
        explanation += "Despite the price being relatively high compared to other offers, "
    elif P > 0.7:
        explanation += "The offer has a competitive price compared to other offers. "

    if D < 0.3:
        explanation += "The journey takes considerably longer than competing offers. "
    elif D > 0.7:
        explanation += "The journey has a relatively short duration. "

    if T < 0.3:
        explanation += "The departure time is far from the preferred departure time. "
    elif T > 0.7:
        explanation += "The departure time is close to the preferred departure time. "

    if F < 0.3:
        explanation += "The ticket has limited flexibility. "
    elif F > 0.7:
        explanation += "The ticket offers good flexibility. "

    if R < 0.3:
        explanation += "The customer rating is relatively low. "
    elif R > 0.7:
        explanation += "The offer has a high customer rating. "

    if TR < 0.3:
        explanation += "The journey requires many transfers. "
    elif TR > 0.7:
        explanation += "The journey has relatively few transfers. "

    if E < 0.3:
        explanation += "The environmental performance is relatively poor. "
    elif E > 0.7:
        explanation += "The offer has good environmental performance. "

    return explanation