from django.urls import path
from .views import health, count

urlpatterns = [
    path('health/', health, name='Health'),
    path('count/', count, name='Count'),
]
