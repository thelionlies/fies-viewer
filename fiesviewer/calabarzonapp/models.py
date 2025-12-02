from django.db import models

class Province(models.Model):
    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='province_images/', blank=True, null=True)
    image_description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class Household(models.Model):

    URB_CHOICES = [
        (1, "Urban"),
        (2, "Rural"),
    ]

    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    SEQ_NO = models.IntegerField(unique=True)
    FSIZE = models.FloatField()
    URB = models.IntegerField(choices=URB_CHOICES)
    RFACT = models.FloatField(null=True, blank=True)
    TOINC = models.FloatField()
    WAGES = models.IntegerField()
    RPCINC = models.IntegerField()
    CASH_ABROAD = models.IntegerField(null=True, blank=True)
    CASH_DOMESTIC = models.IntegerField(null=True, blank=True)
    TOTEX = models.FloatField()
    PERCAPITA = models.FloatField(null=True, blank=True)
    FOOD = models.FloatField()
    CLOTH = models.IntegerField()
    HEALTH = models.IntegerField()
    TRANSPORT = models.IntegerField()
    COMMUNICATION = models.IntegerField()
    RECREATION = models.IntegerField()
    EDUCATION = models.IntegerField()

    def __str__(self):
        return f"Household {self.SEQ_NO} in {self.province}"
