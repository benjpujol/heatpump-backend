from django.db import models
from catalog.models import HeatPump
from users.models import CustomUser

# Create your models here.



# class for the user heat pumps
class UserHeatPump(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    heat_pump = models.ForeignKey(HeatPump, on_delete=models.CASCADE)
    price = models.FloatField()
    description = models.TextField()

    class Meta:
        unique_together = ('user', 'heat_pump',)

   