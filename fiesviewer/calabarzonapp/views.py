from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max, Count, Avg, Sum, Min
from django.contrib import messages
from .models import Household, Province
from .forms import HouseholdFilterForm, HouseholdAddForm
from django.core.paginator import Paginator

def index(request):
    return render(request, 'calabarzonapp/base_template.html')

def listhouseholds(request):
    all_households = Household.objects.all().order_by('SEQ_NO')
    paginator = Paginator(all_households, 20)  # 20 households per page

    page_number = request.GET.get('page')  # Get ?page=1, ?page=2, etc.
    page_obj = paginator.get_page(page_number)

    return render(request, 'calabarzonapp/household_list.html', {'page_obj': page_obj})


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

def province_level(request, province_id=None):
    all_provinces = Province.objects.all().order_by('name')

    if province_id is None:
        current_province = all_provinces.first()
    else:
        current_province = get_object_or_404(Province, id=province_id)

    # Get the index of current province
    province_list = list(all_provinces)
    current_index = province_list.index(current_province)
    
    # Determine previous and next provinces
    previous_province = province_list[current_index - 1] if current_index > 0 else None
    next_province = province_list[current_index + 1] if current_index < len(province_list) - 1 else None
    
    # Some aggregates
    province_households = Household.objects.filter(province=current_province)
    urban_households = province_households.filter(URB=1).count()
    rural_households = province_households.filter(URB=2).count()
    total_households = province_households.count()
    avg_income = province_households.aggregate(Avg('TOINC'))['TOINC__avg'] or 0
    avg_expenditure = province_households.aggregate(Avg('TOTEX'))['TOTEX__avg'] or 0
    avg_food = province_households.aggregate(Avg('FOOD'))['FOOD__avg'] or 0
    avg_cloth = province_households.aggregate(Avg('CLOTH'))['CLOTH__avg'] or 0
    avg_health = province_households.aggregate(Avg('HEALTH'))['HEALTH__avg'] or 0
    avg_transport = province_households.aggregate(Avg('TRANSPORT'))['TRANSPORT__avg'] or 0
    avg_communication = province_households.aggregate(Avg('COMMUNICATION'))['COMMUNICATION__avg'] or 0
    avg_recreation = province_households.aggregate(Avg('RECREATION'))['RECREATION__avg'] or 0
    avg_education = province_households.aggregate(Avg('EDUCATION'))['EDUCATION__avg'] or 0
    avg_fsize = province_households.aggregate(Avg('FSIZE'))['FSIZE__avg'] or 1  # to avoid division by zero
    avg_pcp = province_households.aggregate(Avg('PERCAPITA'))['PERCAPITA__avg'] or 0

    # For viz
    categories = ['Food', 'Clothing', 'Health', 'Transport', 'Communication', 'Recreation', 'Education']
    expenditure_values = [
        round(avg_food, 2),
        round(avg_cloth, 2),
        round(avg_health, 2),
        round(avg_transport, 2),
        round(avg_communication, 2),
        round(avg_recreation, 2),
        round(avg_education, 2)
    ]

    context = {
        'current_province': current_province,
        'all_provinces': all_provinces,
        'previous_province': previous_province,
        'next_province': next_province,
        'urban_households': urban_households,
        'rural_households': rural_households,
        'total_households': total_households,
        'avg_fsize': round(avg_fsize, 2),
        'avg_income': round(avg_income, 2),
        'avg_expenditure': round(avg_expenditure, 2),
        'avg_pcp': round(avg_pcp, 2),
        'categories': categories,
        'expenditure_values': expenditure_values,
    }
    
    return render(request, 'calabarzonapp/province_level.html', context)