from django import forms
from .models import Province

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
