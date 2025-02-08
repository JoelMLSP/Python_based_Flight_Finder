import requests
import os
from dotenv import load_dotenv

load_dotenv()


class DataManager:
    """Handles all interactions with the Google Sheet via Sheety API."""

    def __init__(self):
        self.base_url = os.environ["sheety_endpoint"]
        self.bearer_token = os.environ["sheety_bearer_token"]
        self.headers = {
            "Authorization": f"Bearer {self.bearer_token}"
        }

    def get_sheety(self):
        """
        Gets all price data from the sheet.
        Returns:
            dict: Data from sheet with format {"prices": [{city, iataCode, lowestPrice, id}, ...]}
        """
        response = requests.get(self.base_url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def put_sheety(self, data):
        """
        Updates existing rows in the sheet.
        Args:
            data (dict): Full sheet data including all rows to update
        """
        for row in data["prices"]:
            row_data = {
                "price": {
                    'city': row["city"],
                    'iataCode': row["iataCode"],
                    'lowestPrice': row["lowestPrice"],
                }
            }
            row_id = row["id"]
            response = requests.put(
                url=f"{self.base_url}/{row_id}",
                json=row_data,
                headers=self.headers
            )
            response.raise_for_status()