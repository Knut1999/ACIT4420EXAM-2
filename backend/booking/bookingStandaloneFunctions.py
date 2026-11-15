from database.offers.offersDatabase import OfferDatabase

def availableSeats(id) -> bool:
    route = OfferDatabase.getLineFromId(id)
    seats = route[0][12]
    if(seats <= 0):
        return False
    else:
        return True

def createBookingRef(offerId: int, firstName: str, lastName: str):
    offerRef = f"{firstName}-{lastName}-"
    offerRef += getOfferInfo(offerId)
    return offerRef
    

def addFirstChar(func):
    def wrapper(*args, **kwargs):
        offer = func(*args, **kwargs)

        offerId = offer[0][0]
        company = offer[0][1]
        destination = offer[0][2]

        bookingRef = f"{offerId}-{company[:3].upper()}-{destination[:3].upper()}"

        return bookingRef

    return wrapper

@addFirstChar
def getOfferInfo(offerId:int):
    offer = OfferDatabase.getLineFromId(offerId)
    return offer



if __name__ == "__main__":
    print(createBookingRef(1,"k","k"))