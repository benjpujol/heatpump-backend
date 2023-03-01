from django.contrib import admin

# Register your models here.
from .models import Wall, Roof, Floor, Window

admin.site.register(Wall)
admin.site.register(Roof)
admin.site.register(Floor)
admin.site.register(Window)
