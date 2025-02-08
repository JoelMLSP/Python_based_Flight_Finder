# Flight Deals Finder

## Overview
Flight Deals Finder is a Python-based CLI tool that searches for flight deals using the Amadeus API and compares them with stored price data to find the best offers. If a cheaper flight is found, a notification is sent via Twilio.

## Features
- Search for flights based on origin, destination, departure date range, and duration.
- Retrieve and update flight pricing information from a Google Sheet.
- Compare new flight prices with stored data.
- Send WhatsApp notifications when a cheaper flight is found.

## Technologies Used
- **Python 3**
- **Amadeus API** (for flight data)
- **Google Sheets API** (for stored pricing data)
- **Twilio API** (for sending notifications)
- **dotenv** (for managing environment variables)

## Installation & Setup
### Prerequisites
Ensure you have Python 3 installed on your system.

### Clone the Repository
```bash
git clone https://github.com/yourusername/flight-deals-finder.git
cd flight-deals-finder
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file in the root directory and add the following:
```
sheety_bearer_token=your_token
sheety_endpoint=your_sheety_endpoint
amadeus_API_KEY=your_amadeus_api_key
amadeus_API_SECRET=your_amadeus_api_secret
account_sid=your_twilio_account_sid
auth_token=your_twilio_auth_token
```

### Running the Program
To start the flight deal finder, run:
```bash
python flight_ui.py
```

## Usage Guide
1. Enter your trip details (start date, duration, months to search ahead).
2. The program will search for the best available deals.
3. If a better price is found, you will receive a WhatsApp notification.

## Screenshots
previus interaction via console ->
![Screenshot_1](https://github.com/user-attachments/assets/7b4c7b20-5f7c-4078-9e3b-00ee12543959)

new UI -> 

![image](https://github.com/user-attachments/assets/63e16ed6-c18a-428c-8a58-abcb3d186084)


![IMG_9729](https://github.com/user-attachments/assets/76ec0a63-9b8a-47d4-b4ad-be7d904620b6)


## Contributing
Feel free to submit pull requests to improve functionality or fix issues. I always appricate help :)

## License
MIT License

