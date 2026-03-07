from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('turfs/', views.dashboard_turfs, name='dashboard_turfs'),
    path('turfs/add/', views.add_turf, name='add_turf'),
    path('turfs/edit/<int:pk>/', views.edit_turf, name='edit_turf'),
    path('turfs/delete/<int:pk>/', views.delete_turf, name='delete_turf'),
    path('bookings/', views.dashboard_bookings, name='dashboard_bookings'),
    path('bookings/export-csv/', views.export_bookings_csv, name='export_bookings_csv'),
    path('users/', views.dashboard_users, name='dashboard_users'),
    path('maintenance/', views.dashboard_maintenance, name='dashboard_maintenance'),
    path('maintenance/add/', views.add_maintenance, name='add_maintenance'),
    path('maintenance/delete/<int:pk>/', views.delete_maintenance, name='delete_maintenance'),
]
