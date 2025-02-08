import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from data_manager import DataManager
from flight_data import FlightData
from flight_search import FlightSearch
from notification_manager import NotificationManager
from datetime import datetime, timedelta
import logging
import time

# Setup logging to debug API requests
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def update_date_range(start_date):
    departure = datetime.strptime(start_date, "%Y-%m-%d")
    range_end = departure + timedelta(days=25)
    return (
        datetime.strftime(departure, "%Y-%m-%d"),
        datetime.strftime(range_end, "%Y-%m-%d")
    )

def validate_input(start_date, stay_duration, search_months):
    try:
        # Validate start_date format
        datetime.strptime(start_date, "%Y-%m-%d")

        # Validate stay_duration (e.g., "2,14")
        if "," not in stay_duration or not all(i.isdigit() for i in stay_duration.split(",")):
            raise ValueError("Invalid stay duration. Format must be '2,14'.")

        # Validate search_months is an integer and within range
        if not (1 <= int(search_months) <= 6):
            raise ValueError("Search months must be between 1 and 6.")

        return True
    except ValueError as e:
        messagebox.showerror("Input Error", f"Invalid input: {e}")
        return False

def search_flights():
    start_date = entry_start_date.get()
    stay_duration = entry_stay_duration.get()
    search_months = entry_search_months.get()

    if not validate_input(start_date, stay_duration, search_months):
        return

    flight_search = FlightSearch()
    data_manager = DataManager()
    flight_data = FlightData()
    notification = NotificationManager()

    try:
        # Fetch bearer token once and reuse
        flight_search.get_bearer_token()

        # Load Google Sheet data
        sheet_data = data_manager.get_sheety()
        logging.info("Sheet data loaded successfully")

        # Update IATA codes if missing
        cities_without_code = [
            row["city"] for row in sheet_data["prices"]
            if row["iataCode"] == ""
        ]
        if cities_without_code:
            for i, city in enumerate(cities_without_code):
                iata_code = flight_search.get_iatacode(city)
                sheet_data["prices"][i]["iataCode"] = iata_code
            data_manager.put_sheety(sheet_data)
            logging.info("IATA codes updated")

        best_prices = {"flights": []}

        for destination in sheet_data["prices"]:
            current_date = start_date
            for _ in range(int(search_months)):
                departure_date, end_date = update_date_range(current_date)

                # Debugging log for API parameters
                api_query = f"origin=LON, destination={destination['iataCode']}, "
                api_query += f"departure={departure_date},{end_date}, duration={stay_duration}, max_price=1000"
                logging.debug(f"Searching flights: {api_query}")

                try:
                    search_results = flight_search.search_flight(
                        origin="LON",
                        destination=destination["iataCode"],
                        departure=f"{departure_date},{end_date}",
                        duration=stay_duration,
                        max_price=1000
                    )
                    if search_results and "data" in search_results and search_results["data"]:
                        flight_data.sort_data(search_results)
                    else:
                        logging.warning(f"No valid flight data returned for destination {destination['iataCode']}.")

                except Exception as api_error:
                    logging.error(f"Error searching flights for destination {destination['iataCode']}: {api_error}")

                # Delay to avoid rate-limiting
                time.sleep(1)

                current_date = end_date

            best_flight = flight_data.sort_sorted_data()
            if best_flight:
                best_prices["flights"].append(best_flight)
            flight_data.best_prices["flights"] = []

        if best_prices["flights"]:
            better_deals = flight_data.is_flight_cheaper(sheet_data, best_prices)
            if better_deals:
                notification.send_message(better_deals)
                messagebox.showinfo("Success", "Notifications sent for better deals!")
            else:
                messagebox.showinfo("Info", "No better deals found.")
        else:
            messagebox.showinfo("Info", "No flights found for the given criteria.")

    except Exception as e:
        logging.error(f"Error during flight search: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

# Initialize Tkinter window
root = tk.Tk()
root.title("Flight Deals Finder")
root.geometry("500x400")
root.configure(bg="#f0f8ff")

# Add header label
header = tk.Label(root, text="Flight Deals Finder", font=("Helvetica", 16, "bold"), bg="#f0f8ff", fg="#333")
header.pack(pady=10)

# Labels and Entry Fields
frame = tk.Frame(root, bg="#f0f8ff")
frame.pack(pady=10)

start_date_label = tk.Label(frame, text="Start Date (YYYY-MM-DD):", font=("Helvetica", 12), bg="#f0f8ff")
start_date_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
entry_start_date = ttk.Entry(frame, width=20)
entry_start_date.grid(row=0, column=1, pady=5)

stay_duration_label = tk.Label(frame, text="Trip Duration Range (e.g., 2,14):", font=("Helvetica", 12), bg="#f0f8ff")
stay_duration_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_stay_duration = ttk.Entry(frame, width=20)
entry_stay_duration.grid(row=1, column=1, pady=5)

search_months_label = tk.Label(frame, text="Months to Search Ahead (1-6):", font=("Helvetica", 12), bg="#f0f8ff")
search_months_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
entry_search_months = ttk.Entry(frame, width=20)
entry_search_months.grid(row=2, column=1, pady=5)

# Search Button
btn_search = ttk.Button(root, text="Search Flights", command=search_flights)
btn_search.pack(pady=20)

# Run Tkinter main loop
root.mainloop()