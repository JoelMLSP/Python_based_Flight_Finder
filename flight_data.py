class FlightData:


    def __init__(self):
        self.current_search_data = {}
        self.best_prices = {"flights": []}

    def sort_data(self, data):

        if not data["data"]:
            return

        cheapest_flight = data["data"][0]
        lowest_price = float(cheapest_flight["price"]["total"])

        # Find cheapest flight in current search
        for flight in data["data"]:
            current_price = float(flight["price"]["total"])
            if current_price < lowest_price:
                lowest_price = current_price
                cheapest_flight = flight

        self.best_prices["flights"].append(cheapest_flight)

    def sort_sorted_data(self):

        if not self.best_prices["flights"]:
            print("No flights found.")
            return None

        cheapest_flight = None
        lowest_price = float('inf')

        for flight in self.best_prices["flights"]:
            if "price" in flight and "total" in flight["price"]:
                current_price = float(flight["price"]["total"])
                if current_price < lowest_price:
                    lowest_price = current_price
                    cheapest_flight = flight

        return cheapest_flight

    def is_flight_cheaper(self, sheet_data, new_prices):

        found_better_price = False

        for i, row in enumerate(sheet_data["prices"]):
            new_price = float(new_prices["flights"][i]["price"]["total"])
            if float(row["lowestPrice"]) > new_price:
                row["lowestPrice"] = new_price
                found_better_price = True

        if not found_better_price:
            print("No better prices found")
            return None

        return sheet_data