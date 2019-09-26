from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView

from search.models import Restaurant, Review
from .zomato import ZomatoAPI


class SearchView(View):

    def get(self, request):
        api = ZomatoAPI()
        search_results = api.search(
            q=request.GET.get("q"),
            cuisines=",".join(request.GET.getlist("cuisine")),
            category=",".join(request.GET.getlist("category")),
            establishment_type=",".join(
                request.GET.getlist("establishment_type"))
        )

        # Create restaurants from the search results if not already created
        for restaurant in search_results:
            obj, created = Restaurant.objects.get_or_create(
                zomato_rest_id=restaurant["id"])
            restaurant["local_rest_id"] = obj.id

        context = {}
        context["cuisines"] = api.get_cuisines()
        context["categories"] = api.get_categories()
        context["establishments"] = api.get_establishments()
        context["search_results"] = search_results
        return render(request, "search/results.html", context)


class RestaurantDetailView(DetailView):
    model = Restaurant
    context_object_name = "restaurant"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs['pk'])
        context["reviews"] = restaurant.reviews.all()
        context["reviewers"] = restaurant.reviews.all().values_list(
            'user', flat=True)
        return context


class ReviewCreateView(CreateView):
    model = Review
    template_name = "search/add_review.html"
    fields = ['rating', 'description']

    def form_valid(self, form):
        user = self.request.user
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs["res_id"])
        form.instance.user = user
        form.instance.restaurant = restaurant
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'search:restaurant-detail', kwargs={"pk": self.kwargs["res_id"]})


class ReviewUpdateView(UpdateView):
    model = Review
    fields = ['rating', 'description']

    def get_success_url(self):
        return reverse(
            'search:restaurant-detail', kwargs={"pk": self.kwargs["res_id"]})
