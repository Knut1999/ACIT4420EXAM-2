from database.offers.offersDatabase import OfferDatabase

class Company:
    def __init__(self, name:str):
        self.name = name
        self.offers:list[Offer] = []
        self.companyRouts = []

    def generateOffers(self, destination:str) -> None:

        self.offers = [] #so we dont get double is we search in frontend many times
        self.companyRouts = self._getCompanyRouts(destination) #find the destination
        for rout in self.companyRouts:
            offer = Offer(rout)
            self.offers.append(offer)

    def _getCompanyRouts(self, destination:str) -> list:
        return OfferDatabase.getCompanyRouts(self.name, destination)

    def getOffers(self):
        return self.offers


class Offer:
    def __init__(self, info:list) -> None:
        self.id = info[0]
        self.companyName = info[1]
        self.destination = info[2]
        self.travelDate = info[3]
        self.departureTime = info[4]
        self.duration = info[5]
        self.arrivalTime = info[6]
        self.price = info[7]
        self.transfers = info[8]
        self.luggageAllowance = info[9]
        self.changeability = info[10]
        self.refundability = info[11]
        self.availableSeats = info[12]
        self.customerRating = info[13]
        self.environmentalMeasure = info[14]

        self.score = None
        self.priceScore = None
        self.durationScore = None
        self.timeScore = None
        self.flexibilityScore = None
        self.ratingScore = None
        self.transfersScore = None
        self.environmentScore = None

    def setScore(
        self,
        score: float,
        priceScore: float,
        durationScore: float,
        timeScore: float,
        flexibilityScore: float,
        ratingScore: float,
        transfersScore: float,
        environmentScore: float
        ):
        self.score = score
        self.priceScore = priceScore
        self.durationScore = durationScore
        self.timeScore = timeScore
        self.flexibilityScore = flexibilityScore
        self.ratingScore = ratingScore
        self.transfersScore = transfersScore
        self.environmentScore = environmentScore