import requests

from django.conf import settings


class ZomatoAPI:

    def __init__(self):
        self.api_key = settings.ZOMATO_API_KEY
        self.api = "https://developers.zomato.com/api/v2.1/"

    def search(self, **kwargs):
        url = self.api + "search"
        headers = {
            "content-type": "application/json",
            "user-key": self.api_key
        }
        params = {
            "q": kwargs.get("q"),
            "entity_id": 4,
            "entity_type": "city",
            "cuisines": kwargs.get("cuisines"),
            "category": kwargs.get("category"),
            "establishment_type": kwargs.get("establishment_type"),
        }
        r = requests.get(url, headers=headers, params=params)
        results = []
        if r.status_code == 200:
            restaurants = r.json()["restaurants"]
            for restaurant in restaurants:
                results.append({
                    "id": restaurant["restaurant"]["id"],
                    "name": restaurant["restaurant"]["name"],
                    "url": restaurant["restaurant"]["url"],
                    "cuisines": restaurant["restaurant"]["cuisines"],
                    "avg_cost_for_two":
                        restaurant["restaurant"]["average_cost_for_two"],
                    "thumb": restaurant["restaurant"]["thumb"],
                    "user_rating": restaurant["restaurant"]["user_rating"]
                })
        return results

    def get_cuisines(self):
        url = self.api + "/cuisines"
        headers = {
            "content-type": "application/json",
            "user-key": self.api_key
        }
        r = requests.get(url, headers=headers, params={"city_id": 4})
        results = r.json()["cuisines"] if r.status_code == 200 else []
        return results

    def get_categories(self):
        url = self.api + "/categories"
        headers = {
            "content-type": "application/json",
            "user-key": self.api_key
        }
        r = requests.get(url, headers=headers)
        results = r.json()["categories"] if r.status_code == 200 else []
        return results

    def get_establishments(self):
        url = self.api + "/establishments"
        headers = {
            "content-type": "application/json",
            "user-key": self.api_key
        }
        r = requests.get(url, headers=headers, params={"city_id": 4})
        results = r.json()["establishments"] if r.status_code == 200 else []
        return results

    def get_restaurant(self, _id):
        url = self.api + "/restaurant"
        headers = {
            "content-type": "application/json",
            "user-key": self.api_key
        }
        r = requests.get(url, headers=headers, params={"res_id": _id})
        if r.status_code == 200:
            restaurant = r.json()
            return {
                "id": restaurant["id"],
                "name": restaurant["name"],
                "url": restaurant["url"],
                "cuisines": restaurant["cuisines"],
                "avg_cost_for_two":
                    restaurant["average_cost_for_two"],
                "thumb": restaurant["thumb"],
                "user_rating": restaurant["user_rating"]
            }
        else:
            return {}
