from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),  # <== api/ prefix added here
    path('api/', include('businessdetails.urls')),
    path('api/', include('clients.urls')),
]
