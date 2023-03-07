import graphene
from graphene_django import DjangoObjectType
from heatloss.models import Wall, Roof, Floor, Window
from mainapp.models import Building




class WindowType(DjangoObjectType):
    class Meta:
        model = Window


## Wall
# Wall object type (graphene)
class WallType(DjangoObjectType):
    class Meta:
        model = Wall

# Wall input type
class WallInput(graphene.InputObjectType):
    wall_area = graphene.Int()
    wall_height = graphene.Int()
    wall_insulation_u_value = graphene.Float()
    building = graphene.ID()


# mutation to create wall
class CreateWall(graphene.Mutation):
    class Arguments:
        input = WallInput(required=True)

    wall = graphene.Field(WallType)

    @staticmethod
    def mutate(root, info, input=None):
        wall_instance = Wall(wall_area=input.wall_area, wall_height=input.wall_height, wall_insulation_u_value=input.wall_insulation_u_value,  building_id=input.building)
        wall_instance.save()
        return CreateWall(wall=wall_instance)

# mutation to update wall info based on building id
class UpdateWallByBuildingId(graphene.Mutation):
    class Arguments:
        input = WallInput(required=True)

    wall = graphene.Field(WallType)

    @staticmethod
    def mutate(root, info, input=None):
        building_instance = Building.objects.get(id=input.building)
        if building_instance :
            wall_instance = Wall.objects.get(building_id=input.building)
            if "wall_area" in input:
                wall_instance.wall_area = input.wall_area
            if "wall_height" in input:
                wall_instance.wall_height = input.wall_height
            if "wall_insulation_u_value" in input:
                wall_instance.wall_insulation_u_value = input.wall_insulation_u_value
            if "building" in input:
                wall_instance.building = building_instance
            wall_instance.save()
            return UpdateWallByBuildingId(wall=wall_instance)
        return UpdateWallByBuildingId(wall=None)
   

## Roof
# Roof object type (graphene)
class RoofType(DjangoObjectType):
    class Meta:
        model = Roof

# Roof input type
# Use the same input type as Roof model
class RoofInput(graphene.InputObjectType):
    roof_area = graphene.Int()
    roof_shape = graphene.String()
    roof_type = graphene.String()
    roof_insulation_u_value = graphene.Float()
    building = graphene.ID()

# mutation to create roof
class CreateRoof(graphene.Mutation):
    class Arguments:
        input = RoofInput(required=True)

    roof = graphene.Field(RoofType)

    @staticmethod
    def mutate(root, info, input=None):
        roof_instance = Roof(roof_area=input.roof_area, roof_shape=input.roof_shape, roof_insulation_u_value=input.roof_insulation_u_value, building_id=input.building)
        roof_instance.save()
        return CreateRoof(roof=roof_instance)   

# mutation to update roof info based on building id
class UpdateRoofByBuildingId(graphene.Mutation):
    class Arguments:
        input = RoofInput(required=True)

    roof = graphene.Field(RoofType)

    @staticmethod
    def mutate(root, info, input=None):
        building_instance = Building.objects.get(id=input.building)
        if building_instance :
            roof_instance = Roof.objects.get(building_id=input.building)
            if "roof_area" in input:
                roof_instance.roof_area = input.roof_area
            if "roof_shape" in input:
                roof_instance.roof_shape = input.roof_shape
            if "roof_type" in input:
                roof_instance.roof_type = input.roof_type
            if "roof_insulation_u_value" in input:
                roof_instance.roof_insulation_u_value = input.roof_insulation_u_value
            if "building" in input:
                roof_instance.building = building_instance
            roof_instance.save()
            return UpdateRoofByBuildingId(roof=roof_instance)
        return UpdateRoofByBuildingId(roof=None)    

## Floor
class FloorType(DjangoObjectType):
    class Meta:
        model = Floor

class FloorInput(graphene.InputObjectType):
    floor_area = graphene.Int()
    floor_height = graphene.Int()
    floor_type = graphene.String()
    floor_insulation_u_value = graphene.Float()
    building = graphene.ID()

class CreateFloor(graphene.Mutation):
    class Arguments:
        input = FloorInput(required=True)

    floor = graphene.Field(FloorType)

    @staticmethod
    def mutate(root, info, input=None):
        floor_instance = Floor(floor_area=input.floor_area, floor_height=input.floor_height, floor_insulation_u_value=input.floor_insulation_u_value,  building_id=input.building)
        floor_instance.save()
        return CreateFloor(floor=floor_instance)

class UpdateFloorByBuildingId(graphene.Mutation):
    class Arguments:
        input = FloorInput(required=True)

    floor = graphene.Field(FloorType)

    @staticmethod
    def mutate(root, info, input=None):
        building_instance = Building.objects.get(id=input.building)
        if building_instance :
            floor_instance = Floor.objects.get(building_id=input.building)
            if "floor_area" in input:
                floor_instance.floor_area = input.floor_area
            if "floor_type" in input:
                floor_instance.floor_type = input.floor_type
            if "floor_insulation_u_value" in input:
                floor_instance.floor_insulation_u_value = input.floor_insulation_u_value
            if "building" in input:
                floor_instance.building = building_instance
            floor_instance.save()
            return UpdateFloorByBuildingId(floor=floor_instance)
        return UpdateFloorByBuildingId(floor=None)

    


class Query(graphene.ObjectType):
    walls = graphene.List(WallType)
    wall_by_building_id = graphene.Field(WallType, building_id=graphene.ID())
    wall_by_customer_id = graphene.Field(WallType, customer_id=graphene.ID())
    
    roofs = graphene.List(RoofType)
    roof_by_building_id = graphene.Field(RoofType, building_id=graphene.ID())
    roof_by_customer_id = graphene.Field(RoofType, customer_id=graphene.ID())

    floors = graphene.List(FloorType)
    floor_by_building_id = graphene.Field(FloorType, building_id=graphene.ID())
    floor_by_customer_id = graphene.Field(FloorType, customer_id=graphene.ID())

    windows = graphene.List(WindowType)
    windows_by_customer_id = graphene.List(WindowType, customer_id=graphene.Int())

    def resolve_walls(self, info, **kwargs):
        return Wall.objects.all()

    def resolve_wall_by_building_id(self, info, building_id):
        return Wall.objects.get(building_id=building_id)
    
    def resolve_wall_by_customer_id(self, info, customer_id):
        # get building id from customer id
        building_id = Building.objects.get(customer_id=customer_id).id
        return Wall.objects.get(building_id=building_id)


    def resolve_roofs(self, info, **kwargs):
        return Roof.objects.all()

    def resolve_roof_by_building_id(self, info, building_id):
        return Roof.objects.get(building_id=building_id)

    def resolve_roof_by_customer_id(self, info, customer_id):
        # get building id from customer id
        building_id = Building.objects.get(customer_id=customer_id).id
        return Roof.objects.get(building_id=building_id)



    def resolve_floors(self, info, **kwargs):
        return Floor.objects.all()

    def resolve_floor_by_building_id(self, info, building_id):
        return Floor.objects.get(building_id=building_id)

    def resolve_floor_by_customer_id(self, info, customer_id):
        # get building id from customer id
        building_id = Building.objects.get(customer_id=customer_id).id
        return Floor.objects.get(building_id=building_id)

    def resolve_windows(self, info, **kwargs):
        return Window.objects.all()
    
    def resolve_windows_by_customer_id(self, info, customer_id):
        # get building id from customer id
        building_id = Building.objects.get(customer_id=customer_id).id
        return Window.objects.filter(building_id=building_id)



class Mutation(graphene.ObjectType):
    create_wall = CreateWall.Field()
    update_wall_by_building_id = UpdateWallByBuildingId.Field()

    create_roof = CreateRoof.Field()
    update_roof_by_building_id = UpdateRoofByBuildingId.Field()

    create_floor = CreateFloor.Field()
    update_floor_by_building_id = UpdateFloorByBuildingId.Field()




schema = graphene.Schema(query=Query, mutation=Mutation)



# # mutation to update wall info based on building id
# written in the gql javascrtipt file with the gql client
# const UPDATE_WALL_BY_BUILDING_ID = gql`
#     mutation UpdateWallByBuildingId($input: WallInput!) {
#         updateWallByBuildingId(input: $input) {
#             wall {
#                 wallArea
#                 wallHeight
#                 wallInsulationUValue
#                 wallHeatLoss
#             }
#         }
#     }
# `;

# call from the frontend with the gql client
# const [updateWallByBuildingId] = useMutation(UPDATE_WALL_BY_BUILDING_ID, {
#     variables: {
#         input: {
#             wallArea: wallArea,
#             wallHeight: wallHeight,
#             wallInsulationUValue: wallInsulationUValue,
#             wallHeatLoss: wallHeatLoss,
#             building: buildingId
#         }

