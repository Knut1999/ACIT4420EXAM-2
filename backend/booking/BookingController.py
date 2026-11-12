from logging.logging import Log
from database.booking.BookingDatabase import BookingDatabase
from booking.bookingStandaloneFunctions import availableSeats
from database.offers.offersDatabase import OfferDatabase

class BookingController:

    def bookingInputs(self, offerId:int, firstName:str, lastName:str):
        Log.logInsert("Try to book seat")
        #checking if there are available seats
        if(availableSeats(offerId) == False):
            Log.logInsert("No available seats")
            return "No available seats"

        #creating booking
        self.bookSeat(offerId, firstName, lastName)
        Log.logInsert("Booking successful")

    def bookSeat(self, offerId:int, firstName:str, lastName:str):
        Log.logInsert("Book seat")
        #we use offer ids to book the offers
        BookingDatabase.bookSeat(offerId, firstName, lastName)
        OfferDatabase.reduceSeatFromId(offerId)

    def getAllBookings(self, firstName:str, lastName:str):
        Log.logInsert("Get all bookings")
        #we need offer ids to get the offer we have ordered
        allBookings = BookingDatabase.getBookingsFromName(firstName, lastName)
        # print(allBookings)
        bookedOffers = []
        for id in allBookings:
            bookedOffers.append(OfferDatabase.getLineFromId(id)[0])

        return bookedOffers

    def cancelBooking(self, offerId:int, firstName:str, lastName:str):
        Log.logInsert("Cancel booking")
        #we need offer ids to get the offer we have ordered
        allBookings = BookingDatabase.getBookingsFromName(firstName, lastName)
        
        for booking in allBookings:
            if booking == offerId:
                BookingDatabase.unBookSeat(offerId, firstName, lastName)
                OfferDatabase.increaseSeatFromId(offerId)
                Log.logInsert("Cancel successful")
                return
        Log.logInsert("Cancel not successful")
        

