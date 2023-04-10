import requests

SHEETY_ENDPOINT = "https://api.sheety.co/b6c48f01f18939838bfc5472d1b8150c/pythonFlightDeals/prices"


class DataManager:
    # This class is responsible for talking to the Google Sheet.

    def __init__(self):
        self.destination_data = {}

    def get_data(self):
        response = requests.get(url=SHEETY_ENDPOINT)
        self.destination_data = response.json()["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"],
                }
            }
            response = requests.put(
                url=F"{SHEETY_ENDPOINT}/{city['id']}",
                json=new_data)
            print(response.text)

    def get_customer_emails(self):
        customers_endpoint = "https://api.sheety.co/b6c48f01f18939838bfc5472d1b8150c/pythonFlightDeals/users"
        response = requests.get(customers_endpoint)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data