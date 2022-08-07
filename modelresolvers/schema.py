import strawberry
from strawberry import Schema as StrawberrySchema

from modelresolvers.modelresolvers import ModelResolvers


class Schema:
    def __init__(self, resolvers):
        self._queries = {}
        self._mutations = {}
        self.group_by_opr_type(resolvers)
        self.strawberry_schema = StrawberrySchema(
            query=self.create_strawberry_root_query()
        )

    def group_by_opr_type(self, resolvers: list[ModelResolvers]):
        for resolver in resolvers:
            for type_, res in resolver._queries.items():
                self._queries[type_] = res

            for type_, res in resolver._mutations.items():
                self._mutations[type_] = res

    def create_strawberry_root_query(self):
        resolvers = {
            name: strawberry.field(resolver) for name, resolver in self._queries.items()
        }
        return strawberry.type(type("Query", (), resolvers))
