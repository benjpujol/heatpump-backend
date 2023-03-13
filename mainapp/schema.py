import graphene
from graphene_django import DjangoObjectType
from mainapp.models import Customer, Building, Estimate
from usercatalog.models import UserHeatPump
from heatloss.models import Wall, Roof, Floor, Window, Radiator
from graphql import GraphQLError
import traceback
from users.models import CustomUser

# create basic schema for user in graphene


class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser


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


class RadiatorType(DjangoObjectType):
    class Meta:
        model = Radiator

# create basic schema for building in graphene


class BuildingType(DjangoObjectType):
    class Meta:
        model = Building

    heat_loss = graphene.Float()
    heat_power = graphene.Float()

    def resolve_heat_loss(self, info):
        return self.heat_loss()

    def resolve_heat_power(self, info):
        return self.heat_power()


# create basic schema for estimate in graphene
class EstimateType(DjangoObjectType):
    class Meta:
        model = Estimate


# Customer

class CustomerType(DjangoObjectType):
    default_state_subsidy = graphene.Float()
    default_energy_certificate = graphene.Float()

    class Meta:
        model = Customer

    def resolve_state_subsidy_amount(parent, info):
        print("parent.get_default_subsidy()", parent.get_default_subsidy())
        return parent.get_default_subsidy().get('state_subsidy_amount')

    def resolve_energy_certificate_amount(parent, info):
        return parent.get_default_subsidy().get('energy_certificate_amount')


class CustomerCreateInput(graphene.InputObjectType):
    user_id = graphene.Int(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String(required=True)
    address = graphene.String(required=True)
    latitude = graphene.Float()
    longitude = graphene.Float()
    eligible_for_subsidy = graphene.Boolean()
    tax_household_size = graphene.Int()
    tax_income_category = graphene.Int()

# mutation to create customer


class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CustomerCreateInput(required=True)

    customer = graphene.Field(CustomerType)
    building = graphene.Field(BuildingType)
    roof = graphene.Field(RoofType)
    wall = graphene.Field(WallType)
    floor = graphene.Field(FloorType)
    windows = graphene.List(WindowType)
    radiators = graphene.List(RadiatorType)

    def mutate(self, info, input=None):
        user_instance = CustomUser.objects.get(pk=input.user_id)
        print(user_instance)
        if user_instance:

            try : 
                customer_instance = Customer.objects.create(
                    first_name=input.first_name, last_name=input.last_name, email=input.email, phone=input.phone, address=input.address, latitude=input.latitude, longitude=input.longitude,   user=user_instance)

                # create building instance with default valies
                building = Building.objects.create(year_built=1950, square_footage=150, number_of_floors=2, occupancy_status="owner", residence_type="main", primary_heating_system="gas",
                                                hot_water_system="boiler", secondary_heating_system=None, temperature_setpoint=19, annual_energy_bill=2000, annual_energy_consumption=30000,  customer=customer_instance)

                # create roof instance with default values
                roof = Roof.objects.create(roof_area=100, roof_flat_area=100, roof_perimeter=40, roof_polygon=None,
                                        roof_shape="hip-roof", roof_height=2, roof_type="lost-attic", roof_insulation_u_value=2, building=building)

                # create wall instance with default values
                wall = Wall.objects.create(wall_area=100, wall_insulation_u_value=2,
                                        number_of_storeys=1, storey_height=2.8, building=building)

                # create floor instance with default values
                floor = Floor.objects.create(
                    floor_area=100, floor_type="solid-ground", floor_insulation_u_value=2, building=building)

                # create windows instance with default values
                windows = []
                for i in range(3):
                    window = Window.objects.create(
                        window_area=1, window_width=1, window_height=1, window_insulation_type="single", window_size_type="medium", window_insulation_u_value=2, window_orientation="north", building=building
                    )
                    windows.append(window)

                # create radiators instance with default values
                radiators = []
                for i in range(10):
                    radiator = Radiator.objects.create(
                        type="cast-iron", height=1.5, width=1.5, depth=0.5, building=building
                    )
                    radiators.append(radiator)
                        

                return CreateCustomer(customer=customer_instance, building=building, roof=roof, wall=wall, floor=floor, windows=windows, radiators=radiators)
            except Exception as e:
                print(e)
        
        else:
            raise Exception('User does not exist')
                  


class CustomerUpdateInput(graphene.InputObjectType):
    id=graphene.Int(required = True)
    first_name=graphene.String()
    last_name=graphene.String()
    email=graphene.String()
    phone=graphene.String()
    address=graphene.String()
    latitude=graphene.Float()
    longitude=graphene.Float()
    eligible_for_subsidy=graphene.Boolean()
    tax_household_size=graphene.Int()
    tax_income_category=graphene.Int()

#  mutation to update customer info based on id


class UpdateCustomerById(graphene.Mutation):
    class Arguments:
        input=CustomerUpdateInput(required = True)

    customer=graphene.Field(CustomerType)

    @ staticmethod
    def mutate(root, info, input = None):
        print(input.id)
        customer_instance=Customer.objects.get(pk = input.id)
        print(customer_instance)

        if customer_instance:
            if 'first_name' in input:
                customer_instance.first_name=input.first_name
            if 'last_name' in input:
                customer_instance.last_name=input.last_name
            if 'email' in input:
                customer_instance.email=input.email
            if 'phone' in input:
                customer_instance.phone=input.phone
            if 'address' in input:
                customer_instance.address=input.address
            if 'latitude' in input:
                customer_instance.latitude=input.latitude
            if 'longitude' in input:
                customer_instance.longitude=input.longitude
            if 'eligible_for_subsidy' in input:
                customer_instance.eligible_for_subsidy=input.eligible_for_subsidy
            if 'tax_household_size' in input:
                customer_instance.tax_household_size=input.tax_household_size
            if 'tax_income_category' in input:
                customer_instance.tax_income_category=input.tax_income_category

            try:
                customer_instance.save()
            except Exception as e:
                print(e)
                traceback.print_exc()
                return UpdateCustomerById(customer = None)
            return UpdateCustomerById(customer = customer_instance)
        return UpdateCustomerById(customer = None)


# Building
class BuildingInput(graphene.InputObjectType):
    id=graphene.Int()
    year_built=graphene.Int()
    square_footage=graphene.Int()
    number_of_floors=graphene.Int()
    occupancy_status=graphene.String()
    residence_type=graphene.String()
    primary_heating_system=graphene.String()
    secondary_heating_system=graphene.String()
    hot_water_system=graphene.String()
    temperature_setpoint=graphene.Int()
    annual_energy_bill=graphene.Int()
    annual_energy_consumption=graphene.Int()
    customer_id=graphene.Int(required = True)

# mutation to create building


class CreateBuilding(graphene.Mutation):

    class Arguments:
        input=BuildingInput(required = True)

    building=graphene.Field(BuildingType)

    @ staticmethod
    def mutate(root, info, input = None):
        customer_instance=Customer.objects.get(pk = input.customer_id)
        print(customer_instance)
        if customer_instance:
            try:
                building_instance=Building(
                    year_built = input.year_built,
                    square_footage = input.square_footage,
                    number_of_floors = input.number_of_floors,
                    occupancy_status = input.occupancy_status,
                    residence_type = input.residence_type,
                    primary_heating_system = input.primary_heating_system,
                    secondary_heating_system = input.secondary_heating_system,
                    hot_water_system = input.hot_water_system,
                    temperature_setpoint = input.temperature_setpoint,
                    annual_energy_bill = input.annual_energy_bill,
                    annual_energy_consumption = input.annual_energy_consumption,
                    customer = customer_instance,
                )
                print(building_instance)
                building_instance.save()
            except Exception as e:
                print(e)
                traceback.print_exc()

            return CreateBuilding(building = building_instance)
        return CreateBuilding(building = None)


# mutation to update building info based on customer id
class UpdateBuildingByCustomerId(graphene.Mutation):
    class Arguments:
        input=BuildingInput(required = True)

    building=graphene.Field(BuildingType)

    @ staticmethod
    def mutate(root, info, input = None):
        print(input)
        customer_instance=Customer.objects.get(pk = input.customer_id)

        if customer_instance:
            building_instance=Building.objects.get(
                customer = customer_instance)
            if building_instance:
                if 'year_built' in input:
                    building_instance.year_built=input.year_built
                if 'square_footage' in input:
                    building_instance.square_footage=input.square_footage
                if 'number_of_floors' in input:
                    building_instance.number_of_floors=input.number_of_floors
                if 'occupancy_status' in input:
                    building_instance.occupancy_status=input.occupancy_status
                if 'residence_type' in input:
                    building_instance.residence_type=input.residence_type
                if 'primary_heating_system' in input:
                    building_instance.primary_heating_system=input.primary_heating_system
                if 'secondary_heating_system' in input:
                    building_instance.secondary_heating_system=input.secondary_heating_system
                if 'hot_water_system' in input:
                    building_instance.hot_water_system=input.hot_water_system
                if 'temperature_setpoint' in input:
                    building_instance.temperature_setpoint=input.temperature_setpoint
                if 'annual_energy_bill' in input:
                    building_instance.annual_energy_bill=input.annual_energy_bill
                if 'annual_energy_consumption' in input:
                    building_instance.annual_energy_consumption=input.annual_energy_consumption
                if 'customer' in input:
                    building_instance.customer=customer_instance

                building_instance.save()

                return UpdateBuildingByCustomerId(building = building_instance)
        return UpdateBuildingByCustomerId(building = None)


# Estimates

from graphene.types import Scalar

class SavingsDict(Scalar):
    @staticmethod
    def serialize(value):
        print("value", value)
        return value
    
class EmissionsDict(Scalar):
    @staticmethod
    def serialize(value):
        print("value", value)
        return value
    
class EstimateType(DjangoObjectType):
    class Meta:
        model=Estimate
        
    savings = graphene.Field(SavingsDict)
    emissions = graphene.Field(EmissionsDict)

    def resolve_savings(self, info):
        savings = self.get_savings()
        return savings
    
    def resolve_emissions(self, info):
        emissions = self.get_co2_emissions()
        return emissions


class UserHeatPumpType(DjangoObjectType):
    class Meta:
        model=UserHeatPump


# Mutation to create an estimate based on the selection of heat pumps in the user catalogue (UserHeatPumps)
class CreateEstimate(graphene.Mutation):
    class Arguments:
        customer_id=graphene.Int(required = True)
        user_heat_pumps_ids=graphene.List(graphene.Int, required = True)

    estimates=graphene.List(EstimateType)
    customer=graphene.Field(CustomerType)

    @ staticmethod
    def mutate(root, info, customer_id, user_heat_pumps_ids):
        user_heat_pumps=UserHeatPump.objects.filter(
            id__in = user_heat_pumps_ids)

        if len(user_heat_pumps) != len(user_heat_pumps_ids):
            raise GraphQLError('Invalid User Heat Pump Ids')

        # Get the customer instance
        customer=Customer.objects.get(pk = customer_id)

        if customer:
            # create the estimates instances
            estimates=[]
            for user_heat_pump in user_heat_pumps:
                # check if an estimate already exists for the given customer and user_heat_pump
                existing_estimate=Estimate.objects.filter(
                    heat_pump = user_heat_pump,
                    customer = customer
                ).first()

                if existing_estimate:
                    # skip creating a new estimate if one already exists with the same heat pump and customer
                    continue

                try:
                    estimate_instance = Estimate.objects.create(
                        heat_pump=user_heat_pump,
                        customer=customer,
                        price=1.5 * user_heat_pump.price,
                        state_subsidy_amount=0,
                        energy_certificate_amount=0
                    )
                    estimates.append(estimate_instance)
                except Exception as e:
                    print("Error: ", e)
                    traceback.print_exc()

            return CreateEstimate(estimates=estimates, customer=customer)

        return CreateEstimate(estimates=None, customer=None)


# Mutation to delete estimates based on the selection of heat pumps in the user catalogue (UserHeatPumps)
class DeleteEstimate(graphene.Mutation):
    class Arguments:
        customer_id = graphene.Int(required=True)
        user_heat_pumps_ids = graphene.List(graphene.Int, required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, customer_id, user_heat_pumps_ids):
        user_heat_pumps = UserHeatPump.objects.filter(
            id__in=user_heat_pumps_ids)

        if len(user_heat_pumps) != len(user_heat_pumps_ids):
            raise GraphQLError('Invalid User Heat Pump Ids')

        # Get the customer instance
        customer = Customer.objects.get(pk=customer_id)

        if customer:
            # delete the estimate instances
            for user_heat_pump in user_heat_pumps:
                # get the existing estimate for the given customer and user_heat_pump
                existing_estimate = Estimate.objects.filter(
                    heat_pump=user_heat_pump,
                    customer=customer
                ).first()

                if existing_estimate:
                    # delete the existing estimate
                    existing_estimate.delete()

            return DeleteEstimate(success=True)

        return DeleteEstimate(success=False)


# query
class Query(graphene.ObjectType):

    # query to get the list of customers of a user
    customers = graphene.List(CustomerType, user_id=graphene.ID(required=True))

    def resolve_customers(self, info, user_id):
        return Customer.objects.filter(user_id=user_id)

    customer_by_id = graphene.Field(
        CustomerType, id=graphene.Int(required=True))

    def resolve_customer_by_id(self, info, id):
        try:
            customer = Customer.objects.get(id=id)
            customer.default_state_subsidy = customer.get_default_subsidy().get(
                'state_subsidy_amount')
            customer.default_energy_certificate = customer.get_default_subsidy().get(
                'energy_certificate_amount')
            return customer
        except Customer.DoesNotExist:
            return None

    buildings = graphene.List(BuildingType)
    building_by_customer_id = graphene.Field(
        BuildingType, customer=graphene.Int(required=True))

    def resolve_buildings(self, info):
        return Building.objects.all()

    def resolve_building_by_customer_id(self, info, customer):
        try:
            return Building.objects.get(customer=customer)
        except Building.DoesNotExist:
            return None

    estimates = graphene.List(EstimateType)
    estimates_by_customer_id = graphene.List(
        EstimateType, customer_id=graphene.Int(required=True))

    def resolve_estimates(self, info):
        return Estimate.objects.all()

    def resolve_estimates_by_customer_id(self, info, customer_id):
        customer = Customer.objects.get(pk=customer_id)
        try:
            return Estimate.objects.filter(customer=customer)
        except Estimate.DoesNotExist:
            return None


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    update_customer_by_id = UpdateCustomerById.Field()

    create_building = CreateBuilding.Field()
    update_building_by_customer_id = UpdateBuildingByCustomerId.Field()

    create_estimate = CreateEstimate.Field()
    delete_estimate = DeleteEstimate.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
