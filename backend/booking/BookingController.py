from database.booking.BookingDatabase import BookingDatabase
from booking.bookingStandaloneFunctions import availableSeats
from database.offers.offersDatabase import OfferDatabase

class BookingController:

    def bookingInputs(self, offerId:int, firstName:str, lastName:str):
        #checking if there are available seats
        if(availableSeats(offerId) == False):
            return "No available seats"

        #creating booking
        self.bookSeat(offerId, firstName, lastName)

    def bookSeat(self, offerId:int, firstName:str, lastName:str):
        #we use offer ids to book the offers
        BookingDatabase.bookSeat(offerId, firstName, lastName)
        OfferDatabase.reduceSeatFromId(offerId)

    def getAllBookings(self, firstName:str, lastName:str):
        #we need offer ids to get the offer we have ordered
        allBookings = BookingDatabase.getBookingsFromName(firstName, lastName)
        # print(allBookings)
        bookedOffers = []
        for id in allBookings:
            bookedOffers.append(OfferDatabase.getLineFromId(id)[0])

        return bookedOffers

    def cancelBooking(self, offerId:int, firstName:str, lastName:str):
        #we need offer ids to get the offer we have ordered
        allBookings = BookingDatabase.getBookingsFromName(firstName, lastName)
        
        for booking in allBookings:
            if booking == offerId:
                BookingDatabase.unBookSeat(offerId, firstName, lastName)
                OfferDatabase.increaseSeatFromId(offerId)
                break
        return

