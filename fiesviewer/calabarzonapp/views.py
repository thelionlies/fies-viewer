from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max
from django.contrib import messages
from .models import Household, Province
from .forms import HouseholdFilterForm, HouseholdAddForm

def index(request):
    return render(request, 'calabarzonapp/base_template.html')

def listhouseholds(request):
    householdlist = Household.objects.all()
    context = {
        'householdlist': householdlist
    }
    return render(request, 'calabarzonapp/household_list.html', context)

def household_detail(request, pk):
    household = get_object_or_404(Household, pk=pk)
    context = {
        'household': household
    }
    return render(request, 'calabarzonapp/household_detail.html', context)

# This is for adding entries
def household_form(request):
    if request.method == 'POST':
        form = HouseholdAddForm(request.POST)
        
        if form.is_valid():
            household = form.save(commit=False)
            
            # This block is para makakuha ug next SEQ_NO according to max existing SEQ_NO
            max_seq = Household.objects.aggregate(Max('SEQ_NO'))['SEQ_NO__max'] or 0
            next_seq = max_seq + 1

            while Household.objects.filter(SEQ_NO=next_seq).exists():
                next_seq += 1
                
            household.SEQ_NO = next_seq # cant figure out how to auto increment
            household.save()
            
            return redirect('household-list')
    else:
        form = HouseholdAddForm()

    return render(request, 'calabarzonapp/household_form.html', {'form': form})

# For editing existing entries
def household_edit(request, pk):
    household = get_object_or_404(Household, pk=pk)
    
    if request.method == "GET":
        form = HouseholdAddForm(instance=household)
        context = {"form": form, "household": household}
        return render(request, "calabarzonapp/household_form.html", context)
    
    elif request.method == "POST":
        form = HouseholdAddForm(request.POST, instance=household)
        
        if form.is_valid():
            form.save()
            messages.success(request, f"Household #{household.SEQ_NO} has been updated successfully!")
            return redirect('household-detail', pk=household.pk)

        else:
            context = {"form": form, "household": household}
            return render(request, "calabarzonapp/household_form.html", context)

# This is for deleting
def household_delete(request, pk):
    household = get_object_or_404(Household, pk=pk)

    if request.method == "GET":
        context = {"household": household}
        return render(request, "calabarzonapp/household_delete.html", context)
    
    elif request.method == "POST":
        household.delete()
        return redirect("household-list")


def household_search(request):
    form = HouseholdFilterForm()
    max_income = Household.objects.aggregate(Max('TOINC'))['TOINC__max'] or 0
    max_expenditure = Household.objects.aggregate(Max('TOTEX'))['TOTEX__max'] or 0

    return render(request, "calabarzonapp/household_search.html", {
        "form": form,
        "max_income": max_income,
        "max_expenditure": max_expenditure,
    })

def household_filtered(request):
    form = HouseholdFilterForm(request.GET or None)

    max_income = Household.objects.aggregate(Max('TOINC'))['TOINC__max'] or 0
    max_expenditure = Household.objects.aggregate(Max('TOTEX'))['TOTEX__max'] or 0

    households = Household.objects.all()

    if form.is_valid():
        provinces = form.cleaned_data.get('provinces')
        area_type = form.cleaned_data.get('area_type')
        income_min = max(form.cleaned_data.get('income_min') or 0, 0)
        income_max = form.cleaned_data.get('income_max')  # can be None
        exp_min = max(form.cleaned_data.get('exp_min') or 0, 0)
        exp_max = form.cleaned_data.get('exp_max')  # can be None

        if provinces:
            households = households.filter(province__in=provinces)
        if area_type:
            households = households.filter(URB=area_type)

        # Apply min filters
        households = households.filter(TOINC__gte=income_min)
        households = households.filter(TOTEX__gte=exp_min)

        # Apply max filters only if they are set
        if income_max is not None:
            households = households.filter(TOINC__lte=income_max)
        if exp_max is not None:
            households = households.filter(TOTEX__lte=exp_max)

    context = {
        'form': form,
        'households': households,
        'max_income': max_income,
        'max_expenditure': max_expenditure,
    }
    return render(request, 'calabarzonapp/household_filtered.html', context)

def province_level(request):
    return render(request, 'calabarzonapp/province_level.html')
