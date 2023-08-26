### Project Setup

This project folder structure is like the below.

```
modelresolvers-fastapi-example
├── main.py
├── models
│   └── user.py
├── Pipfile
├── Pipfile.lock
└── resolvers
    └── user.py
```
Create a virtual environment with pipenv. Since `modelresolvers` requires Python3.10 
we create virtual env by specify Python version

```
pipenv --python 3.10
```

Install dependencies

```
pipenv install fastapi modelresolvers uvicorn
```

Activate virtual environment

```
pipenv shell
```

### Define User model

Create `user.py` under `models` folder

Import `strawberry` module to define GraphQL type

```py
import strawberry
```

Create User model

```py
@strawberry.type
class User:
    id: int | None
    firstname: str
    lastname: str
```

Since the model is a strawberry GraphQL type it must be decorated with `strawberry.type` decorator.

`id` field is optional because we want to set it automatically instead of getting it from the client.

The entire file code

```py
import strawberry


@strawberry.type
class User:
    id: int | None
    firstname: str
    lastname: str
```

### Resolvers

Create `user.py` under `resolvers` folder

Import modelresolvers

```py
from modelresolvers import ModelResolvers
```

Import the User model that we just created

```py
from models.user import User
```

Create ModelResolvers instance for user model resolvers

```py
user_resolvers = ModelResolvers()
```

Since we are simulating a real-world example we just define a user list

```py
users = [
    User(id=1, firstname="John", lastname="Doe"),
    User(id=2, firstname="Jane", lastname="Doe"),
]
```

Querying a single user

```py
@user_resolvers.query(name="user")
def user(id: int) -> User | None:
    return next((user for user in users if id == user.id), None)
```

To make a function a query we decorate it with the query decorator of ModelResolvers instance.
The name of the query decorator parameter is optional. The default is the function name that
is decorated which in this case is user. The function parameters and return parameter type
should be specified by type hints otherwise the strawberry raises error. The user function
searches the user based on the id it is not found it then returns `None`

```
@user_resolvers.query(name="users")
def get_users() -> list[User]:
    return users
```
`get_users` query returns all users available in the `users` list. Pay close attention to the function name and the name
argument of the query decorator. They are different. `get_users` query will be displayed as `users` in the GraphQL client UI.

Another ModelResolvers decorator is mutation.

```py
@user_resolvers.mutation(name="add_user")
def add_user(firstname: str, lastname: str) -> User:
    user = User(id=len(users) + 1, firstname=firstname, lastname=lastname)
    users.append(user)
    return user
```

firstname and lastname pass by GraphQL client. The id field is set on the backend side.
It is calculated as users list length plus 1. Then the created user returns to the client.


The entire file code

```py
from modelresolvers import ModelResolvers

from models.user import User


user_resolvers = ModelResolvers()

users = [
    User(id=1, firstname="John", lastname="Doe"),
    User(id=2, firstname="Jane", lastname="Doe"),
]


@user_resolvers.query(name="user")
def user(id: int) -> User | None:
    return next((user for user in users if id == user.id), None)


@user_resolvers.query(name="users")
def get_users() -> list[User]:
    return users


@user_resolvers.mutation(name="add_user")
def add_user(firstname: str, lastname: str) -> User:
    user = User(id=len(users) + 1, firstname=firstname, lastname=lastname)
    users.append(user)
    return user
```

### Main file

Create `main.py` file

Import Schema module from modelresolvers package

```py
from modelresolvers import Schema
```

Import FastAPI module from fastapi package

```py
from fastapi import FastAPI
```

Import GraphQLRouter module from strawberry package

```py
from strawberry.fastapi import GraphQLRouter
```

Import resolvers instance you have just created

```py
from resolvers.user import user_resolvers
```

When you create an modelresolvers Schema it will also create a strawberry schema as modelresolvers is based on strawberry
At this point, we need to strawberry schema rather than modelresolvers Schema. We get strawberry schema from modelresolvers schema

```py
schema = Schema(models_resolvers=[user_resolvers]).strawberry_schema
```

Create GraphQL router

```py
graphql_app = GraphQLRouter(schema)
```

Create fastapi app and add GraphQL router to the app

```py
app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
```

The entire file code

```py
from modelresolvers import Schema

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from resolvers.user import user_resolvers

schema = Schema(models_resolvers=[user_resolvers]).strawberry_schema

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
```

Run the application

```
uvicorn main:app --reload
```

Go to `http://127.0.0.1:8000/graphql` and run queries and mutations
