from pytest import MonkeyPatch
import strawberry
from modelresolvers.schema import Schema, ModelResolvers


def test_create_strawberry_root_mutation(monkeypatch: MonkeyPatch):
    root_mutation = type("Mutation", (), {})

    strawberry_root_mutations = strawberry.type(root_mutation)
    monkeypatch.setattr(
        "modelresolvers.schema.Schema.create_strawberry_root_mutation",
        lambda: strawberry_root_mutations,
    )

    output = Schema.create_strawberry_root_mutation()
    assert output == strawberry_root_mutations


def test_create_strawberry_root_query(monkeypatch: MonkeyPatch):
    root_query = type("Query", (), {})

    strawberry_root_queries = strawberry.type(root_query)
    monkeypatch.setattr(
        "modelresolvers.schema.Schema.create_strawberry_root_query",
        lambda: strawberry_root_queries,
    )

    output = Schema.create_strawberry_root_query()
    assert output == strawberry_root_queries


def test_group_by_opr_type():
    @strawberry.type
    class User:
        first_name: str
        last_name: str

    @strawberry.type
    class Post:
        content: str

    user_resolvers = ModelResolvers()

    @user_resolvers.query(name="user")
    def get_user() -> User:
        return User(first_name="John", last_name="Doe")

    @user_resolvers.mutation(name="create_user")
    def create_user(first_name: str, last_name: str) -> User:
        return User(first_name, last_name)

    post_resolvers = ModelResolvers()

    @post_resolvers.query(name="post")
    def get_post() -> Post:
        return Post(content="First post")

    @post_resolvers.mutation(name="create_post")
    def create_post(content: str) -> Post:
        return Post(content)

    schema = Schema(models_resolvers=[user_resolvers, post_resolvers])
    queries = {"user": get_user, "post": get_post}
    mutations = {
        "create_user": create_user,
        "create_post": create_post,
    }
    expected = queries, mutations
    output = schema.group_by_opr_type()
    assert expected == output
