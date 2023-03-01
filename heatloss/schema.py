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
    pass

schema = graphene.Schema(query=Query)
