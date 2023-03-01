from django.contrib import admin

# Register your models here.
from .models import Customer, Building, Estimate

admin.site.register(Customer)
admin.site.register(Building)
admin.site.register(Estimate)

