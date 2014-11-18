System of Record
================

[![Build Status](https://travis-ci.org/LandRegistry/system-of-record.svg)](https://travis-ci.org/LandRegistry/system-of-record)

[![Coverage Status](https://img.shields.io/coveralls/LandRegistry/system-of-record.svg)](https://coveralls.io/r/LandRegistry/system-of-record)

## Storage of minted title entries

Service to create new versions of a title, hashed and signed.

### Try it out

Check out the repo. Then cd into the repo directory:

 Create a virtualenv (assuming you have virtualenv and virtualenvwrapper installed)

 ```
 mkvirtualenv system-of-record
 ```

 **Install some stuff**

 Install dependencies into the virtualenv

```
pip install -r requirements
```

#### Create a local Postgres db.

Assuming you have postgres 9.3 installed and running

##### OSX

```
createuser -s sysofrec
```
 That should work out of the box if you're on OSX using Postgres.app.

Create the sysofrec database
```
createdb -U sysofrec -O sysofrec sysofrec -T template0
```

Export a couple of environment variables

For the moment export the following:

```
export SETTINGS='config.Config'
export  DATABASE_URL='postgresql://localhost/sysofrec'
```

For the future you can create a .env file alongside the Profile with this content

```
SETTINGS=config.Config
DATABASE_URL=postgresql://localhost/sysofrec
```

It's a special file that if sitting alongside a Procfile, foreman will use to create the environment variables contained. So anytime you run using
the run.sh (which uses foreman) these will be set.

###### psycopg on Mac

If ```pip install -r requirements.txt``` fail on Mac, try pointing your PATH to Postgres.App:


    export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/9.3/bin

#####  Linux

The intial createuser may ask for a password and whether user should be super user. If so, add a password and and say yes to give
all privileges. This is only for local development so let's be relaxed. If you have created the user with a password change the last line of .env to this:

```
export export DATABASE_URL='postgresql://sysofrec:password@localhost/sysofrec'
```

#### Create the schema

There's an intial migration script in the project created using Flask-Migrate so you just need to call the following

```
python manage.py db upgrade
```

On heroku run this
```
heroku run python manage.py db upgrade --app lr-system-of-record
```

Run the upgrade command whenever you have additional migrations


### Install and start Redis to enqueue data for the feeder


```
brew install redis
```

```
redis-server
```

#### Run the app

```
./run.sh
```

**PUT some data**

```
curl -X PUT -H "Content-Type: application/json"  http://localhost:8000/titles/TEST_AB1234567 \
-d '{ "title":
        {
            "title_number": "TEST_AB1234567",
            "proprietors": [
                {
                    "first_name": "firstname",
                    "last_name": "lastname"
                }
            ],
            "property" : {
                "address": {
                    "house_number": "house number",
                    "road": "road",
                    "town": "town",
                    "postcode": ""
                },
                "tenure": "freehold",
                "class_of_title": "absolute"
            },
            "payment": {
                "price_paid": "12345",
                "titles": ["TEST_AB1234567"]
            }
        }
    }'
```


**GET some data**

```
curl -H "Accept: application/json"  http://localhost:8000/titles/TEST_AB1234567
```

Which should return:

```
{
  "title": {
    "data": "{u'title': {u'proprietors': [{u'first_name': u'firstname', u'last_name': u'lastname'}], u'title_number': u'TEST_AB1234567', u'property': {u'tenure': u'freehold', u'class_of_title': u'absolute', u'address': {u'house_number': u'house number', u'town': u'town', u'postcode': u'', u'road': u'road'}}, u'payment': {u'titles': [u'TEST_AB1234567'], u'price_paid': u'12345'}}}",
    "number": "TEST_AB1234567"
  }
}
```

### Seeing everything in the store

```
curl -H "Accepts application/json"  http://localhost:8000/titles
```


### Run the tests

```
export SETTINGS='config.TestConfig'
py.test
```

### TODO

Check incoming title entry for integrity using public key.
