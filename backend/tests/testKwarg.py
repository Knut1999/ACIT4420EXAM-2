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

    return info

print(create_valid_offer(id=2))