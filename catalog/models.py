from django.db import models

# Create your models here.

# Create an abstract class for the catalog items
class CatalogItem(models.Model):
    # define the reference code of the catalog item
    reference_code = models.CharField(max_length=50)
    # define the name of the catalog item
    name = models.CharField(max_length=50, default="")
    # define the manufacturer of the catalog item
    manufacturer = models.CharField(max_length=50, default="")
    # define the price of the catalog item
    price = models.FloatField(default=0)
    # define the cost of the catalog item
    cost = models.FloatField(default=0)
    # define the description of the catalog item
    description = models.CharField(max_length=500, default="",      blank=True)
    # define the image of the catalog item
    image = models.CharField(max_length=500, default="", null=True, blank=True)
    # define the type of catalog item
    type = models.CharField(max_length=50, default="",  null=True, blank=True)

    class Meta:
        # set this model to be abstract so that it won't create a separate table
        # in the database, but will be used as a base class for other models
        abstract = True


class HeatPump(CatalogItem):
    # define the heat pump seasonal efficiency (scop)
    scop = models.FloatField(default=3.5)
    # define the heat pump Etas
    etas = models.FloatField(default=0.8)
    # define if the heat pump can provide hot water
    hot_water = models.BooleanField(default=False)
    # define the heat pump power at -7C/55C
    power_minus_7_55 = models.FloatField(default=8.5)
    # define the heat pump cop at -7C/55C
    cop_minus_7_55 = models.FloatField(default=3.5)
    # define the heat pump power at -7C/35C
    power_minus_7_35 = models.FloatField(default=8.5)
    # define the heat pump cop at -7C/35C
    cop_minus_7_35 = models.FloatField(default=3.5)
    # define the heat pump power at 7C/35C
    power_7_35 = models.FloatField(default=8.5)
     # define the heat pump cop at 7C/35C
    cop_7_35 = models.FloatField(default=3.5)
    # define the heat pump power at 7C/55C
    power_7_55 = models.FloatField(default=8.5)
    # define the heat pump cop at 7C/55C
    cop_7_55 = models.FloatField(default=3.5)
    

