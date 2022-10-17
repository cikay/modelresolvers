import strawberry
from strawberry import Schema as StrawberrySchema

from modelresolvers.modelresolvers import ModelResolvers


class Schema:
    def __init__(self, models_resolvers: list[ModelResolvers]):
        self.models_resolvers = models_resolvers
        self._queries, self._mutations = self.group_by_opr_type()
        self.strawberry_schema = StrawberrySchema(
            query=self.create_strawberry_root_query(),
            mutation=self.create_strawberry_root_mutation(),
        )

    def group_by_opr_type(self):
        queries = {}
        mutations = {}
        for model_resolvers in self.models_resolvers:
            queries |= model_resolvers._queries
            mutations |= model_resolvers._mutations

        return queries, mutations

    def create_strawberry_root_query(self):
        resolvers = {
            name: strawberry.field(resolver) for name, resolver in self._queries.items()
        }
        query = type("Query", (), resolvers)
        return strawberry.type(query)

    def create_strawberry_root_mutation(self):
        resolvers = {
            name: strawberry.mutation(resolver)
            for name, resolver in self._mutations.items()
        }
        mutation = type("Mutation", (), resolvers)
        return strawberry.type(mutation)
