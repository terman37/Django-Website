from django.urls import path
from . import views

urlpatterns = [
    path('summary/', views.summary, name='summary'),
    path('details/', views.details, name='details'),
    path('importofx/', views.importofx, name='importofx'),
    path('', views.summary, name='summary'),
]