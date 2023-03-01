import graphene
from graphene_django import DjangoObjectType
from heatloss.models import Wall, Roof, Floor, Window

class WallType(DjangoObjectType):
    class Meta:
        model = Wall

class RoofType(DjangoObjectType):
    class Meta:
        model = Roof

class FloorType(DjangoObjectType):
    class Meta:
        model = Floor

class WindowType(DjangoObjectType):
    class Meta:
        model = Window

## Wall
# Wall input type
class WallInput(graphene.InputObjectType):
    id = graphene.ID()
    wall_area = graphene.Int()
    wall_height = graphene.Int()
    wall_insulation_u_value = graphene.Float()
    wall_heat_loss = graphene.Int()
    building = graphene.ID()


# mutation to create wall
class CreateWall(graphene.Mutation):
    class Arguments:
        input = WallInput(required=True)

    wall = graphene.Field(WallType)

    @staticmethod
    def mutate(root, info, input=None):
        wall_instance = Wall(wall_area=input.wall_area, wall_height=input.wall_height, wall_insulation_u_value=input.wall_insulation_u_value, wall_heat_loss=input.wall_heat_loss, building_id=input.building)
        wall_instance.save()
        return CreateWall(wall=wall_instance)


    

class Query(graphene.ObjectType):
    walls = graphene.List(WallType)
    roofs = graphene.List(RoofType)
    floors = graphene.List(FloorType)
    windows = graphene.List(WindowType)

    def resolve_walls(self, info, **kwargs):
        return Wall.objects.all()

    def resolve_roofs(self, info, **kwargs):
        return Roof.objects.all()

    def resolve_floors(self, info, **kwargs):
        return Floor.objects.all()

    def resolve_windows(self, info, **kwargs):
        return Window.objects.all()



class Mutation(graphene.ObjectType):
    create_wall = CreateWall.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
