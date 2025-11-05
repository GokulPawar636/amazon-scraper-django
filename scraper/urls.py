from django.urls import path
from .views import scrape_view

urlpatterns = [
    path('', scrape_view, name='scrape'),
]
