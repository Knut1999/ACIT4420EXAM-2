from offer.standaloneFunctions import findMinOrMaxRating, findMinOrMaxTransfers, timeStrToHour, timeDelta, findMinOrMaxWait,findMinOrMaxDuration,findMinOrMaxPrice,findMinOrMaxEnvironment, explainValues
from offer.offerClasses import Company, Offer

class OfferRanker:
    def __init__(self, companies:list[Company], destination:str, preferredDepartureTime:str, budget:float, weights:list[float]):
        self._companies = companies
        self._destination = destination
        self._preferredDepartureTime = timeStrToHour(preferredDepartureTime)
        self._budget = budget
        #we could filter by budget in _fillAllOffers(), but for readability, we dont
        self._rankedOffersList:list[Offer] = self._fillAllOffers()
        #filtered by budget, so the list below does not have offer above budget
        self._validRankedOffersList:Offer = self._filterByBudget(self._rankedOffersList)
        # we need to find min and max values for later
        self.maxPrice = findMinOrMaxPrice(self._validRankedOffersList, True)
        self.maxDuration = findMinOrMaxDuration(self._validRankedOffersList, True)        
        self.minPrice = findMinOrMaxPrice(self._validRankedOffersList, False)
        self.minDuration = findMinOrMaxDuration(self._validRankedOffersList, False)
        self.maxWait = findMinOrMaxWait(self._validRankedOffersList, self._preferredDepartureTime, True)
        self.minWait = findMinOrMaxWait(self._validRankedOffersList, self._preferredDepartureTime, False)
        self.maxRating = findMinOrMaxRating(self._validRankedOffersList, True)
        self.minRating = findMinOrMaxRating(self._validRankedOffersList, False)
        self.maxTransfers = findMinOrMaxTransfers(self._validRankedOffersList, True)
        self.minTransfers = findMinOrMaxTransfers(self._validRankedOffersList, False)
        self.maxEnvironment = findMinOrMaxEnvironment(self._validRankedOffersList, True)
        self.minEnvironment = findMinOrMaxEnvironment(self._validRankedOffersList, False)

        self.minWait
        #defult values
        self.w_price = weights[0]
        self.w_duration = weights[1]
        self.w_time = weights[2]
        self.w_flexibility = weights[3]
        self.w_customerRating = weights[4]
        self.w_transfers = weights[5]
        self.w_environment = weights[6]
        self._calculateScores()
        self._sortOffers()

    def _filterByBudget(self, _rankedOffersList):
        updatetList = []
        for offer in _rankedOffersList:
            if offer.price <= self._budget:
                updatetList.append(offer)
        return updatetList

    def _sortOffers(self):
        #used example: sorted(student_tuples, key=lambda student: student[2])   # sort by age
        #from this link: https://docs.python.org/3/howto/sorting.html
        self._validRankedOffersList = sorted(self._validRankedOffersList, key=lambda offer: offer.score, reverse=True)


    def _fillAllOffers(self):
        allOffers = []
        for company in self._companies:
            allOffers.extend(company.getOffers())
        return allOffers

    def getRankedOffers(self):
        return self._validRankedOffersList

    def getExplentation(self):
        return self.explaneWinner()


    def _calculateScores(self):
        for offer in self._validRankedOffersList:
            #find the _score
            #put the _score in the offer object
            offer.setScore(
                self._score(offer),
                self._P(offer),
                self._D(offer),
                self._T(offer),
                self._F(offer),
                self._R(offer),
                self._TR(offer),
                self._E(offer)
            )

    def explaneWinner(self):
        highestScore = 0
        winnerOffer = None
        for offer in self._validRankedOffersList:
            if(offer.score > highestScore):
                highestScore = offer.score
                winnerOffer = offer

        if(winnerOffer == None):
            return "Ingen vinner"

        explenation = explainValues(
            self.w_price,
            self.w_duration,
            self.w_time,
            self.w_flexibility,
            self.w_customerRating,
            self.w_transfers,
            self.w_environment,
            self._P(winnerOffer),
            self._D(winnerOffer),
            self._T(winnerOffer),
            self._F(winnerOffer),
            self._R(winnerOffer),
            self._TR(winnerOffer),
            self._E(winnerOffer)
        )

        return explenation

    def _score(self, offer:Offer) -> float: 
        # Score(j) = w_price P(j) + w_duration D(j) + w_time T(j) + w_flexibility F(j) + w_customerRating R(j) 
        # + w_transfers * TR(j)
        return (self.w_price * self._P(offer) + 
                self.w_duration * self._D(offer) + 
                self.w_time * self._T(offer) + 
                self.w_flexibility * self._F(offer) +
                self.w_customerRating * self._R(offer) +
                self.w_transfers * self._TR(offer) +
                self.w_environment * self._E(offer))

    def _P(self, offer:Offer):
        if (self.maxPrice == self.minPrice):
            return 1.0
        return ((self.maxPrice - offer.price) / (self.maxPrice - self.minPrice))
    def _D(self, offer:Offer):
        if(self.maxDuration == self.minDuration):
            return 1.0
        return ((self.maxDuration - offer.duration) / (self.maxDuration - self.minDuration)) 
    def _T(self, offer:Offer):
        offerDepartureTime = timeStrToHour(offer.departureTime)
        delta = timeDelta(offerDepartureTime, self._preferredDepartureTime)
        if(self.maxWait == self.minWait):
            return 1
        return ((self.maxWait - delta) / (self.maxWait - self.minWait))
    def _F(self, offer:Offer):
        sum = 0
        if(offer.refundability == "LIMITED"): sum += 0.25
        elif(offer.refundability == "FULL"): sum += 0.5
        if(offer.changeability == "LIMITED"): sum += 0.25
        elif(offer.changeability == "FULL"): sum += 0.5
        return sum
    def _R(self, offer:Offer):
        if (self.maxRating == self.minRating):
            return 1.0
        return (offer.customerRating - self.minRating) / (self.maxRating - self.minRating)
    def _TR(self, offer:Offer):
        if (self.maxTransfers == self.minTransfers):
            return 1.0
        return (self.maxTransfers - offer.transfers) / (self.maxTransfers - self.minTransfers)
    def _E(self, offer:Offer):
        if (self.maxEnvironment == self.minEnvironment):
            return 1.0
        return (offer.environmentalMeasure - self.minEnvironment) / (self.maxEnvironment - self.minEnvironment)

