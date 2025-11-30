from django.shortcuts import render
from django.http import HttpResponse

from .models import Household, Province

# Create your views here.
def index(request):
    return render(request, 'calabarzonapp/base_template.html')

def listhouseholds(request):
    householdlist = Household.objects.all()
    context = {
        'householdlist': householdlist
    }
    return render(request, 'calabarzonapp/household_list.html', context)

def household_detail(request, pk):
    household = Household.objects.get(pk=pk)
    context = {
        'household': household
    }
    return render(request, 'calabarzonapp/household_detail.html', context)


def household_form(request):
    return render(request, 'calabarzonapp/household_form.html')

def household_edit(request):
    return render(request, 'calabarzonapp/household_form.html')

def household_delete(request):
    return render(request, 'calabarzonapp/household_delete.html')

def household_search(request):
    return render(request, 'calabarzonapp/household_search.html')

def household_filter(request):
    return render(request, 'calabarzonapp/household_filter.html')

def province_level(request):
    return render(request, 'calabarzonapp/province_level.html')