from database.booking.BookingDatabase import BookingDatabase
from booking.bookingStandaloneFunctions import createUser, availableSeats, findUser
from database.offers.offersDatabase import OfferDatabase
from booking.bookingClasses import User

class BookingController:
    def __init__(self):
        self.users:list[User] = []
    def bookingInputs(self, offerId:int, firstName:str, lastName:str):
        #checking if user exist
        if(BookingDatabase.user_exists(firstName, lastName) == False):
            BookingDatabase.user_to_db(firstName,lastName)
            user = createUser(firstName, lastName)
            self.users.append(user)
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
        userObject = findUser(self.users, firstName, lastName)

        if(userObject == None):
            return "User not in database"

        #we need offer ids to get the offer we have ordered
        offerIds = BookingDatabase(userObject.id)
        bookedOffers = []
        for id in offerIds:
            bookedOffers.append(OfferDatabase.getLineFromId(id))

        return bookedOffers