from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from mainapp.models import Customer, Building
from .models import Subsidy

def calculate_subsidy(request, customer_id, building_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    building = get_object_or_404(Building, pk=building_id)

    # Perform subsidy calculation logic here...
    subsidy_amount = calculate_subsidy_amount(customer, building)

    # Create a new subsidy instance and save it to the database
    subsidy = Subsidy(customer=customer, building=building, amount=subsidy_amount)
    subsidy.save()

    # Return a JSON response with the subsidy amount
    return JsonResponse({'subsidy_amount': subsidy_amount})
