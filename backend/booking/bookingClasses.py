from database.booking.BookingDatabase import BookingDatabase

class User:
    def __init__(self, firstName:str, lastName:str):
        self.firstName = firstName
        self.lastName = lastName
        self.id = BookingDatabase.getIdFromName(firstName, lastName)