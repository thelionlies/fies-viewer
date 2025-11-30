from django.urls import path
from django.http import HttpResponse
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    # localhost:8000/fiesviewer/households
    path('households/', views.listhouseholds, name='household-list'),

    # localhost:8000/fiesviewer/households/<pk>
    path('households/<int:pk>/', views.household_detail, name='household-detail'),

    # localhost:8000/fiesviewer/households/form
    path('households/form/', views.household_form, name='household-form'),

    # localhost:8000/fiesviewer/households/edit # Add pk for the OIC
    path('households/edit/', views.household_edit, name='household-edit'),

    # localhost:8000/fiesviewer/households/delete # Add pk for the OIC
    path('households/delete/', views.household_delete, name='household-delete'),

    #localhost:8000/fiesviewer/households/search
    path('households/search/', views.household_search, name='household-search'),

    #localhost:8000/fiesviewer/households/filtered
    path('households/filtered/', views.household_filtered, name='household-filtered'),

    # localhost:8000/fiesviewer/province-level
    path('province-level/', views.province_level, name='province-level'),



]