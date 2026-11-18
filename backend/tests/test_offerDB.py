##NB! thise test will change the DB!

from database.offers.offersDatabase import OfferDatabase
from database.offers.offersFill_db import offersFill_db


def test_empty_bookings_db():
    OfferDatabase.emptyOffersDB()
    bookings = OfferDatabase.getEveryLineInDb()
    assert bookings == []

def test_fill_offers_db():
    offersFill_db()
    offers = OfferDatabase.getEveryLineInDb()
    assert len(offers) > 200 and len(offers) < 300


def test_get_every_line_in_db():
    routes = OfferDatabase.getEveryLineInDb()
    assert isinstance(routes, list)
    assert len(routes) > 200


def test_get_companies():
    companies = OfferDatabase.getCompanies()
    assert isinstance(companies, set)
    assert len(companies) > 4


def test_get_line_from_id():
    routes = OfferDatabase.getEveryLineInDb()
    offer_id = routes[0][0]
    result = OfferDatabase.getLineFromId(offer_id)
    assert len(result) == 1
    assert result[0][0] == offer_id


def test_empty_offers_db():
    OfferDatabase.emptyOffersDB()
    offers = OfferDatabase.getEveryLineInDb()
    assert offers == []

