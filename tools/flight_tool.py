import os
import requests
from dotenv import load_dotenv

load_dotenv()


def search_flight(query: str):
    url = "https://api.aviationstack.com/v1/flights"

    params = {
        "access_key": os.getenv("aviation_api"),
        "limit": 7
         }

    api_result = requests.get(url=url, params=params)
    data = api_result.json()

    flights = []  # storing flight details

    if "data" in data:
        for flight in data["data"][:7]:
            flight_info = {
                "airline": flight.get("airline", {}).get("name", "Unknown"),
                "departure_airport":flight.get("departure", {}).get("airport", "Unknown"),
                "departure_time":flight.get("departure", {}).get("scheduled", "Unknown"),
                "arrival_airport":flight.get("arrival", {}).get("airport", "Unknown"),
                "arrival_time":flight.get("arrival", {}).get("scheduled", "Unknown"),
                "status":flight.get("flight_status", "Unknown")
            }

            flights.append(flight_info)

    return flights