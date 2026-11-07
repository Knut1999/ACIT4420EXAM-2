from database.offers.offersDatabase import OfferDatabase
from database.booking.BookingDatabase import BookingDatabase

def availableSeats(id) -> bool:
    route = OfferDatabase.getLineFromId(id)
    seats = route[0][12]
    if(seats <= 0):
        return False
    else:
        return True
