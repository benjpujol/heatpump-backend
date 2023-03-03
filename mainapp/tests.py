from django.test import TestCase

# Create your tests here.
from  models import Building
from heatloss.models import Wall, Roof, Floor, Window
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'heatpump-backend.settings')
django.setup()

# define the function to calculate heat loss
def calculate_building_heat_loss(building_id):
    # get the building object
    building = Building.objects.get(id=building_id)

    # get the roof and wall objects for the building
    roof = Roof.objects.filter(building=building).first()
    wall = Wall.objects.filter(building=building).first()

    # calculate the heat loss for the building
    heat_loss = 0
    if roof:
        heat_loss += roof.calculate_heat_loss()
    if wall:
        heat_loss += wall.calculate_heat_loss()

    return heat_loss

# test the function
if __name__ == "__main__":
    building_id = 2
    heat_loss = calculate_building_heat_loss(building_id)
   
