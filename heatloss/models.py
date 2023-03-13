from django.db import models
import math

# Create your models here.
# import the building class from mainapp
from mainapp.models import Building
from .utils import *

# create the wall class
# this class will be used to store the wall data (wall type, wall area, wall insulation, wall insulation thickness)
class Wall(models.Model):
    # define the wall area
    wall_area = models.FloatField()
    # define the wall insulation
    wall_insulation_u_value = models.FloatField(max_length=50)
    number_of_storeys = models.IntegerField(default=1)
    storey_height = models.FloatField(default=2.8)
    # foreign key to building
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    def heat_loss(self):
        # calculate the heat loss for the wall
        heat_loss = 0
        heat_loss += self.wall_area  * self.wall_insulation_u_value
        return heat_loss
    
    def calculate_wall_area(self):
        roof = self.building.roof
        roof_perimeter = roof.roof_perimeter
        print(roof_perimeter)
        return calculate_wall_area(self.number_of_storeys, self.storey_height,  roof_perimeter)

# create the roof class
# this class will be used to store the roof data (roof type, roof area, roof insulation, roof insulation thickness)
class Roof(models.Model):
    # define the roof sloped area
    roof_area = models.FloatField()
    # define the roof flat area
    roof_flat_area = models.FloatField()
    # define the roof perimeter
    roof_perimeter = models.FloatField()
    # define the roof polygon coordinates
    roof_polygon = models.TextField(null=True, blank=True)
    # define the roof shape
    roof_shape = models.CharField(max_length=50)
    # define the roof_heihgt
    roof_height = models.IntegerField()
    # define the roof type
    roof_type = models.CharField(max_length=50)
    # define the roof insulation
    roof_insulation_u_value = models.FloatField(max_length=50)

    # foreign key to building
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    def heat_loss(self):
        # calculate the heat loss for the roof
        heat_loss = 0
        heat_loss += self.roof_area  * self.roof_insulation_u_value
        return heat_loss
    
    def calculate_roof_area(self):
        return calculate_roof_area(self.roof_shape, self.roof_type, self.roof_perimeter, self.roof_flat_area, self.roof_height)


# create the floor class
# this class will be used to store the floor data (floor type, floor area, floor insulation, floor insulation thickness)
class Floor(models.Model):
    # define the floor area
    floor_area = models.FloatField()
    # define the type of floor (what is underneat the house) : garage, basement, crawl space, slab
    floor_type = models.CharField(max_length=50)
    # define the floor insulation
    floor_insulation_u_value = models.FloatField(max_length=50)
    # foreign key to building
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    def heat_loss(self):
        # calculate the heat loss for the floor
        heat_loss = 0
        heat_loss += self.floor_area  * self.floor_insulation_u_value
        return heat_loss
    

# create the window class
# this class will be used to store the window data (window type, window area, window insulation, window insulation thickness)
class Window(models.Model):
    # define the window area
    window_area = models.IntegerField(null=True, blank=True)
    # define the window dimensions
    window_width = models.IntegerField(null=True, blank=True)
    window_height = models.IntegerField(null=True, blank=True)
    # define the window insulation type (single, double, triple)
    window_insulation_type = models.CharField(max_length=50, null=True, blank=True)
    # define the window size type (small, medium, large)
    window_size_type = models.CharField(max_length=50, null=True, blank=True)
    # define the window insulation
    window_insulation_u_value = models.FloatField(max_length=50, null=True, blank=True)
    #define the window orientation
    window_orientation = models.CharField(max_length=50, null=True, blank=True)
    # foreign key to building
    building = models.ForeignKey(Building, on_delete=models.CASCADE)



# create the radiator class
class Radiator(models.Model):
    # define the radiator type :  cast-iron, aluminium, 
    type = models.CharField(max_length=50)
    # define the radiator height
    height = models.FloatField(default=1.5)
    # define the radiator width
    width = models.FloatField(default=1.5)
    # define the radiator depth
    depth = models.FloatField(default=0.5)    
    # foreign key to building
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    def heat_power(self, inlet_temperature=55, outlet_temperature=45,  surrounding_temperature=20):

        n_coeff_values = {"cast-iron": 1.33, "aluminium": 1.4, "steel": 1.4, "steel-1": 1.4, "steel-2":1.4} #constant describing the type of radiator
        n_coeff = n_coeff_values[self.type]
        p_50 = 1200               #heat emission from radiator with temperature difference 50 oC (W)

        # calculate the heat power for the radiator
    
        heat_power = p_50 * ((inlet_temperature - outlet_temperature) / math.log( (inlet_temperature - surrounding_temperature) / (outlet_temperature - surrounding_temperature))/ 49.32)**(n_coeff)
        return heat_power


