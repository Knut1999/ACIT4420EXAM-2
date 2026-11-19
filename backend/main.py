from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app_logging.logging import Log
from database.offers.offersDatabase import OfferDatabase
from booking.BookingController import BookingController
from offer.OfferController import OfferController
from database.offers.offersFill_db import offersFill_db
from database.errors.ErrorDatabase import ErrorDatabase
from database.booking.BookingDatabase import BookingDatabase


app = FastAPI()
offerController = OfferController()

origins = [
    "https://acit4420exam-2-frontend.vercel.app",
    "http://localhost:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)

@app.get("/getDB")
def read_root():
    return OfferDatabase.getEveryLineInDb()

@app.post("/newDatabase")
def read_root():
    #when we fill our new db, we also want to delete the content of our error db
    ErrorDatabase.emptyErrorMessageDB()
    #same with bookings
    BookingDatabase.emptyBookingsDB()

    offersFill_db()
    return {"message": "Database generated successfully"}



class Item(BaseModel):
    destination: str
    budgetSum: float
    preferredDepartureTime: str
    weights: list[float]
@app.post("/search/")
async def create_item(item: Item):
    offers = offerController.websiteInputs(item.destination,item.budgetSum, item.preferredDepartureTime, item.weights)
    result = []
    for offer in offers:
        result.append(offer.__dict__)

    return result

@app.get("/explaneWinner/")
def read_root():
    return offerController.offerRanker.explaneWinner()

bookingController = BookingController()
class Booking(BaseModel):
    id: int
    firstName: str
    lastName: str
@app.post("/booking/")
async def book_item(booking: Booking):
    bookingRef = bookingController.bookingInputs(booking.id, booking.firstName, booking.lastName)
    
    return bookingRef

@app.get("/getBookings")
def read_root(firstName, lastName):
    return bookingController.getAllBookings(firstName, lastName)



class Booking(BaseModel):
    offerId: int
    firstName: str
    lastName: str
@app.post("/unBook/")
async def book_item(booking: Booking):
    bookingController.cancelBooking(booking.offerId, booking.firstName, booking.lastName)
    return 

@app.get("/getLog")
def read_root():
    return Log.getLog()

@app.delete("/deleteLog")
def read_root():
    Log.emptyLogDb()
    return {"message": "Log deleted"}

@app.delete("/deleteBookings")
def read_root():
    BookingDatabase.emptyBookingsDB()
    return {"message": "Log deleted"}

@app.get("/getAllErrors")
def read_root():
    return ErrorDatabase.getAllErrors()

@app.delete("/deleteErrors")
def read_root():
    return ErrorDatabase.emptyErrorMessageDB()