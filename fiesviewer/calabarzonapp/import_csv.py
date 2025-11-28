import pandas as pd
from calabarzonapp.models import Household

# Reference: https://medium.com/@sunilnepali844/understanding-get-or-create-and-update-or-create-in-django-a-beginners-guide-e9040f24500c

# Load CSV
df = pd.read_csv('calabarzonapp/data.csv')

# Insert into database
for _, row in df.iterrows():
    Household.objects.update_or_create(
        SEQ_NO=row['SEQ_NO'],
        defaults={
            'W_PROV': row['W_PROV'],
            'FSIZE': row['FSIZE'],
            'URB': row['URB'],
            'RFACT': row['RFACT'],
            'TOINC': row['TOINC'],
            'WAGES': row['WAGES'],
            'RPCINC': row['RPCINC'],
            'CASH_ABROAD': row['CASH_ABROAD'],
            'CASH_DOMESTIC': row['CASH_DOMESTIC'],
            'TOTEX': row['TOTEX'],
            'PERCAPITA': row['PERCAPITA'],
            'FOOD': row['FOOD'],
            'CLOTH': row['CLOTH'],
            'HEALTH': row['HEALTH'],
            'TRANSPORT': row['TRANSPORT'],
            'COMMUNICATION': row['COMMUNICATION'],
            'RECREATION': row['RECREATION'],
            'EDUCATION': row['EDUCATION']
        }
    )

print(f'Successfully imported {len(df)} rows.')
