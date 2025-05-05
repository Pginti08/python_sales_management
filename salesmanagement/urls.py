from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),  # <== api/ prefix added here
    path('api/', include('businessdetails.urls')),
    path('api/', include('clients.urls')),
    path('api/', include('common_country_module.urls')),
    path('api/', include('bankdetails.urls')),
    path('api/', include('invoice.urls')),
    path('api/', include('projects.urls')),
    path('api/', include('count.urls')),

]
