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

    # Get the subsidy amount for the equipment type and income category
    subsidy_object = Subsidy.objects.filter(equipment_type=estimate.equipment_type, income_category=estimate.customer.tax_income_category).first()

    # If the subsidy amount is not None, return the subsidy amount
    if subsidy_object:
        return {'state_subsidy_amount' : subsidy_object.state_subsidy_amount, 'energy_cerficate_amount' : subsidy_object.energy_certificate_amount}
    else:
        return {'state_subsidy_amount' : 0, 'energy_cerficate_amount' : 0}