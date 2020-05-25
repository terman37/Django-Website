from django.urls import path
from . import views

urlpatterns = [
    path('summary/', views.summary, name='summary'),
    path('details/', views.details, name='details'),
    path('details_modal/', views.details_modal, name='details_modal'),
    path('importofx/', views.importofx, name='importofx'),
    path('', views.summary, name='summary'),
]