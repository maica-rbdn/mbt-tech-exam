## Description:
Tech used: Python (Flask) v3.7.4, HTML (no frameworks), ORM SQLAlchemy (NoSQL)
App needed to be installed: Postman => for creating and fetching roles, permissions and mappings

## Diagram

[ERD](https://drive.google.com/file/d/1m2gEGQEVJLg7JmyPKP2T86vOfB8gwQVD/view?usp=sharing)

## Install the following:
You may use virtual env

```
python3 -m venv .venv
source .venv/bin/activate
```

Then install the following
```
pip3 install flask
pip3 install Flask Flask-SQLAlchemy
```

## Run command in the project terminal:
```
flask --app app run
```

## After succcessful run:
Go to the localhost to create the local db => Required to be able to create all needed database.
If an error occurred, try to reload the page again.
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

## If access denied after retrying:
Open a new tab.
Type the url in the search box:
```
chrome://net-internals/#dns
```
Hit the “Clear host cache” button.
And you are done as DNS is flushed out.
Open another tab and type URL:
```
chrome://net-internals/#sockets
```
Click on the “Flush socket pools” button.
Close the Google chrome tab.


