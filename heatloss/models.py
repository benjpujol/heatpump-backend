from django.db import models

# Create your models here.
# import the building class from mainapp
from mainapp.models import Building

# create the wall class
# this class will be used to store the wall data (wall type, wall area, wall insulation, wall insulation thickness)
class Wall(models.Model):
    # define the wall area
    wall_area = models.IntegerField()
    # define the wall height
    wall_height = models.IntegerField()
    # define the wall insulation
    wall_insulation_u_value = models.FloatField(max_length=50)
    # foreign key to building
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    def heat_loss(self):
        # calculate the heat loss for the wall
        heat_loss = 0
        heat_loss += self.wall_area  * self.wall_insulation_u_value
        return heat_loss

# create the roof class
# this class will be used to store the roof data (roof type, roof area, roof insulation, roof insulation thickness)
class Roof(models.Model):
    # define the roof area
    roof_area = models.IntegerField()
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



# create the floor class
# this class will be used to store the floor data (floor type, floor area, floor insulation, floor insulation thickness)
class Floor(models.Model):
    # define the floor area
    floor_area = models.IntegerField()
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
    window_area = models.IntegerField()
    # define the window dimensions
    window_width = models.IntegerField()
    window_height = models.IntegerField()
    # define the window insulation type (single pane, double pane, triple pane)
    window_type = models.CharField(max_length=50)
    # define the window size type (small, medium, large)
    window_size_type = models.CharField(max_length=50)
    # define the window insulation
    window_insulation_u_value = models.FloatField(max_length=50)
    # foreign key to building
    building = models.ForeignKey(Building, on_delete=models.CASCADE)



