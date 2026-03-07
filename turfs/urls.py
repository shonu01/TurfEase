from django.urls import path
from . import views

urlpatterns = [
    path('', views.turf_list, name='turf_list'),
    path('<int:pk>/', views.turf_detail, name='turf_detail'),
]
