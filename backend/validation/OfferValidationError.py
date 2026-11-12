class OfferValidationError(Exception):
        """This is the superclass"""
        pass

class InvalidDestinationError(OfferValidationError):
    pass

class InvalidDateError(OfferValidationError):
    pass

class InvalidTimeError(OfferValidationError):
    pass

class InvalidPriceOrDurationError(OfferValidationError):
    pass

class InvalidRatingError(OfferValidationError):
    pass

class InvalidIntegerError(OfferValidationError):
    pass