# modelresolvers

modelresolvers is a python grapqhl package(inspired by [type-graphql](https://typegraphql.com/)) on top of
[strawberry](https://github.com/strawberry-graphql/strawberry) to structure your project by feature(model) instead of operation type(mutation and query)
to manage it easier.

### Requirement

python3.10 and above

### Install by the following command

`pip install modelresolvers`


### Examples

Put the following example to main.py

```py
import strawberry
from modelresolvers import ModelResolvers, Schema


user_resolvers = ModelResolvers()


@strawberry.type
class User:
    firstname: str
    lastname: str


users = [
    User(firstname="John", lastname="Doe"),
    User(firstname="Jahe", lastname="Doe"),
]


@user_resolvers.query(name="user")
def user() -> User:
    return users[0]


@user_resolvers.mutation(name="add_user")
def add_user(firstname: str, lastname: str) -> User:
    user = User(firstname, lastname)
    users.append(user)
    return user


schema = Schema(models_resolvers=[user_resolvers]).strawberry_schema
```

Run `strawberry server main`

Go to `http://0.0.0.0:8000/graphql` and try your mutations and queries.
