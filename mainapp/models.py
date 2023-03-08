from django.db import models
from subsidies.utils import calculate_subsidy
# import module from subsidies app
from subsidies.utils import calculate_subsidy, calculate_default_subsidy
from django.contrib.auth.models import User

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def get_default_subsidy(self, equipment_type="air_water_heat_pump"):
        return calculate_default_subsidy(self, equipment_type)
   

    def save(self, *args, **kwargs):
        # Allow to update estimate subsidy when customer is updated
        super().save(*args, **kwargs)
        estimates = Estimate.objects.filter(customer=self)
        for estimate in estimates:
            subsidies = calculate_subsidy(estimate)
            estimate.state_subsidy_amount = subsidies["state_subsidy_amount"]
            estimate.energy_certificate_amount = subsidies["energy_certificate_amount"]
            estimate.save()

    

# Create building class
class Building(models.Model):
    id = models.AutoField(primary_key=True)
    year_built = models.IntegerField(default=1950, null=True, blank=True)
    square_footage = models.IntegerField(default=150, null=True, blank=True)
    number_of_floors = models.IntegerField(default=2, null=True, blank=True)
    occupancy_status = models.CharField(default="owner", max_length=50, null=True, blank=True)
    residence_type = models.CharField(default="main", max_length=50, null=True, blank=True)
    primary_heating_system = models.CharField(max_length=50, null=True, blank=True)
    secondary_heating_system = models.CharField(max_length=50, null=True, blank=True)
    hot_water_system = models.CharField(max_length=501, null=True, blank=True)
    temperature_setpoint = models.IntegerField(default=19, null=True, blank=True)
    annual_energy_bill = models.IntegerField(null=True, blank=True)
    annual_energy_consumption = models.IntegerField(null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)    



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
    
    def heat_power(self, inlet_temperature=55, outlet_temperature=45):
        # iterate over each radiator associated with the building
        heat_power = 0
        for radiator in self.radiator_set.all():
            # calculate the heat power of the radiator
            heat_power += radiator.heat_power(inlet_temperature=inlet_temperature, outlet_temperature=outlet_temperature, surrounding_temperature=self.temperature_setpoint)
        return heat_power
    




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
            energy_certificate_amount = subsidies["energy_certificate_amount"]
            self.state_subsidy_amount = state_subsidy_amount
            self.energy_certificate_amount = energy_certificate_amount
        super().save(*args, **kwargs)
    

if __name__ == "__main__":
    # get the building with id 2
    building = Building.objects.get(id=2)

    # call the heat loss function
    heat_loss = building.heat_loss()
    
    #print the heat loss
    