from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database.offers.offersDatabase import OfferDatabase
from booking.BookingController import BookingController
from offer.OfferController import OfferController
from database.offers.offersFill_db import offersFill_db
from database.errors.ErrorDatabase import ErrorDatabase
from database.booking.BookingDatabase import BookingDatabase


app = FastAPI()
offerController = OfferController()

origins = [
    "https://busbidder.knutonsoyen.no",
    "https://acit4420exam-2-frontend.vercel.app",
    "http://localhost:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
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
@app.post("/items/")
async def create_item(item: Item):
    offers = offerController.websiteInputs(item.destination,item.budgetSum, item.preferredDepartureTime, item.weights)
    result = []
    for offer in offers:
        result.append(offer.__dict__)

    return result

bookingController = BookingController()
class Booking(BaseModel):
    id: int
    firstName: str
    lastName: str
@app.post("/booking/")
async def book_item(booking: Booking):
    bookingRef = bookingController.bookingInputs(booking.id, booking.firstName, booking.lastName)
    
    return bookingRef

@app.get("/getOffers")
def read_root(firstName, lastName):
    return bookingController.getAllBookings(firstName, lastName)


class Booking(BaseModel):
    offerId: int
    firstName: str
    lastName: str
@app.post("/unBook/")
async def book_item(booking: Booking):
    bookingRef = bookingController.cancelBooking(booking.offerId, booking.firstName, booking.lastName)
    return 