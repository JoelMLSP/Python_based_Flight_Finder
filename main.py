from datetime import datetime, timedelta
import time
from dotenv import load_dotenv #make sure that pip install python-dotenv has been run in terminal to install package
from data_manager import DataManager
from flight_data import FlightData
from flight_search import FlightSearch
from notification_manager import NotificationManager

load_dotenv()


def update_date_range(start_date):
    """Calculate the date range for flight search."""
    departure = datetime.strptime(start_date, "%Y-%m-%d")
    range_end = departure + timedelta(days=25)
    return (
        datetime.strftime(departure, "%Y-%m-%d"),
        datetime.strftime(range_end, "%Y-%m-%d")
    )


def main():

    flight_search = FlightSearch()
    data_manager = DataManager()
    flight_data = FlightData()
    notification = NotificationManager()


    sheet_data = data_manager.get_sheety()
    print("Sheet data loaded successfully")


    cities_without_code = [
        row["city"] for row in sheet_data["prices"]
        if row["iataCode"] == ""
    ]

    if cities_without_code:
        for i, city in enumerate(cities_without_code):
            iata_code = flight_search.get_iatacode(city)
            sheet_data["prices"][i]["iataCode"] = iata_code
        data_manager.put_sheety(sheet_data)
        print("IATA codes updated")

    # Get search parameters
    print("\nEnter dates in YYYY-MM-DD format")
    start_date = input("Enter start date (e.g., 2025-02-01): ")
    stay_duration = input("Enter trip duration range (e.g., 2,14): ")
    search_months = int(input("Enter the months ahead you want to search (1-6): "))

    print (start_date)


    best_prices = {"flights": []}


    for destination in sheet_data["prices"]:
        print(f"\nSearching flights to {destination['city']}...")
        current_date = start_date

        # Search across multiple months
        for _ in range(search_months):
            time.sleep(5)  # slå inte i taket på APIn

            departure_date, end_date = update_date_range(current_date)

            try:
                search_results = flight_search.search_flight(
                    origin="LON",
                    destination=destination["iataCode"],
                    departure=f"{departure_date},{end_date}",
                    duration=stay_duration,
                    max_price=1000
                )

                if search_results:
                    flight_data.sort_data(search_results)

            except Exception as e:
                print(f"Error during search: {e}")
                continue

            current_date = end_date

        best_flight = flight_data.sort_sorted_data()
        if best_flight:
            best_prices["flights"].append(best_flight)
        flight_data.best_prices["flights"] = []

    # Compare prices and send notifications will probably figure out a better way for this in the future
    better_deals = flight_data.is_flight_cheaper(sheet_data, best_prices)
    if better_deals:
        notification.send_message(better_deals)
        print("Notifications has been sent for better deals!")


if __name__ == "__main__":
    main()