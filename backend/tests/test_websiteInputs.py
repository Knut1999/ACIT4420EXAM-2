from offer.OfferController import OfferController
#make sure offer db is not empty
def test_websiteInputs():
    controller = OfferController()
    weights = [0.1667, 0.1667, 0.1667, 0.1667, 0.1667, 0.1667, 0.342]

    offers = controller.websiteInputs("Cadiz", 42.0, "12:50", weights)

    assert isinstance(offers, list)
    assert len(offers) >= 5

    for offer in offers:
        assert offer.destination == "Cadiz"
        assert offer.price <= 42.0
        assert offer.score is not None


def test_price_weight_prioritizes_cheapest_offer():
    controller = OfferController()
    weights = [1, 0, 0, 0, 0, 0, 0]

    offers = controller.websiteInputs("Cadiz", 200, "12:50", weights)

    cheapestPrice = offers[0].price

    for offer in offers:
        if offer.price < cheapestPrice:
            cheapestPrice = offer.price

    assert offers[0].price == cheapestPrice


def test_duration_weight_prioritizes_shortest_offer():
    controller = OfferController()
    weights = [0, 1, 0, 0, 0, 0, 0]

    offers = controller.websiteInputs("Cadiz", 200, "12:50", weights)

    shortestDuration = offers[0].duration

    for offer in offers:
        if offer.duration < shortestDuration:
            shortestDuration = offer.duration

    assert offers[0].duration == shortestDuration


def test_rating_weight_prioritizes_highest_rating():
    controller = OfferController()
    weights = [0, 0, 0, 0, 1, 0, 0]

    offers = controller.websiteInputs("Cadiz", 200, "12:50", weights)

    highestRating = offers[0].customerRating

    for offer in offers:
        if offer.customerRating > highestRating:
            highestRating = offer.customerRating

    assert offers[0].customerRating == highestRating
