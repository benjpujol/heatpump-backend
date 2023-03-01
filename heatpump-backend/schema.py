from graphene import ObjectType, Schema
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from mainapp.schema import Query as Query1
from mainapp.schema import Mutation as Mutation1
from subsidies.schema import Query as Query2



# Define the root query and mutation for the combined schema
class Query(Query1, Query2, ObjectType):
    pass


class Mutation(Mutation1, ObjectType):
    pass


# Create the schema and add the root query and mutation to it
schema = Schema(query=Query, mutation=Mutation)
