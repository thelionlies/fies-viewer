from django.db import models

# Create your models here.
class Household(models.Model):
    # Identification
    W_PROV = models.IntegerField()
    SEQ_NO = models.IntegerField(unique=True)

    # Household Characteristics
    FSIZE = models.FloatField()
    URB = models.IntegerField()
    RFACT = models.FloatField(null=True, blank=True)

    # Income
    TOINC = models.FloatField()
    WAGES = models.IntegerField()
    RPCINC = models.IntegerField()
    CASH_ABROAD = models.IntegerField(null=True, blank=True)
    CASH_DOMESTIC = models.IntegerField(null=True, blank=True)

    # Expenditure
    TOTEX = models.FloatField()
    PERCAPITA = models.FloatField(null=True, blank=True)

    # Specific expenditures
    FOOD = models.FloatField()
    CLOTH = models.IntegerField()
    HEALTH = models.IntegerField()
    TRANSPORT = models.IntegerField()
    COMMUNICATION = models.IntegerField()
    RECREATION = models.IntegerField()
    EDUCATION = models.IntegerField()

    def __str__(self):
        return f"Household {self.SEQ_NO} in Province {self.W_PROV}"