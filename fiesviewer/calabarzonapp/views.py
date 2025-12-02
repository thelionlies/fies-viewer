from pydoc import Helper
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max, Count, Avg, Sum, Min, F, FloatField
from django.contrib import messages
from .models import Household, Province
from .forms import HouseholdFilterForm, HouseholdAddForm
from django.core.paginator import Paginator


def index(request):
    return render(request, 'calabarzonapp/base_template.html')


def listhouseholds(request):
    all_households = Household.objects.all().order_by('SEQ_NO')
    paginator = Paginator(all_households, 20) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'calabarzonapp/household_list.html', {'page_obj': page_obj})


def household_detail(request, pk):
    household = get_object_or_404(Household, pk=pk)
    context = {
        'household': household
    }
    return render(request, 'calabarzonapp/household_detail.html', context)


def household_form(request):
    if request.method == 'POST':
        form = HouseholdAddForm(request.POST)
        
        if form.is_valid():
            household = form.save(commit=False)
            
            # Auto-increment
            max_seq = Household.objects.aggregate(Max('SEQ_NO'))['SEQ_NO__max'] or 0
            next_seq = max_seq + 1

            while Household.objects.filter(SEQ_NO=next_seq).exists():
                next_seq += 1
            
            household.SEQ_NO = next_seq
            household.save()

            total_households = Household.objects.count()
            per_page = 20
            last_page = (total_households + per_page - 1) // per_page

            return redirect(f'/fiesviewer/households/?page={last_page}')
        
        else:
            messages.error(request, "Please correct the errors below.")
            
    else:
        form = HouseholdAddForm()

    return render(request, 'calabarzonapp/household_form.html', {'form': form})


def household_edit(request, pk):
    household = get_object_or_404(Household, pk=pk)
    
    if request.method == "GET":
        form = HouseholdAddForm(instance=household)
        context = {"form": form, "household": household}
        return render(request, "calabarzonapp/household_edit_form.html", context)
    
    elif request.method == "POST":
        print(f"POST request received for household #{household.SEQ_NO}")
        print(f"POST data: {request.POST}")
        
        form = HouseholdAddForm(request.POST, instance=household)
        
        if form.is_valid():
            print("Form is VALID - Saving...")
            saved_household = form.save()
            print(f"Household saved: {saved_household.SEQ_NO}")
            messages.success(request, f"✓ Household #{household.SEQ_NO} has been successfully updated!")
            print(f"Redirecting to household-detail with pk={household.pk}")
            return redirect('household-detail', pk=household.pk)

        else:
            print("Form is NOT valid!")
            print("Form errors:", form.errors)
            print("Form data:", request.POST)
            messages.error(request, "Please correct the errors below.")
            context = {"form": form, "household": household}
            return render(request, "calabarzonapp/household_edit_form.html", context)


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
    households = Household.objects.all().order_by('SEQ_NO')

    if form.is_valid():
        # Filter by province
        provinces = form.cleaned_data.get('provinces')
        if provinces:
            households = households.filter(province__in=provinces)

        # Filter by area type
        area_type = form.cleaned_data.get('area_type')
        if area_type:
            households = households.filter(URB=area_type)

        # Filter by income
        income_min = form.cleaned_data.get('income_min')
        if income_min is not None:
            households = households.filter(TOINC__gte=income_min)
        income_max = form.cleaned_data.get('income_max')
        if income_max is not None:
            households = households.filter(TOINC__lte=income_max)

        # Filter by expenditure
        exp_min = form.cleaned_data.get('exp_min')
        if exp_min is not None:
            households = households.filter(TOTEX__gte=exp_min)
        exp_max = form.cleaned_data.get('exp_max')
        if exp_max is not None:
            households = households.filter(TOTEX__lte=exp_max)

    # Pagination
    paginator = Paginator(households, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    show_disclaimer = not request.GET

    context = {
        'form': form,
        'households': page_obj,
        'show_disclaimer': show_disclaimer,
        'paginator': paginator,
        'page_obj': page_obj,
    }

    return render(request, 'calabarzonapp/household_filtered.html', context)

def province_level(request, province_id=None):
    all_provinces = Province.objects.all().order_by('name')

    if province_id is None:
        current_province = all_provinces.first()
    else:
        current_province = get_object_or_404(Province, id=province_id)

    province_list = list(all_provinces)
    current_index = province_list.index(current_province)
    previous_province = province_list[current_index - 1] if current_index > 0 else None
    next_province = province_list[current_index + 1] if current_index < len(province_list) - 1 else None
    
    # Some aggregates
    province_households = Household.objects.filter(province=current_province)
    urban_households = province_households.filter(URB=1).count()
    rural_households = province_households.filter(URB=2).count()
    total_households = province_households.count()
    total_rfact = province_households.aggregate(total=Sum('RFACT'))['total'] or 1

     #Helper function for weighted averages
    def weighted_avg(field_name):
        result = province_households.aggregate(
            weighted=Sum(F(field_name) * F('RFACT'), output_field=FloatField())
        )['weighted']
        return result / total_rfact if result else 0

    avg_income = weighted_avg('TOINC')
    avg_expenditure = weighted_avg('TOTEX')
    avg_food = weighted_avg('FOOD')
    avg_cloth = weighted_avg('CLOTH')
    avg_health = weighted_avg('HEALTH')
    avg_transport = weighted_avg('TRANSPORT')
    avg_communication = weighted_avg('COMMUNICATION')
    avg_recreation = weighted_avg('RECREATION')
    avg_education = weighted_avg('EDUCATION')
    avg_fsize = weighted_avg('FSIZE') or 1
    avg_pcp = weighted_avg('PERCAPITA')

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