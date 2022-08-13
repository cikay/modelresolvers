from pytest import MonkeyPatch
import strawberry
from modelresolvers.schema import Schema


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
