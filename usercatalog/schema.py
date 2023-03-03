from graphene_django import DjangoObjectType
import graphene
from .models import UserHeatPump
from catalog.models import HeatPump
from django.contrib.auth.models import User
from graphql import GraphQLError

import logging
logging.basicConfig(filename="heatpump-backend.log", level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')

class UserType(DjangoObjectType):
    class Meta:
        model = User

        
class UserHeatPumpType(DjangoObjectType):
    class Meta:
        model = UserHeatPump
    
    user = graphene.Field(UserType)

class HeatPumpType(DjangoObjectType):
    class Meta:
        model = HeatPump




# create user heat pump mutation by user id and a list of heat pumps ids
class CreateUserHeatPump(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        heat_pump_ids = graphene.List(graphene.Int, required=True)
      

    user_heat_pump = graphene.Field(UserHeatPumpType)
    user = graphene.Field(UserType)
    heat_pumps = graphene.List(HeatPumpType)

    @staticmethod
    def mutate(root, info, user_id, heat_pump_ids ):
        # Get the HeatPump instances based on IDs
        
        heat_pumps = HeatPump.objects.filter(id__in=heat_pump_ids)
        
        if len(heat_pumps) != len(heat_pump_ids):
            raise GraphQLError('Invalid Heat Pump ID!')

        # Get the User instance based on user_id
        user = User.objects.get(id=user_id)

        if user:
            # Create the UserHeatPump instances
            user_heat_pumps = []
            for heat_pump in  heat_pumps.exclude(userheatpump__user=user): # exclude the heat pumps that the user has already added
                heat_pump_instance = HeatPump.objects.get(id=heat_pump.id)
                try :
                    user_heat_pump =  UserHeatPump(user=user, heat_pump=heat_pump_instance, price=heat_pump_instance.price, description=heat_pump_instance.description)
                    user_heat_pump.save()
                    user_heat_pumps.append(user_heat_pump)
                except ValueError as e:
                    raise GraphQLError('The user has already added this heat pump')

               

            return CreateUserHeatPump(user_heat_pump=user_heat_pumps[0], heat_pumps=heat_pumps)
        else:
            raise GraphQLError('Invalid User ID!')


# delete user heat pump mutation by user id and a list of heat pumps ids
class DeleteUserHeatPump(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        heat_pump_ids = graphene.List(graphene.Int, required=True)

    user = graphene.Field(UserType)
    heat_pumps = graphene.List(HeatPumpType)

    @staticmethod
    def mutate(root, info, user_id, heat_pump_ids):
        # Get the HeatPump instances based on IDs
        heat_pumps = HeatPump.objects.filter(id__in=heat_pump_ids)
        if len(heat_pumps) != len(heat_pump_ids):
            raise GraphQLError('Invalid Heat Pump ID!')

        # Get the User instance based on user_id
        user = User.objects.get(id=user_id)

        if user:
            # Delete the UserHeatPump instances
            for heat_pump in heat_pumps:
                user_heat_pump = UserHeatPump.objects.filter(user=user, heat_pump=heat_pump).first()
                if user_heat_pump:
                    user_heat_pump.delete()

            return DeleteUserHeatPump(user=user, heat_pumps=heat_pumps)
        else:
            raise GraphQLError('Invalid User ID!')



class UpdateUserHeatPump(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        heat_pump_reference_code = graphene.String()
        heat_pump_id = graphene.Int()
        price = graphene.Float()
        description = graphene.String()

    user_heat_pump = graphene.Field(UserHeatPumpType)
    user = graphene.Field(UserType)
    heatPump = graphene.Field(HeatPumpType)

    @staticmethod
    def mutate(root, info, user_id, heat_pump_reference_code=None, heat_pump_id=None, price=None, description=None):
        if heat_pump_reference_code:
            # Get the UserHeatPump instance based on user and heat pump reference code
            user_heat_pump = UserHeatPump.objects.get(user_id=user_id, heat_pump__reference_code=heat_pump_reference_code)
        elif heat_pump_id:
            # Get the UserHeatPump instance based on user and heat pump id
            user_heat_pump = UserHeatPump.objects.get(user_id=user_id, heat_pump_id=heat_pump_id)
        else:
            raise Exception('Invalid Heat Pump Reference Code or ID!')

        # Update the UserHeatPump instance
        if price is not None:
            user_heat_pump.price = price
        if description is not None:
            user_heat_pump.description = description

        try:
            user_heat_pump.save()
        except Exception as e:
            raise Exception(e)
        
    

        return UpdateUserHeatPump(user_heat_pump=user_heat_pump)


# query
class Query(graphene.ObjectType):
    user_heat_pumps = graphene.List(
        UserHeatPumpType,
        user_id=graphene.Int(required=True))

    @staticmethod
    def resolve_user_heat_pumps(root, info, user_id):
        return UserHeatPump.objects.filter(user_id=user_id)

class Mutation(graphene.ObjectType):
    create_user_heat_pump = CreateUserHeatPump.Field()
    delete_user_heat_pump = DeleteUserHeatPump.Field()
    update_user_heat_pump = UpdateUserHeatPump.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)