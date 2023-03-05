from django.db import models
from subsidies.utils import calculate_subsidy
# import module from subsidies app
from subsidies.utils import calculate_subsidy

from usercatalog.models import UserHeatPump


# Create customer model
class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    eligible_for_subsidy = models.BooleanField(default=True)
    tax_household_size =  models.IntegerField(default=2)  
    tax_income_category = models.IntegerField(default=500000)

    def save(self, *args, **kwargs):
        # Allow to update estimate subsidy when customer is updated
        super().save(*args, **kwargs)
        estimates = Estimate.objects.filter(customer=self)
        for estimate in estimates:
            subsidies = calculate_subsidy(estimate)
            estimate.state_subsidy_amount = subsidies["state_subsidy_amount"]
            estimate.energy_certificate_amount = subsidies["energy_cerficate_amount"]
            estimate.save()

    

# Create building class
class Building(models.Model):
    id = models.AutoField(primary_key=True)
    year_built = models.IntegerField()
    square_footage = models.IntegerField()
    number_of_floors = models.IntegerField()
    occupancy_status = models.CharField(max_length=50)
    residence_type = models.CharField(max_length=50)
    primary_heating_system = models.CharField(max_length=50)
    secondary_heating_system = models.CharField(max_length=50)
    hot_water_system = models.CharField(max_length=501)
    temperature_setpoint = models.IntegerField(default=19)
    annual_energy_bill = models.IntegerField()
    annual_energy_consumption = models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)    

    def save(self, *args, **kwargs):
        # Allow to update estimate subsidy when building is updated
        super().save(*args, **kwargs)
        estimates = Estimate.objects.filter(building=self)
        for estimate in estimates:
            subsidies = calculate_subsidy(estimate)
            estimate.state_subsidy_amount = subsidies["state_subsidy_amount"]
            estimate.energy_cerficate_amount = subsidies["energy_cerficate_amount"]
            estimate.save()

    # function to calculate the heat loss of the building
    def heat_loss(self):
        # calculate the heat loss per kelvin (W/K) of the building based on its wall and roof
        heat_loss_per_kelvin = 0
        
        # iterate over each wall associated with the building
        for wall in self.wall_set.all():
            # calculate the heat loss of the wall
            heat_loss_per_kelvin += wall.heat_loss()
        # iterate over each roof associated with the building
        for roof in self.roof_set.all():
            # calculate the heat loss of the roof
            heat_loss_per_kelvin += roof.heat_loss()
        for floor in self.floor_set.all():
            # calculate the heat loss of the roof
            heat_loss_per_kelvin += floor.heat_loss()
        
        # calculate the heat loss of the building
        # reference temperature is hardcode to -7 degrees
        heat_loss = heat_loss_per_kelvin * (self.temperature_setpoint + 7)
        
        return heat_loss



# class for one estimate
class Estimate(models.Model):
    heat_pump = models.ForeignKey(UserHeatPump, on_delete=models.CASCADE) #the estimate is associated with a heat pump in the user catalog
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    price = models.FloatField() 
    state_subsidy_amount = models.DecimalField(max_digits=8, decimal_places=2) #will need to compute subsidies based on the heat pump, the building and the customer
    energy_certificate_amount = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.pk:  # if the object is being created
            print("creating estimate")
            subsidies = calculate_subsidy(self)
            state_subsidy_amount = subsidies["state_subsidy_amount"]
            energy_cerficate_amount = subsidies["energy_cerficate_amount"]
            self.state_subsidy_amount = state_subsidy_amount
            self.energy_certificate_amount = energy_cerficate_amount
        super().save(*args, **kwargs)
    

if __name__ == "__main__":
    # get the building with id 2
    building = Building.objects.get(id=2)

    # call the heat loss function
    heat_loss = building.heat_loss()
    
    #print the heat loss
    