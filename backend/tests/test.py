from offer.OfferController import OfferController
controller = OfferController()
weights = [0.1667,0.1667,0.1667,0.1667,0.1667,0.1667,0.342]
offers = controller.websiteInputs("Cadiz", "Budget traveller", 42.0, "12:50", weights)
result = []
for offer in offers:
    result.append(offer.__dict__)

for res in result:
    print(res)

# {
#   "destination": "Cadiz",
#   "budgetType": "Budget traveller",
#   "budgetSum": 50.0,
#   "preferredDepartureTime": "12:50",
#   "weights": [
#     0.1667,0.1667,0.1667,0.1667,0.1667,0.1667,0.342
#   ]
# }