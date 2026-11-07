from database.offers.offersDatabase import OfferDatabase
from booking.bookingClasses import User


def createUser(firstName, lastName) -> User:
    return User(firstName, lastName)

def availableSeats(id) -> bool:
    route = OfferDatabase.getLineFromId(id)
    seats = route[0][12]
    if(seats <= 0):
        return False
    else:
        return True

def findUser(users, firstName, lastName):
    for user in users:
        if(user.firstName == firstName and user.lastName == lastName):
            return user
    return None