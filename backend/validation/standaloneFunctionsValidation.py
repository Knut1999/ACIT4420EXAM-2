from datetime import date, datetime
import re

from offer.offerClasses import Offer
from offer.standaloneFunctions import getDestinations

#our exception classes
from validation.OfferValidationError import (
    InvalidDestinationError,
    InvalidDateError,
    InvalidTimeError,
    InvalidPriceOrDurationError,
    InvalidRatingError,
    InvalidIntegerError
)

#all the functions return the error type and the specific error
def validateDestination(offer):
    if offer.destination not in getDestinations():
        raise InvalidDestinationError(
            f"Invalid destination {offer.destination}"
        )

def validateDate(offer):
    try:
        dateString = offer.travelDate
        parsedDate = datetime.strptime(dateString, "%Y-%m-%d")
        travelDate = parsedDate.date()
        # print(type(travelDate), travelDate)
        #not check if traveldate is in the past because then it heppens no 
        #dates are old because noonre refreshed database
        # if travelDate < date.today():
        #     raise InvalidDateError(
        #         "Travel date is in the past"
        #     )
    except ValueError:
        raise InvalidDateError(
            "Invalid travel date"
        )

def validateDepartureAndArrival(offer: Offer):
    for stringType, time in [("Departure",offer.departureTime), ("Arrival", offer.arrivalTime)]:
        #regex, not totally nessecarry, but makes code more compact
        if not re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", time):
            raise InvalidTimeError(
                f"Invalid {stringType} time"
            )

        

def validateNonNegativeFloat(offer:Offer):
    #both duration and price uses same function due to both beeing float above 0   
    for stringType, value in [("Duration",offer.duration), ("Price",offer.price)]:
        try:
            number = float(value)
            if number <= 0:
                raise InvalidPriceOrDurationError(f"Invalid, {stringType} cant be less or equal 0 -> : {value}")
        except ValueError:
            raise InvalidPriceOrDurationError(f"Invalid, {stringType} cant converted to float ->  value is: {value}")

def validateNonNegativeInteger(offer: Offer):
    for stringType, value in [("Luggage allowance",offer.luggageAllowance), ("Available seats",offer.availableSeats), ("Environmental measure", offer.environmentalMeasure)]:
        try:
            integer = int(value)
            if integer < 0:
                raise InvalidIntegerError(
                    f"{stringType} cant be lower than 0"
                )
        except ValueError:
            raise InvalidIntegerError(
                f"{stringType} cant converted to integer"
            )

def validateCustomerRating(offer: Offer):
    try:
        rating = float(offer.customerRating)
        if rating < 0 or rating > 5:
            raise InvalidRatingError(
                "Invalid customer rating, must be between 0 and 5"
            )
    except ValueError:
        raise InvalidRatingError(
            "Invalid customer rating, cant be converted to float"
        )