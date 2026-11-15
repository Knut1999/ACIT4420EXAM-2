from datetime import date, datetime
from logging import exception

from validation.standaloneFunctionsValidation import validateCustomerRating, validateDate, validateDepartureAndArrival, validateDestination, validateNonNegativeFloat, validateNonNegativeInteger
from offer.offerClasses import Company
from database.offers.offersDatabase import OfferDatabase
from offer.standaloneFunctions import getCompanies
from database.errors.ErrorDatabase import ErrorDatabase
from validation.OfferValidationError import OfferValidationError

def validateCompany(companyList: list[Company]) -> list[Company]:
    validCompaniesStr = getCompanies()
    validCompanies = []
    inValidCompanies = []
    for company in companyList:
        if company.name not in validCompaniesStr:
            inValidCompanies.append(company)
            continue
        validCompanies.append(company)

    for errCompany in inValidCompanies:
        errorType = "Invalid company name"
        error = errCompany.name
        # ids = OfferDatabase.getIdFromCompanyName(errCompany.name)
        ErrorDatabase.errorMessageToDB(None, errorType, error)
            
    return validCompanies

def validateOffers(company:Company):
    offersToRemove = []
    for offer in company.offers:
        errorType = []
        error = []
        #companyName is already validated in controller __init__
        try: 
            validateDestination(offer)
        except OfferValidationError as exception:
            #because function use InvalidDestinationError, we can use type.__name__
            errorType.append(type(exception).__name__)
            #get the error message from the function
            error.append(str(exception))

        #checking if traveldate is in future and that type is correct
        try:
            validateDate(offer)
        except OfferValidationError as exception:
            errorType.append(type(exception).__name__)
            error.append(str(exception))

        #checking departure time
        try:
            validateDepartureAndArrival(offer)
        except OfferValidationError as exception:
            errorType.append(type(exception).__name__)
            error.append(str(exception))

        #check duration
        try:
            validateNonNegativeFloat(offer)
        except OfferValidationError as exception:
            errorType.append(type(exception).__name__)
            error.append(str(exception))
        #check transfers for int and above 0
        try:
            validateNonNegativeInteger(offer)
        except OfferValidationError as exception:
            errorType.append(type(exception).__name__)
            error.append(str(exception))
        #customer rating between 1 and 5
        try:
            validateCustomerRating(offer)
        except OfferValidationError as exception:
            errorType.append(type(exception).__name__)
            error.append(str(exception))

        if(errorType):
            print(offer.companyName, offer.destination, errorType, error)
            offersToRemove.append(offer)
            for i in range(len(errorType)):
                ErrorDatabase.errorMessageToDB(offer.id, errorType[i], error[i])
    for offer in offersToRemove:
        company.getOffers().remove(offer)
        # print("remove", offer)
                

