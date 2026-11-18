import sys
from pathlib import Path
from types import SimpleNamespace


# Add the backend directory to Python path when the test is run directly.
BACKEND_PATH = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_PATH))

from offer.offerClasses import Offer, Company
import pytest

from offer.OfferRanker import OfferRanker
from validation.standaloneFunctionsValidation import validateNonNegativeInteger
from validation.OfferValidationError import InvalidIntegerError
from offer.standaloneFunctions import normalizeWeights
from validation.standaloneFunctionsValidation import (
    validateCustomerRating,
    validateDepartureAndArrival,
    validateDestination,
    validateNonNegativeFloat,
)
from validation.OfferValidationError import (
    InvalidDestinationError,
    InvalidPriceOrDurationError,
    InvalidRatingError,
    InvalidTimeError,
)



def create_valid_offer(**kwargs):
    info = [
        kwargs.get("id", 1),
        kwargs.get("companyName", "TestCompany"),
        kwargs.get("destination", "Cadiz"),
        kwargs.get("travelDate", "2026-12-01"),
        kwargs.get("departureTime", "12:00"),
        kwargs.get("duration", 3.0),
        kwargs.get("arrivalTime", "15:00"),
        kwargs.get("price", 25.0),
        kwargs.get("transfers", 0),
        kwargs.get("luggageAllowance", 20),
        kwargs.get("changeability", "FULL"),
        kwargs.get("refundability", "FULL"),
        kwargs.get("availableSeats", 5),
        kwargs.get("customerRating", 4.0),
        kwargs.get("environmentalMeasure", 50)
    ]

    return Offer(info)


def test_normalize_weights_total_one():
    input_weights = [1, 2, 3, 4, 5, 6, 7]

    normalized_weights = normalizeWeights(input_weights)

    # All normalized weights should add up to 1
    assert sum(normalized_weights) == pytest.approx(1.0)

    # The first weight should be 1/28
    expected_first_weight = 1 / 28
    assert normalized_weights[0] == pytest.approx(expected_first_weight)


def test_normalize_zero_weights_returns_equal_weights():
    result = normalizeWeights([0, 0, 0, 0, 0, 0, 0])
    assert sum(result) == pytest.approx(1.0)
    assert all(weight == pytest.approx(1 / 7) for weight in result)


def test_valid_destination_is_accepted():
    validateDestination(create_valid_offer())


def test_unknown_destination_is_rejected():
    with pytest.raises(InvalidDestinationError):
        validateDestination(create_valid_offer(destination="Atlantis"))


def test_invalid_departure_time_is_rejected():
    with pytest.raises(InvalidTimeError):
        validateDepartureAndArrival(create_valid_offer(departureTime="25:70"))


def test_zero_price_is_rejected():
    with pytest.raises(InvalidPriceOrDurationError):
        validateNonNegativeFloat(create_valid_offer(price=0))


def test_rating_above_five_is_rejected():
    with pytest.raises(InvalidRatingError):
        validateCustomerRating(create_valid_offer(customerRating=5.5))


def test_offer_over_budget_is_filtered_and_cheapest_ranks_first():
    cheap = create_valid_offer(price=10)
    medium = create_valid_offer(price=20)
    expensive = create_valid_offer(price=40)

    company = Company("test")
    company.offers = [cheap, medium, expensive]

    weights = [1, 0, 0, 0, 0, 0, 0]

    ranker = OfferRanker([company], "Cadiz", "12:00", 30, weights)
    ranked = ranker.getRankedOffers()

    assert len(ranked) == 2
    assert expensive not in ranked
    assert ranked[0] is cheap
    assert ranked[1] is medium


def test_duration_above_24_is_rejected():
    with pytest.raises(InvalidPriceOrDurationError):
        validateNonNegativeFloat(create_valid_offer(duration=25))


def test_price_above_200_is_rejected():
    with pytest.raises(InvalidPriceOrDurationError):
        validateNonNegativeFloat(create_valid_offer(price=201))


def test_transfers_above_10_are_rejected():
    with pytest.raises(InvalidIntegerError):
        validateNonNegativeInteger(create_valid_offer(transfers=11))


def test_valid_arrival_time_is_accepted():
    validateDepartureAndArrival(
        create_valid_offer(arrivalTime="15:30")
    )

