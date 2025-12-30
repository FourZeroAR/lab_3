from django.urls import path
from . import views

urlpatterns = [
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/create/', views.booking_edit, name='booking_create'),
    path('bookings/<int:pk>/edit/', views.booking_edit, name='booking_edit'),
    path('bookings/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('bookings/<int:pk>/delete/', views.booking_delete, name='booking_delete'),

    path('colleague/books/', views.colleague_books, name='colleague_books'),
    path('colleague/books/<int:pk>/delete/', views.colleague_book_delete, name='colleague_delete'),
    path('dashboard/v1/', views.dashboard_v1, name='dashboard_v1'),
    path('dashboard/v2/', views.dashboard_v2, name='dashboard_v2'),
    path('performance/', views.performance_test, name='performance_test'),
]