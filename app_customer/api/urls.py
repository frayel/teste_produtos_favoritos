from django.urls import path

from api.views.customer import CustomerView
from api.views.customer_detail import CustomerDetailView
from api.views.favorite import FavoriteView

urlpatterns = [
    path("customer/", CustomerView.as_view(), name="customer"),
    path("customer/<str:customer_id>/", CustomerDetailView.as_view(), name="customer_detail"),
    path("customer/<str:customer_id>/favorite/", FavoriteView.as_view(), name="favorite"),
]

