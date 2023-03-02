import graphene
from graphene_django import DjangoObjectType
from catalog.models import HeatPump

# Write the schema for the catalog app


# Heat Pump  object type (graphene)
class HeatPumpType(DjangoObjectType):
    class Meta:
        model = HeatPump


class Query(graphene.ObjectType):
    heat_pumps = graphene.List(HeatPumpType)

    def resolve_heat_pumps(self, info, **kwargs):
        return HeatPump.objects.all()


class Mutation(graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)


