from django.db import models
from subsidies.utils import calculate_subsidy


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
        print("estimate change")
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

# Create project class
class Estimate(models.Model):
    id = models.AutoField(primary_key=True)
    equipment_type = models.CharField(max_length=50, default='air_water_heat_pump')
    project_status = models.CharField(max_length=50)
    hot_water_production = models.BooleanField()
    created_date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    state_subsidy_amount = models.DecimalField(max_digits=8, decimal_places=2)
    energy_certificate_amount = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.pk:  # if the object is being created
            print('Creating new estimate')
            subsidies = calculate_subsidy(self)
            state_subsidy_amount = subsidies["state_subsidy_amount"]
            energy_cerficate_amount = subsidies["energy_cerficate_amount"]
            self.state_subsidy_amount = state_subsidy_amount
            self.energy_certificate_amount = energy_cerficate_amount
        super().save(*args, **kwargs)
    
