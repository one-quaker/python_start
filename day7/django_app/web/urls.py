from django.urls import path, re_path
from .views import IndexView, TopDonationView, ApiTopList


urlpatterns = [
    path('', IndexView.as_view(), name='index-page'),
    path('top', TopDonationView.as_view(), name='top-page'),
    path('api/top', ApiTopList.as_view(), name='api-top-list'),
]
