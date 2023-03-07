import graphene
from graphene_django import DjangoObjectType
from .models import IncomeCategory, Subsidy
from mainapp.models import Customer
from .utils import calculate_default_subsidy

class IncomeCategoryType(DjangoObjectType):
    class Meta:
        model = IncomeCategory

class SubsidyType(DjangoObjectType):
    class Meta:
        model = Subsidy


class Query(graphene.ObjectType):
    income_categories = graphene.List(IncomeCategoryType, tax_household_size=graphene.Int())

    def resolve_income_categories(self, info, tax_household_size=None):
        if tax_household_size is not None:
            return IncomeCategory.objects.filter(tax_household_size=tax_household_size)
        else:
            return IncomeCategory.objects.all()
        
    subsidy = graphene.Field(SubsidyType, equipment_type=graphene.String(), income_category=graphene.String())

    def resolve_subsidy(self, info, customer_id, equipment_type="air_water_heat_pump"):
        customer = Customer.objects.get(id=customer_id)
        return calculate_default_subsidy(customer, equipment_type)

schema = graphene.Schema(query=Query)