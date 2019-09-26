from django.db import models
from django.contrib.auth.models import User

from .zomato import ZomatoAPI
api = ZomatoAPI()


RATING_CHOICES = (
    (1, "POOR"),
    (2, "AVERAGE"),
    (3, "GOOD"),
    (4, "VERY GOOD"),
    (5, "EXCELLENT"),
)


class Restaurant(models.Model):
    zomato_rest_id = models.IntegerField(unique=True, null=False)

    @property
    def name(self):
        return api.get_restaurant(self.zomato_rest_id).get("name")

    @property
    def url(self):
        return api.get_restaurant(self.zomato_rest_id).get("url")

    @property
    def avg_cost_for_two(self):
        return api.get_restaurant(self.zomato_rest_id).get("avg_cost_for_two")

    @property
    def thumb(self):
        return api.get_restaurant(self.zomato_rest_id).get("thumb")

    @property
    def cuisines(self):
        return api.get_restaurant(self.zomato_rest_id).get("cuisines")

    @property
    def user_rating(self):
        return api.get_restaurant(self.zomato_rest_id).get("user_rating")


class Review(models.Model):
    rating = models.IntegerField(choices=RATING_CHOICES, default=3)
    description = models.TextField(blank=True, null=True)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["restaurant", "user"]
