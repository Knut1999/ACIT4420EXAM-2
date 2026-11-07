from database.database import Database

class BookingController:
    def __init__(self):
        pass

    def bookingInputs(self, id:int):
        self.id = id
        self.route = Database.getLineFromId(self.id)
        self.available_seats = (self.route[0][12])
        if(self.available_seats <= 0):
            return "No seats available"
        