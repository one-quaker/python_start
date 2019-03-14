from django.urls import path, re_path
from .views import IndexView, TopDonationView


urlpatterns = [
    path('', IndexView.as_view(), name='index-page'),
    path('top', TopDonationView.as_view(), name='top-page'),
]
