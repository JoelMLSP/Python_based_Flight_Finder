import requests
import os
from dotenv import load_dotenv

load_dotenv()


class FlightSearch:
    """Handles all interactions with the Amadeus Flight Search API."""

    BASE_URL = "https://test.api.amadeus.com"

    def __init__(self):
        self.api_key = os.environ["amadeus_API_KEY"]
        self.api_secret = os.environ["amadeus_API_SECRET"]
        self.bearer_token = None

    def get_bearer_token(self):

        token_url = f"{self.BASE_URL}/v1/security/oauth2/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret,
        }
        response = requests.post(
            url=token_url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=data
        )
        self.bearer_token = response.json()["access_token"]

    def search_flight(self, origin, destination, departure, duration, max_price):
        """
        Searches for flights matching given criteria.

        Args:
            origin (str): Departure city IATA code
            destination (str): Arrival city IATA code
            departure (str): Departure date range (YYYY-MM-DD,YYYY-MM-DD)
            duration (str): Trip duration range (e.g., "2,14")
            max_price (int): Maximum price limit

        Returns:
            dict: Flight search results or None if no matches found
        """
        self.get_bearer_token()
        headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            'accept': 'application/vnd.amadeus+json'
        }
        params = {
            "origin": origin,
            "destination": destination,
            "departureDate": departure,
            "oneWay": "false",
            "duration": duration,
            "nonStop": "false",
            "maxPrice": max_price,
            "viewBy": "DATE"
        }

        try:
            response = requests.get(
                url=f'{self.BASE_URL}/v1/shopping/flight-dates',
                headers=headers,
                params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error searching flights: {e}")
            return None

    def get_iatacode(self, city):
        """
        Retrieves IATA code for a given city name.

        Args:
            city (str): City name to look up

        Returns:
            str: IATA code for the city
        """
        self.get_bearer_token()
        headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            'accept': 'application/vnd.amadeus+json'
        }
        params = {
            "keyword": city.strip(),
            "max": 1
        }

        response = requests.get(
            url=f'{self.BASE_URL}/v1/reference-data/locations/cities',
            headers=headers,
            params=params
        )
        response.raise_for_status()
        return response.json()["data"][0]["iataCode"]