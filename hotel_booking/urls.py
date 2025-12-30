from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('hotel.urls')),
    path('pages/', include('hotel_pages.urls')),
]