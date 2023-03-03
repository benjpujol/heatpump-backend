from mainapp.models import Building


# get the building object you want to calculate heat loss for
building = Building.objects.get(id=2)

# get the roof object corresponding to the building
roof = building.roof_set.get()


# call the heat_loss() method to calculate the heat loss for the building
heat_loss = building.heat_loss()


