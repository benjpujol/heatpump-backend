import graphene
from graphene_django import DjangoObjectType
from heatloss.models import Wall, Roof, Floor, Window, Radiator
from mainapp.models import Building
from .utils import *


# OrderBY
class OrderByInput(graphene.InputObjectType):
    field = graphene.String()
    direction = graphene.String(default_value="ASC")


# Wall
# Wall object type (graphene)
class WallType(DjangoObjectType):
    class Meta:
        model = Wall

# Wall input type


class WallInput(graphene.InputObjectType):
    wall_area = graphene.Float()
    storey_height = graphene.Float()
    number_of_storeys = graphene.Int()
    wall_insulation_u_value = graphene.Float()
    building = graphene.ID()


# mutation to create wall
class CreateWall(graphene.Mutation):
    class Arguments:
        input = WallInput(required=True)

    wall = graphene.Field(WallType)

    @staticmethod
    def mutate(root, info, input=None):
        wall_instance = Wall(wall_area=input.wall_area, wall_height=input.wall_height,
                             wall_insulation_u_value=input.wall_insulation_u_value,  building_id=input.building)
        wall_instance.save()
        return CreateWall(wall=wall_instance)

# mutation to update wall info based on building id
# mutation to update roof info based on customer id
class UpdateWall(graphene.Mutation):
    class Arguments:
        input = WallInput(required=True)
        customer_id = graphene.Int(required=True)

    wall = graphene.Field(WallType)

    @staticmethod
    def mutate(root, info, input=None, customer_id=None):
        # find the building instance based on customer id

        building_instance = Building.objects.get(customer_id=customer_id)

        print(building_instance)
        if building_instance:
            try:
                wall_instance = Wall.objects.get(
                    building_id=building_instance.id)
                roof_instance = Roof.objects.get(
                    building_id=building_instance.id)
                

                if "number_of_storeys" in input:
                    wall_instance.number_of_storeys = input.number_of_storeys
                if "storey_height" in input:
                    wall_instance.storey_height = input.storey_height
                if "wall_insulation_u_value" in input:
                    wall_instance.wall_insulation_u_value = input.wall_insulation_u_value
               
                wall_instance.wall_area = calculate_wall_area(
                        wall_instance.storey_height, wall_instance.number_of_storeys, roof_instance.roof_perimeter)

                wall_instance.save()

                return UpdateWall(wall=wall_instance)
            except Exception as e:
                print(f"Error: {e}")

        return UpdateWall(wall=None)



# Roof
# Roof object type (graphene)
class RoofType(DjangoObjectType):
    class Meta:
        model = Roof

# Roof input type
# Use the same input type as Roof model


class RoofInput(graphene.InputObjectType):
    roof_area = graphene.Float()
    roof_flat_area = graphene.Float()
    roof_perimeter = graphene.Float()
    roof_shape = graphene.String()
    roof_type = graphene.String()
    roof_insulation_u_value = graphene.Float()
    roof_polygon = graphene.String()

# mutation to create roof


class CreateRoof(graphene.Mutation):
    class Arguments:
        input = RoofInput(required=True)
        customer_id = graphene.Int(required=True)

    roof = graphene.Field(RoofType)

    @staticmethod
    def mutate(root, info, input=None):
        # find the building instance based on customer id
        building_instance = Building.objects.get(customer_id=input.customer_id)

        roof_instance = Roof(roof_area=input.roof_area, roof_flat_area=input.roof_flat_area, roof_perimeter=input.roof_perimeter,
                             roof_shape=input.roof_shape, roof_type=input.roof_type, roof_insulation_u_value=input.roof_insulation_u_value, building=building_instance)
        roof_instance.save()
        return CreateRoof(roof=roof_instance)


# mutation to update roof info based on customer id
class UpdateRoof(graphene.Mutation):
    class Arguments:
        input = RoofInput(required=True)
        customer_id = graphene.Int(required=True)

    roof = graphene.Field(RoofType)

    @staticmethod
    def mutate(root, info, input=None, customer_id=None):
        # find the building instance based on customer id

        building_instance = Building.objects.get(customer_id=customer_id)

        print(building_instance)
        if building_instance:
            try:
                roof_instance = Roof.objects.get(
                    building_id=building_instance.id)

                if "roof_flat_area" in input:
                    roof_instance.roof_flat_area = input.roof_flat_area
                    # calculate roof area using your custom function
                if "roof_perimeter" in input:
                    roof_instance.roof_perimeter = input.roof_perimeter
                if "roof_polygon" in input:
                    roof_instance.roof_polygon = input.roof_polygon
                if "roof_shape" in input:
                    roof_instance.roof_shape = input.roof_shape
                if "roof_height" in input:
                    roof_instance.roof_height = input.roof_height
                if "roof_type" in input:
                    roof_instance.roof_type = input.roof_type
                    # calculate roof area using your custom function
                if "roof_insulation_u_value" in input:
                    roof_instance.roof_insulation_u_value = input.roof_insulation_u_value

                if "roof_area" in input and (int(roof_instance.roof_area) != int((input.roof_area))):
                    print("roof area is changed",
                          roof_instance.roof_area, input.roof_area)
                    roof_instance.roof_area = input.roof_area
                else:
                    roof_instance.roof_area = calculate_roof_area(
                        roof_instance.roof_shape, roof_instance.roof_type, roof_instance.roof_perimeter, roof_instance.roof_flat_area, roof_instance.roof_height)

                roof_instance.save()

                return UpdateRoof(roof=roof_instance)
            except Exception as e:
                print(f"Error: {e}")

        return UpdateRoof(roof=None)

# Floor


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
        floor_instance = Floor(floor_area=input.floor_area, floor_height=input.floor_height,
                               floor_insulation_u_value=input.floor_insulation_u_value,  building_id=input.building)
        floor_instance.save()
        return CreateFloor(floor=floor_instance)



# mutation to update wall info based on building id
# mutation to update roof info based on customer id
class UpdateFloor(graphene.Mutation):
    class Arguments:
        input = FloorInput(required=True)
        customer_id = graphene.Int(required=True)

    floor = graphene.Field(FloorType)

    @staticmethod
    def mutate(root, info, input=None, customer_id=None):
        # find the building instance based on customer id

        building_instance = Building.objects.get(customer_id=customer_id)

        print(building_instance)
        if building_instance:
            try:
                floor_instance = Floor.objects.get(
                    building_id=building_instance.id)

                if "floor_area" in input:
                    floor_instance.floor_area = input.floor_area
                if "floor_type" in input:
                    floor_instance.floor_type = input.floor_type
                if "floor_insulation_u_value" in input:
                    floor_instance.floor_insulation_u_value = input.floor_insulation_u_value
                floor_instance.save()

                return UpdateFloor(floor=floor_instance)
            except Exception as e:
                print(f"Error: {e}")

        return UpdateFloor(wall=None)

# window

class WindowType(DjangoObjectType):
    success = graphene.Boolean()

    class Meta:
        model = Window


class DeleteWindowById(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    Output = WindowType

    @staticmethod
    def mutate(root, info, id):
        try:
            window = Window.objects.get(id=id)
            window.delete()
            return WindowType(id=id, success=True)
        except Window.DoesNotExist:
            return WindowType(id=None, success=False)


class WindowInput(graphene.InputObjectType):
    window_area = graphene.Int()
    window_width = graphene.Int()
    window_height = graphene.Int()
    window_insulation_type = graphene.String()
    window_size_type = graphene.String()
    window_insulation_u_value = graphene.Float()
    window_orientation = graphene.String()
    customer_id = graphene.Int(required=True)


class CreateWindow(graphene.Mutation):
    class Arguments:
        input = WindowInput(required=True)

    window = graphene.Field(WindowType)

    @staticmethod
    def mutate(root, info, input=None):
        print(input)
        building_id = Building.objects.get(customer_id=input.customer_id).id
        try:
            window_instance = Window(window_area=input.window_area, window_width=input.window_width, window_height=input.window_height, window_insulation_type=input.window_insulation_type,
                                     window_size_type=input.window_size_type, window_insulation_u_value=input.window_insulation_u_value, window_orientation=input.window_orientation, building_id=building_id)
            window_instance.save()
        except Exception as e:
            print(e)

        return CreateWindow(window=window_instance)


class UpdateWindowInput(graphene.InputObjectType):
    window_area = graphene.Int()
    window_width = graphene.Int()
    window_height = graphene.Int()
    window_insulation_type = graphene.String()
    window_size_type = graphene.String()
    window_insulation_u_value = graphene.Float()
    window_orientation = graphene.String()
    customer_id = graphene.Int(required=True)
    id = graphene.Int(required=True)


class UpdateWindow(graphene.Mutation):
    class Arguments:
        input = UpdateWindowInput(required=True)

    window = graphene.Field(WindowType)

    @staticmethod
    def mutate(root, info, input=None):
        print(input)
        window_instance = Window.objects.get(id=input.id)
        print(window_instance)
        if "window_area" in input:
            window_instance.window_area = input.window_area
        if "window_width" in input:
            window_instance.window_width = input.window_width
        if "window_height" in input:
            window_instance.window_height = input.window_height
        if "window_insulation_type" in input:
            window_instance.window_insulation_type = input.window_insulation_type
        if "window_size_type" in input:
            window_instance.window_size_type = input.window_size_type
        if "window_insulation_u_value" in input:
            window_instance.window_insulation_u_value = input.window_insulation_u_value
        if "window_orientation" in input:
            window_instance.window_orientation = input.window_orientation
        window_instance.save()
        return UpdateWindow(window=window_instance)


# Radiators

class RadiatorType(DjangoObjectType):
    success = graphene.Boolean()

    class Meta:
        model = Radiator


class DeleteRadiatorById(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    Output = RadiatorType

    @staticmethod
    def mutate(root, info, id):
        try:
            radiator = Radiator.objects.get(id=id)
            radiator.delete()
            return RadiatorType(id=id, success=True)
        except Radiator.DoesNotExist:
            return RadiatorType(id=None, success=False)


class RadiatorInput(graphene.InputObjectType):
    type = graphene.String()
    width = graphene.Float(default_value=1.5)
    height = graphene.Float(default_value=1)
    depth = graphene.Float(default_value=0.5)
    customer_id = graphene.Int(required=True)


class CreateRadiator(graphene.Mutation):
    class Arguments:
        input = RadiatorInput(required=True)

    radiator = graphene.Field(RadiatorType)

    @staticmethod
    def mutate(root, info, input=None):
        print(input)
        building_id = Building.objects.get(customer_id=input.customer_id).id
        try:
            radiator_instance = Radiator(type=input.type, width=input.width,
                                         height=input.height, depth=input.depth, building_id=building_id)
            radiator_instance.save()
        except Exception as e:
            print(e)

        return CreateRadiator(radiator=radiator_instance)


class UpdateRadiatorInput(graphene.InputObjectType):
    type = graphene.String()
    width = graphene.Float(default_value=1.5)
    height = graphene.Float(default_value=1)
    depth = graphene.Float(default_value=0.5)
    customer_id = graphene.Int(required=True)
    id = graphene.Int(required=True)


class UpdateRadiator(graphene.Mutation):
    class Arguments:
        input = UpdateRadiatorInput(required=True)

    radiator = graphene.Field(RadiatorType)

    @staticmethod
    def mutate(root, info, input=None):
        print(input)
        radiator_instance = Radiator.objects.get(id=input.id)
        print(radiator_instance)
        if input.type:
            radiator_instance.type = input.type
        if input.width:
            radiator_instance.width = input.width
        if input.height:
            radiator_instance.height = input.height
        if input.depth:
            radiator_instance.depth = input.depth
        try:
            radiator_instance.save()
        except Exception as e:
            print(e)
        return UpdateRadiator(radiator=radiator_instance)


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
    windows_by_customer_id = graphene.List(WindowType, customer_id=graphene.Int(
    ), order_by=graphene.List(OrderByInput, default_value=[{"field": "id", "direction": "ASC"}]))

    radiators = graphene.List(RadiatorType)
    radiators_by_customer_id = graphene.List(RadiatorType, customer_id=graphene.Int(
    ), order_by=graphene.List(OrderByInput, default_value=[{"field": "id", "direction": "ASC"}]))

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

    def resolve_windows_by_customer_id(self, info, customer_id, order_by=None):
        building_id = Building.objects.get(customer_id=customer_id).id
        queryset = Window.objects.filter(building_id=building_id)
        if order_by:
            for ordering in order_by:
                if ordering.direction.lower() == "asc":
                    queryset = queryset.order_by(ordering.field)
                else:
                    queryset = queryset.order_by("-" + ordering.field)
        return queryset

    def resolve_radiators(self, info, **kwargs):
        return Radiator.objects.all()

    def resolve_radiators_by_customer_id(self, info, customer_id, order_by=None):
        building_id = Building.objects.get(customer_id=customer_id).id
        queryset = Radiator.objects.filter(building_id=building_id)
        if order_by:
            for ordering in order_by:
                if ordering.direction.lower() == "asc":
                    queryset = queryset.order_by(ordering.field)
                else:
                    queryset = queryset.order_by("-" + ordering.field)
        return queryset


class Mutation(graphene.ObjectType):
    create_wall = CreateWall.Field()
    update_wall= UpdateWall.Field()

    create_roof = CreateRoof.Field()
    update_roof = UpdateRoof.Field()

    create_floor = CreateFloor.Field()
    update_floor = UpdateFloor.Field()

    create_window = CreateWindow.Field()
    delete_window_by_id = DeleteWindowById.Field()
    update_window = UpdateWindow.Field()

    create_radiator = CreateRadiator.Field()
    delete_radiator_by_id = DeleteRadiatorById.Field()
    update_radiator = UpdateRadiator.Field()


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
