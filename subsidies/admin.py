from django.contrib import admin

# Register your models here.
from .models import  IncomeCategory, Subsidy

admin.site.register(IncomeCategory)
admin.site.register(Subsidy)

