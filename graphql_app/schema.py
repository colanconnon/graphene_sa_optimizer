from graphene import Schema
from .queries import Query
from .mutations import Mutation


schema = Schema(
    query=Query,
    mutation=Mutation
)
