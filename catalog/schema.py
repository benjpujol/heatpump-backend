import graphene
from graphene_django import DjangoObjectType
from catalog.models import HeatPump

# Write the schema for the catalog app


# Heat Pump  object type (graphene)
class HeatPumpType(DjangoObjectType):
    class Meta:
        model = HeatPump

# Heat Pump input type (graphene)
class HeatPumpInput(graphene.InputObjectType):
    id = graphene.Int(required=True)
    reference_code = graphene.String()
    name = graphene.String()
    manufacturer = graphene.String()
    price = graphene.Float()
    cost = graphene.Float()
    description = graphene.String()
    image = graphene.String()
    type = graphene.String()
    scop = graphene.Float()
    etas = graphene.Float()
    hot_water = graphene.Boolean()
    power_minus_7_55 = graphene.Float()
    cop_minus_7_55 = graphene.Float()
    power_minus_7_35 = graphene.Float()
    cop_minus_7_35 = graphene.Float()
    power_7_35 = graphene.Float()
    cop_7_35 = graphene.Float()
    power_7_55 = graphene.Float()
    cop_7_55 = graphene.Float()

# mutation to update a heat pump
class UpdateHeatPumpById(graphene.Mutation):
    class Arguments:
        input = HeatPumpInput(required=True)
    
    heat_pump = graphene.Field(HeatPumpType)

    @staticmethod
    def mutate(root, info, input=None):
        heat_pump_instance = HeatPump.objects.get(id=input.id)
        if heat_pump_instance:
            if "reference_code" in input:
                heat_pump_instance.reference_code = input.reference_code
            if "name" in input:
                heat_pump_instance.name = input.name
            if "manufacturer" in input:
                heat_pump_instance.manufacturer = input.manufacturer
            if "price" in input:
                heat_pump_instance.price = input.price
            if "cost" in input:
                heat_pump_instance.cost = input.cost
            if "description" in input:
                heat_pump_instance.description = input.description
            heat_pump_instance.save()
            return UpdateHeatPumpById(heat_pump=heat_pump_instance)
        return UpdateHeatPumpById(heat_pump=None)



# mutation to delete a heat pump
class DeleteHeatPumpById(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    
    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id):
        success = False
        heat_pump_instance = HeatPump.objects.get(id=id)
        if heat_pump_instance:
            heat_pump_instance.delete()
            return DeleteHeatPumpById(success=True)
        return DeleteHeatPumpById(success=False)

# graphql query to delete a heat pump with gql and apollo
# mutation deleteHeatPumpById($id: Int!) {
#   deleteHeatPumpById(id: $id) {
#     heatPump {
#       id
#     }
#   }
# }

class Query(graphene.ObjectType):
    heat_pumps = graphene.List(
        HeatPumpType,
        sort_by=graphene.String())

    def resolve_heat_pumps(self, info, sort_by=None, **kwargs):
        query_set = HeatPump.objects.all()
        if sort_by:
            query_set = query_set.order_by(sort_by)
        return query_set


class Mutation(graphene.ObjectType):
    update_heat_pump_by_id = UpdateHeatPumpById.Field()
    delete_heat_pump_by_id = DeleteHeatPumpById.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)


