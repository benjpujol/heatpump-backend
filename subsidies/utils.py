from datetime import datetime
# Import the models from this app
from .models import IncomeCategory, Subsidy


# function that return the subdi


def calculate_subsidy(estimate):
    # Perform subsidy calculation logic here for one estimate

    # Get the income categories for the customer's household size
    # This return the first income category that matches the customer's household size
    # If there is no income category for the customer's household size, return None
    # TODO - Deal with the case where household size is not in the income categories ( > 5 people)
    income_categories = IncomeCategory.objects.filter(tax_household_size=estimate.customer.tax_household_size).first()

    # set the estimate equipment type to air_water_heat_pump
    equipment_type = "air_water_heat_pump"

    # If the customer is not eligible for subsidy, return 0
    if estimate.customer.eligible_for_subsidy == False:
        return {'state_subsidy_amount' : 0, 'energy_cerficate_amount' : 0}
    

    # Get the subsidy amount for the equipment type and income category
    subsidy_object = Subsidy.objects.filter(equipment_type=equipment_type, income_category=estimate.customer.tax_income_category).first()

    # If the subsidy amount is not None, return the subsidy amount
    if subsidy_object:
        return {'state_subsidy_amount' : subsidy_object.state_subsidy_amount, 'energy_certificate_amount' : subsidy_object.energy_certificate_amount}
    else:
        return {'state_subsidy_amount' : 0, 'energy_certificate_amount' : 0}
    
    

def calculate_default_subsidy(customer, equipment_type="air_water_heat_pump"):
    # Perform subsidy calculation logic for a generic air water heat pump
    # It is an estimate because the heat pump is not yet selected

    if customer.eligible_for_subsidy == False:
        return {'state_subsidy_amount' : 0, 'energy_certificate_amount' : 0}

    subsidy_object = Subsidy.objects.filter(equipment_type=equipment_type, income_category=customer.tax_income_category).first()  

    if subsidy_object:
        return {'state_subsidy_amount' : subsidy_object.state_subsidy_amount, 'energy_certificate_amount' : subsidy_object.energy_certificate_amount}
    else:
        return {'state_subsidy_amount' : 0, 'energy_certificate_amount' : 0}
    



