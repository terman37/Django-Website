from django.urls import path
from . import views

urlpatterns = [
    path('summary/', views.summary, name='summary'),
    path('details/', views.details, name='details'),
    path('details/modal/', views.details_modal, name='details_modal'),
    path('details/modal/save/', views.details_modal_save, name='details_modal_save'),
    path('importofx/', views.importofx, name='importofx'),
    path('', views.summary, name='summary'),
]