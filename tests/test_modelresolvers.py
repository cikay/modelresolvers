import pytest
from modelresolvers.modelresolvers import ModelResolvers


def test_query_decorator():
    user_resolvers = ModelResolvers()

    @user_resolvers.query(name="get_user")
    def get_user() -> str:
        pytest.set_trace()
        assert user_resolvers._queries

    assert user_resolvers._queries == {"get_user": get_user}
