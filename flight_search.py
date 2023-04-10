from data_manager import DataManager
import requests
from flight_data import FlightData
from datetime import datetime, timedelta

FLIGHT_SEARCH_ENDPOINT = "https://api.tequila.kiwi.com/locations/query"
FLIGHT_SEARCH_API = "ARpssl2nn8lbYz1wS1nirpjBtzGV_c8f"

API_ENDPOINT = "https://api.tequila.kiwi.com/v2/search"
API_KEY = "ARpssl2nn8lbYz1wS1nirpjBtzGV_c8f"

TOMORROW = (datetime.today().date() + timedelta(days=1))
SIX_MONTHS = (TOMORROW + timedelta(days=6*29)).strftime("%d/%m/%Y")
SEVEN_DAYS = (TOMORROW + timedelta(days=6)).strftime("%d/%m/%Y")
TWENTYEIGHT_DAYS = (TOMORROW + timedelta(days=27)).strftime("%d/%m/%Y")


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.

    def get_destination_code(self, city_name):
        query = {
            "term": city_name,
            "location_types": "city",
        }

        headers = {
            "apikey": FLIGHT_SEARCH_API
        }

        response = requests.get(url=f"{FLIGHT_SEARCH_ENDPOINT}", headers=headers, params=query)
        code = response.json()["locations"][0]["code"]
        return code

    def check_flights(self, city_code, destination_city_code, from_time, to_time):
        query = {
            "fly_from": city_code,
            "fly_to": destination_city_code,
            "dateFrom": from_time.strftime("%d/%m/%Y"),
            "dateTo": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one for city": 1,
            "max_stopovers": 0,
            "curr": "GBP",
        }
        headers = {
            "apikey": API_KEY
        }

        response = requests.get(url=API_ENDPOINT,
                                params=query,
                                headers=headers,
                                )

        try:
            data = response.json()["data"][0]
        except IndexError:
            # print(f"No flights found for {destination_city_code}")
            query["max_stopovers"] = 2
            response = requests.get(url=API_ENDPOINT, params=query, headers=headers)
            data = response.json()["data"][0]

            flight_data = FlightData(price=data["price"],
                                     origin_city=data["route"][0]["cityFrom"],
                                     origin_airport=data["route"][0]["flyFrom"],
                                     destination_city=data["route"][0]["cityTo"],
                                     destination_airport=data["route"][0]["flyTo"],
                                     out_date=data["route"][0]["local_departure"].split("T")[0],
                                     return_date=data["route"][1]["local_departure"].split("T")[0],
                                     stopovers=1,
                                     via_city=data["route"][0]["cityTo"],
                                )

            return flight_data

        else:
            flight_data = FlightData(price=data["price"],
                                     origin_city=data["route"][0]["cityFrom"],
                                     origin_airport=data["route"][0]["flyFrom"],
                                     destination_city=data["route"][0]["cityTo"],
                                     destination_airport =data["route"][0]["flyTo"],
                                     out_date = data["route"][0]["local_departure"].split("T")[0],
                                     return_date = data["route"][1]["local_departure"].split("T")[0],
                                    )

            return flight_data
