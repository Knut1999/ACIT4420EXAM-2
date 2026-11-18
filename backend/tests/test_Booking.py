from database.booking.BookingDatabase import BookingDatabase
from booking.BookingController import BookingController


bookingController = BookingController()

def test_bookingInputs():
    bookingController.bookingInputs(1, "Test", "User")
    bookings = BookingDatabase.getBookingsFromName("Test", "User")

    assert len(bookings) > 0


def test_cancel_booking():
    bookingController.bookingInputs(1, "Test", "User")
    bookingsBeforeCancel = BookingDatabase.getBookingsFromName("Test", "User")
    bookingController.cancelBooking(1, "Test", "User")
    bookingsAfterCancel = BookingDatabase.getBookingsFromName("Test", "User")

    assert len(bookingsAfterCancel) < len(bookingsBeforeCancel)