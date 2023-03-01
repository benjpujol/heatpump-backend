from django.db import models

class IncomeCategory(models.Model):
    # define the income brackets for subsidy calculation
    tax_household_size = models.PositiveIntegerField()
    upper_income_bound_1 = models.PositiveIntegerField(default = 22461)
    upper_income_bound_2 = models.PositiveIntegerField(default = 27343)
    upper_income_bound_3 = models.PositiveIntegerField(default = 38184)

    

class Subsidy(models.Model):
    # define the subsidy amount for an equipment type and income category
    equipment_type = models.CharField(max_length=50)
    income_category = models.IntegerField()
    state_subsidy_amount = models.IntegerField()
    energy_certificate_amount = models.IntegerField()
    eligible = models.BooleanField(default=True)

