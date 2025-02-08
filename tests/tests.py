import pytest
from unittest.mock import patch, MagicMock
from flight_data import FlightData
from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager

# sorting of flight data
def test_sort_data():
    flight_data = FlightData()
    sample_data = {
        "data": [
            {"price": {"total": "200"}},
            {"price": {"total": "150"}},
            {"price": {"total": "250"}}
        ]
    }
    flight_data.sort_data(sample_data)
    assert flight_data.best_prices["flights"][0]["price"]["total"] == "150"

# Test searching for flights
def test_search_flight():
    flight_search = FlightSearch()
    flight_search.get_bearer_token = MagicMock(return_value=None)
    with patch("flight_search.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": [{"price": {"total": "100"}}]}
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        result = flight_search.search_flight("LON", "NYC", "2025-05-01,2025-05-10", "2,14", 1000)
        assert result["data"][0]["price"]["total"] == "100"

# Test data from Google Sheet
def test_get_sheety():
    data_manager = DataManager()
    with patch("data_manager.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"prices": [{"city": "New York", "iataCode": "NYC", "lowestPrice": "200"}]}
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        result = data_manager.get_sheety()
        assert result["prices"][0]["city"] == "New York"

# Test Twilio notification
def test_send_message():
    notification_manager = NotificationManager()
    with patch("notification_manager.Client") as mock_client:
        mock_twilio = MagicMock()
        mock_client.return_value = mock_twilio
        notification_manager.send_message({"prices": [{"city": "New York", "iataCode": "NYC", "lowestPrice": "150"}]})
        mock_twilio.messages.create.assert_called_once()

# TODO: Add more tests for data validation and error handling
