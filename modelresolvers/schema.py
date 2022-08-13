import strawberry
from strawberry import Schema as StrawberrySchema

from modelresolvers.modelresolvers import ModelResolvers


class Schema:
    def __init__(self, models_resolvers):
        self._queries = {}
        self._mutations = {}
        self.group_by_opr_type(models_resolvers)
        self.strawberry_schema = StrawberrySchema(
            query=self.create_strawberry_root_query(),
            mutation=self.create_strawberry_root_mutation(),
        )

    def group_by_opr_type(self, models_resolvers: list[ModelResolvers]):
        for model_resolvers in models_resolvers:
            for type_, res in model_resolvers._queries.items():
                self._queries[type_] = res

            for type_, res in model_resolvers._mutations.items():
                self._mutations[type_] = res

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
