import requests

class NetworkHelper:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_list(self):
        response = requests.get(f"{self.base_url}api/tours/")
        return response.json()


    def delete_item(self, item_id):
        requests.delete(f"{self.base_url}api/delete_tour/{item_id}/")