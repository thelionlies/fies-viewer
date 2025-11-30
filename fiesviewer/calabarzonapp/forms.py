from django import forms
from .models import Province, Household
from django.db.models import Max

AREA_CHOICES = (
    ('', 'Any'),
    (1, 'Urban'),
    (2, 'Rural'),
)

class HouseholdFilterForm(forms.Form):
    provinces = forms.ModelMultipleChoiceField(
        queryset=Province.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Provinces"
    )
    area_type = forms.ChoiceField(
        choices=AREA_CHOICES,
        required=False,
        label="Area Type"
    )
    income_min = forms.FloatField(
        required=False,
        label="Income Min",
        min_value=0,
        widget=forms.NumberInput(attrs={'step': 10000, 'min': 0})
    )
    income_max = forms.FloatField(
        required=False,
        label="Income Max",
        min_value=0,
        widget=forms.NumberInput(attrs={'step': 10000, 'min': 0})
    )
    exp_min = forms.FloatField(
        required=False,
        label="Expenditure Min",
        min_value=0,
        widget=forms.NumberInput(attrs={'step': 10000, 'min': 0})
    )
    exp_max = forms.FloatField(
        required=False,
        label="Expenditure Max",
        min_value=0,
        widget=forms.NumberInput(attrs={'step': 10000, 'min': 0})
    )

class HouseholdAddForm(forms.ModelForm):
    class Meta:
        model = Household
        fields = [
            'province', 'FSIZE', 'URB', 'RFACT', 'TOINC', 'WAGES',
            'RPCINC', 'CASH_ABROAD', 'CASH_DOMESTIC', 'TOTEX', 'PERCAPITA',
            'FOOD', 'CLOTH', 'HEALTH', 'TRANSPORT', 'COMMUNICATION',
            'RECREATION', 'EDUCATION'
        ]

        # Add attrs={'class': 'form-control'} later
        # Are there assumptions about TOINC and TOTEX?
        widgets = {
            'province': forms.Select(),
            'FSIZE': forms.NumberInput(),
            # 'URB': forms.NumberInput(), # changed to Select automatically because of choices
            'RFACT': forms.NumberInput(), # is this needed
            'TOINC': forms.NumberInput(), # this should be an autocomputed value
            'WAGES': forms.NumberInput(),
            'RPCINC': forms.NumberInput(), # is this needed
            'CASH_ABROAD': forms.NumberInput(),
            'CASH_DOMESTIC': forms.NumberInput(),
            'TOTEX': forms.NumberInput(), # this should be an autocomputed value
            'PERCAPITA': forms.NumberInput(), # is this needed
            'FOOD': forms.NumberInput(),
            'CLOTH': forms.NumberInput(),
            'HEALTH': forms.NumberInput(),
            'TRANSPORT': forms.NumberInput(),
            'COMMUNICATION': forms.NumberInput(),
            'RECREATION': forms.NumberInput(),
            'EDUCATION': forms.NumberInput(),
        }