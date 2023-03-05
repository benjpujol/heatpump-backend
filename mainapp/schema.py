import graphene
from graphene_django import DjangoObjectType
from mainapp.models import Customer, Building, Estimate
from usercatalog.models import UserHeatPump
from graphql import GraphQLError

#create basic schema for customer in graphene

#create basic schema for building in graphene
class BuildingType(DjangoObjectType):
    class Meta:
        model = Building
    
    heat_loss = graphene.Float()

    def resolve_heat_loss(self, info):
        return self.heat_loss()

#create basic schema for estimate in graphene
class EstimateType(DjangoObjectType):
    class Meta:
        model = Estimate



## Customer

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer


class CustomerInput(graphene.InputObjectType):
    id = graphene.Int(required=True)
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    phone = graphene.String()
    address = graphene.String()
    eligible_for_subsidy = graphene.Boolean()
    tax_household_size = graphene.Int()
    tax_income_category = graphene.Int()

# mutation to create customer
class CreateCustomer(graphene.Mutation):    
    class Arguments:
        input = CustomerInput(required=True)

    customer = graphene.Field(CustomerType)

    def mutate(self, info, input=None):
        customer_instance = Customer(first_name=input.first_name,last_name=input.last_name,email=input.email,phone=input.phone,address=input.address,eligible_for_subsidy=input.eligible_for_subsidy,tax_household_size=input.tax_household_size,tax_income_category=input.tax_income_category)
        customer_instance.save()

        return CreateCustomer(customer=customer_instance)

#  mutation to update customer info based on id
class UpdateCustomerById(graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    customer = graphene.Field(CustomerType)

    @staticmethod
    def mutate(root, info, input=None):
        customer_instance = Customer.objects.get(pk=input.id)
        if customer_instance:
            if 'first_name' in input:
                customer_instance.first_name = input.first_name
            if 'last_name' in input:
                customer_instance.last_name = input.last_name
            if 'email' in input:
                customer_instance.email = input.email
            if 'phone' in input:
                customer_instance.phone = input.phone
            if 'address' in input:
                customer_instance.address = input.address
            if 'eligible_for_subsidy' in input:
                customer_instance.eligible_for_subsidy = input.eligible_for_subsidy
            if 'tax_household_size' in input:
                customer_instance.tax_household_size = input.tax_household_size
            if 'tax_income_category' in input:
                customer_instance.tax_income_category = input.tax_income_category
    
            customer_instance.save()
            return UpdateCustomerById(customer=customer_instance)
        return UpdateCustomerById(customer=None)



## Building
class BuildingInput(graphene.InputObjectType):
    id = graphene.Int()
    year_built = graphene.Int()
    square_footage = graphene.Int()
    number_of_floors = graphene.Int()
    occupancy_status = graphene.String()
    residence_type = graphene.String()
    primary_heating_system = graphene.String()
    secondary_heating_system =  graphene.String()
    hot_water_system = graphene.String()
    temperature_setpoint = graphene.Int()
    annual_energy_bill =  graphene.Int()
    annual_energy_consumption =  graphene.Int()      
    customer = graphene.Field(CustomerInput, required=True)

# mutation to create building
class CreateBuilding(graphene.Mutation):

    class Arguments:
        input = BuildingInput(required=True)
        

    building = graphene.Field(BuildingType)

    @staticmethod
    def mutate(root, info, input=None):
        customer_instance = Customer.objects.get(pk=input.customer.id)
        if customer_instance:
            building_instance = Building(
                year_built=input.year_built,
                square_footage=input.square_footage,
                number_of_floors=input.number_of_floors,
                occupancy_status=input.occupancy_status,
                residence_type=input.residence_type,
                primary_heating_system=input.primary_heating_system,
                secondary_heating_system=input.secondary_heating_system,
                hot_water_system=input.hot_water_system,
                temperature_setpoint=input.temperature_setpoint,
                annual_energy_bill=input.annual_energy_bill,
                annual_energy_consumption=input.annual_energy_consumption,
                customer=customer_instance,
            )
            building_instance.save()
            return CreateBuilding(building=building_instance)
        return CreateBuilding(building=None)

        

# mutation to update building info based on customer id
class UpdateBuildingByCustomerId(graphene.Mutation):
    class Arguments:
        input = BuildingInput(required=True)

    building = graphene.Field(BuildingType)

    @staticmethod
    def mutate(root, info, input=None):
        customer_instance = Customer.objects.get(pk=input.customer.id)
        if customer_instance :
            building_instance = Building.objects.get(customer=customer_instance)
            if building_instance:
                if 'year_built' in input:
                    building_instance.year_built = input.year_built
                if 'square_footage' in input:
                    building_instance.square_footage = input.square_footage
                if 'number_of_floors' in input:
                    building_instance.number_of_floors = input.number_of_floors
                if 'occupancy_status' in input:
                    building_instance.occupancy_status = input.occupancy_status
                if 'residence_type' in input:
                    building_instance.residence_type = input.residence_type
                if 'primary_heating_system' in input:
                    building_instance.primary_heating_system = input.primary_heating_system
                if 'secondary_heating_system' in input:
                    building_instance.secondary_heating_system = input.secondary_heating_system
                if 'hot_water_system' in input:
                    building_instance.hot_water_system = input.hot_water_system
                if 'temperature_setpoint' in input:
                    building_instance.temperature_setpoint = input.temperature_setpoint
                if 'annual_energy_bill' in input:
                    building_instance.annual_energy_bill = input.annual_energy_bill
                if 'annual_energy_consumption' in input:
                    building_instance.annual_energy_consumption = input.annual_energy_consumption
                if 'customer' in input:
                    building_instance.customer = customer_instance
            
                building_instance.save()
        
                
                return UpdateBuildingByCustomerId(building=building_instance)
        return UpdateBuildingByCustomerId(building=None)




### Estimates

class EstimateType(DjangoObjectType):
    class Meta:
        model = Estimate

class UserHeatPumpType(DjangoObjectType):
    class Meta:
        model = UserHeatPump


    
# Mutation to create an estimate based on the selection of heat pumps in the user catalogue (UserHeatPumps)
class CreateEstimate(graphene.Mutation):
    class Arguments:
        customer_id  = graphene.Int(required=True)
        user_heat_pumps_ids = graphene.List(graphene.Int, required=True)

    estimates = graphene.List(EstimateType)
    customer = graphene.Field(CustomerType)

    @staticmethod
    def mutate(root, info, customer_id, user_heat_pumps_ids):
        user_heat_pumps  = UserHeatPump.objects.filter(id__in=user_heat_pumps_ids)
        

        if len(user_heat_pumps) != len(user_heat_pumps_ids):
            raise GraphQLError('Invalid User Heat Pump Ids')
        
        #Get the customer instance
        customer = Customer.objects.get(pk=customer_id)
        print(customer)

        if customer:
            # create the estimates instances
            estimates = []
            for user_heat_pump in user_heat_pumps:
                try :
                    print(user_heat_pump)
                    print(customer)
                    print(user_heat_pump.price)
                    estimate_instance = Estimate(user_heat_pump=user_heat_pump, customer=customer, price=user_heat_pump.price, state_subsidy_amount=0, energy_certificate_amount=0)
                    print(estimate_instance)
                    estimate_instance.save()
                    estimates.append(estimate_instance)
                except ValueError as e :
                    print("Error: ", e)
                    raise GraphQLError('An estimate already exists for this user heat pump and customer')
            
            return CreateEstimate(estimates=estimates, customer=customer)
        return CreateEstimate(estimates=None, customer=None)



#query 
class Query(graphene.ObjectType):
    customers = graphene.List(CustomerType)
    customer_by_id = graphene.Field(CustomerType, id=graphene.Int(required=True))

    def resolve_customers(self, info):
        return Customer.objects.all()

    def resolve_customer_by_id(self, info, id):
        try :
            return Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            return None

    buildings = graphene.List(BuildingType)
    building_by_customer_id = graphene.Field(BuildingType, customer=graphene.Int(required=True))

    # query to return the heat loss of a building
    building_heat_loss = graphene.Float(id=graphene.Int(required=True))

    def resolve_buildings(self, info):
        return Building.objects.all()
    
    def resolve_building_by_customer_id(self, info, customer):
        try :
            return Building.objects.get(customer=customer)
        except Building.DoesNotExist:
            return None

    def resolve_building_heat_loss(self, info, id):
        try :
            building = Building.objects.get(id=id)
            return building.heat_loss
        except Building.DoesNotExist:
            return None

    estimates = graphene.List(EstimateType)
    estimate_by_customer_id = graphene.Field(EstimateType, customer=graphene.Int(required=True))

    def resolve_estimates(self, info):
        return Estimate.objects.all()

    def resolve_estimate_by_customer_id(self, info, customer):
        try :
            return Estimate.objects.get(customer=customer)
        except Estimate.DoesNotExist:
            return None


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    update_customer_by_id = UpdateCustomerById.Field()

    create_building = CreateBuilding.Field()
    update_building_by_customer_id = UpdateBuildingByCustomerId.Field()

    create_estimate = CreateEstimate.Field()



schema = graphene.Schema(query=Query, mutation=Mutation)
