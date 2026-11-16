from offer.OfferRanker import OfferRanker
from offer.standaloneFunctions import getOffers, createCompanyObjects, normalizeWeights
from validation.validation import validateCompany, validateOffers
from database.offers.offersDatabase import OfferDatabase
from app_logging.logging import Log
from database.errors.ErrorDatabase import ErrorDatabase


class OfferController:
    def __init__(self):
        #list of strings of the company names from static Database function
        self._companies_set = OfferDatabase.getCompanies()
        # create company objects
        self._companies = createCompanyObjects(self._companies_set)
        #first create emty invalid csv, then remove _companies with faulty names(put them in the invalid csv), update list with valid _companies
        # create_empty_invalid_records()
        self._companies = validateCompany(self._companies)
        self.offerRanker = None
        self._destination = None
        self._preferredDepartureTime = None
        self._budget = None
        self._weights = None


    def websiteInputs(self, _destination, _budget, _preferredDepartureTime, _weights):
        self._destination = _destination
        self._preferredDepartureTime = _preferredDepartureTime
        self._budget = _budget
        self._weights = normalizeWeights(_weights)
        self._generateOffers()
        return self.offerRanker.getRankedOffers()


    def _generateOffers(self):
        Log.logInsert("generate offers")
        
        #emty the error database before creating new offers, it will be filled with error from
        # the new offers
        ErrorDatabase.emptyErrorMessageDB()
        for company in self._companies:
            company.generateOffers(self._destination)
            validateOffers(company) #removes invalid offers, puts them in invalid_records.csv
        self._rankOffers()

    def _rankOffers(self):
        self.offerRanker = OfferRanker(self._companies, self._destination, self._preferredDepartureTime, self._budget, self._weights)

    
        

    
            

if __name__ == "__main__":
    getOffers()