from graphene import ObjectType, Schema
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from mainapp.schema import Query as Query1
from mainapp.schema import Mutation as Mutation1
from subsidies.schema import Query as Query2
from heatloss.schema import Query as Query3
from heatloss.schema import Mutation as Mutation2
from catalog.schema import Query as Query4
from catalog.schema import Mutation as Mutation3



# Define the root query and mutation for the combined schema
class Query(Query1, Query2, Query3, Query4, ObjectType):
    pass


class Mutation(Mutation1, Mutation2,  ObjectType):
    pass


# Create the schema and add the root query and mutation to it
schema = Schema(query=Query, mutation=Mutation)
