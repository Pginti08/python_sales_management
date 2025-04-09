from django.urls import path
from .views import (
    BusinessDetailListCreateView,
    BusinessDetailRetrieveUpdateDestroyView
)

urlpatterns = [
    # This will handle GET (list) and POST (create)
    path('business/', BusinessDetailListCreateView.as_view(), name='business-list-create'),

    # This will handle GET by ID, PUT/PATCH (update), and DELETE
    path('business/<int:pk>/', BusinessDetailRetrieveUpdateDestroyView.as_view(), name='business-detail'),
]
