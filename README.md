## Description:
Tech used: Python (Flask) v3.7.4, HTML (no frameworks), ORM SQLAlchemy (NoSQL)
App needed to be installed: Postman => for creating and fetching roles, permissions and mappings

## Diagram

[ERD](https://drive.google.com/file/d/1m2gEGQEVJLg7JmyPKP2T86vOfB8gwQVD/view?usp=sharing)

## Install the following:

```
pip3 install flask
pip3 install Flask Flask-SQLAlchemy
```

## Run command in the project terminal:
```
flask --app app run
```

## After succcessful run:
Go to the localhost to create the local db. Required to be able to create all needed database.
Take note: A test user with no mappings will be created once localhost/ has been called

Local host: http://127.0.0.1:5000

## API
For creating and fetching roles, permissions and mappings, see protocol specs below

GET => No response
POST => Use 'raw', and choose 'JSON'

# Sample requests
```
# PERMISSION
Path: localhost/api/permissions
Method: POST
Body (raw, JSON):
[
    {
        "name": "create"
    }
]

# ROLE
Path: localhost/api/roles
Method: POST
Body (raw, JSON):
[
    {
        "name": "staff"
    }
]

# ROLE-PERMISSION MAPPING
Path: localhost/api/roles/:id/permissions
Method: POST
Body (raw, JSON):
{
    "permissions": [1]
}

# USER-ROLE MAPPING
Path: localhost/api/users/:id/roles
Method: POST
Body (raw, JSON):
{
    "roles": [1]
}

```




