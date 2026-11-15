from offer.OfferRanker import OfferRanker
from offer.standaloneFunctions import getOffers, createCompanyObjects, normalizeWeights
from validation.validation import validateCompany, validateOffers
from database.offers.offersDatabase import OfferDatabase
from app_logging.logging import Log
from database.errors.ErrorDatabase import ErrorDatabase


class OfferController:
    def __init__(self):
        #list of strings of the company names from static Database function
        self.companies_set = OfferDatabase.getCompanies()
        # create company objects
        self.companies = createCompanyObjects(self.companies_set)
        #first create emty invalid csv, then remove companies with faulty names(put them in the invalid csv), update list with valid companies
        # create_empty_invalid_records()
        self.companies = validateCompany(self.companies)
        self.offerRanker = None
        self.destination = None
        self.preferredDepartureTime = None
        self.budget = None
        self.weights = None
        

        

    def websiteInputs(self, destination, budget, preferredDepartureTime, weights):
        self.destination = destination
        self.preferredDepartureTime = preferredDepartureTime
        self.budget = budget
        self.weights = normalizeWeights(weights)
        self.generateOffers()
        return self.offerRanker.getRankedOffers()


    def generateOffers(self):
        Log.logInsert("generate offers")
        
        #emty the error database before creating new offers, it will be filled with error from
        # the new offers
        ErrorDatabase.emptyErrorMessageDB()
        for company in self.companies:
            company.generateOffers(self.destination)
            validateOffers(company) #removes invalid offers, puts them in invalid_records.csv
        self.rankOffers()

    def rankOffers(self):
        self.offerRanker = OfferRanker(self.companies, self.destination, self.preferredDepartureTime, self.budget, self.weights)

    
        

    
            

if __name__ == "__main__":
    getOffers()