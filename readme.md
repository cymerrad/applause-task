# Init
```shell
virtualenv env
. env/bin/activate
# TODO: requirements.txt
```

# The plan
1. Have the data stored in some convenient form, i.e. SQL database
1. This suggest using something with ORM capabilities, let it be Django for simplicity
1. Create a Django app for doing the business logic; this should be just a few SQL queries
1. Firstly, create the API
1. Secondly, some simple web interface