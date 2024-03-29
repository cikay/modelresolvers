Create virtual environment with 3.10 since modelresolvers require 3.10 and above

```
pipenv --python 3.10
```
Activate virtual environment

```
pipenv shell
```

Install modelresolvers

```
pipenv install modelresolvers
```


```py title="main.py"
import strawberry

from modelresolvers import ModelResolvers, Schema

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
    user = User(firstname=firstname, lastname=lastname)
    users.append(user)
    return user
```

We are going to run the app by strawberry so we need strawberry schema. modelresolvers Schema converts
its schema to strawberry schema. modelresolvers Schema has an attribute called `strawberry_schema`. So we will
run the app based on strawberry schema

```py
schema = Schema(models_resolvers=[user_resolvers]).strawberry_schema
```

The entire code is below.

```py title="main.py"
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
    user = User(firstname=firstname, lastname=lastname)
    users.append(user)
    return user


schema = Schema(models_resolvers=[user_resolvers]).strawberry_schema
```

Run the app in your terminal

```
strawberry server main
```

Go to `http://0.0.0.0:8000/graphql` and run your mutations and queries.
