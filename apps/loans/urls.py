from django.urls import path
from apps.loans.views import loans

urlpatterns = [
    path('', loans, name='loans'),
]
