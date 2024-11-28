import requests

class NetworkHelper:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_list(self):
        response = requests.get(f"{self.base_url}api/tours/")
        return response.json()


    def delete_item(self, item_id):
        requests.delete(f"{self.base_url}api/delete_tour/{item_id}/")






    def get_avg_tour_price(self):
        response = requests.get(f"{self.base_url}api/avg_tour_price/")
        return response.json()

    def get_tours_by_country(self):
        response = requests.get(f"{self.base_url}api/tours_by_country/")
        return response.json()

    def get_tours_per_month_by_country(self, country):
        response = requests.get(f"{self.base_url}api/tours_per_month_by_country/{country}/")
        return response.json()

    def get_tours_summary(self):
        response = requests.get(f"{self.base_url}api/tours_summary/")
        return response.json()

    def get_tours_with_conditions(self, avg_price_more_than, total_tours_more_than):
        response = requests.get(f"{self.base_url}api/tours_with_conditions/{avg_price_more_than}/{total_tours_more_than}/")
        return response.json()

    def get_transport_data(self):
        response = requests.get(f"{self.base_url}api/transport_data/")
        return response.json()

    def get_countries(self):
        response = requests.get(f"{self.base_url}api/countries/")
        return response.json()