import graphene
from graphene_django import DjangoObjectType
from .models import IncomeCategory

class IncomeCategoryType(DjangoObjectType):
    class Meta:
        model = IncomeCategory

class Query(graphene.ObjectType):
    income_categories = graphene.List(IncomeCategoryType, tax_household_size=graphene.Int())

    def resolve_income_categories(self, info, tax_household_size=None):
        if tax_household_size is not None:
            return IncomeCategory.objects.filter(tax_household_size=tax_household_size)
        else:
            return IncomeCategory.objects.all()

schema = graphene.Schema(query=Query)