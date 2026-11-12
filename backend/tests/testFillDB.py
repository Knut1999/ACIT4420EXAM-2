from database.offers.offersFill_db import offersFill_db
from database.errors.ErrorDatabase import ErrorDatabase
from database.booking.BookingDatabase import BookingDatabase
BookingDatabase.emptyBookingsDB()
ErrorDatabase.emptyErrorMessageDB()
offersFill_db()