# Init
```shell
virtualenv env
. env/bin/activate
pip install -r requirements.txt

cd the_platform
./manage.py makemigrations
./manage.py migrate
./manage.py loaddata tester_matching/fixtures/fixture.test.json
```

Generating fixtures
```shell
# assuming .csv's stored in data/
cd data
./csvs_to_fixtures.py
cd -
```

# Rationales and caveats
Woven into the code, are comments about possible extensions or solutions to potential problems, that might arise with further development.

I've made some bold assumptions about the task. These are:
- Bare-bones Django - I'm not using any frameworks or packages that would introduce unnecessary dependencies
- Keeping it minimal - I expose only one endpoint for solving the task and I'm doing just basic input validation
- Database choice should be transparent, so all the operations performed on the database are done with the most general Django's ORM methods
- Database choice shouldn't matter for this exercise, so I stick with SQLite3
- Table schemas won't change anytime soon, so they are _mostly_ hardcoded - however, I've left some notes in the views file on how I'd solve that issue
- Csv files represent database structure *exactly* and I should conform to that, so field names are sometimes misleading, e.g. 'deviceId' in models.Bug should be just a 'device'
- Crux of the task is one SQL query, so I haven't bothered with separating views from the business logic - this way everything is contained inside one 150-ish LoC file.
- Tests are performed on the constant fixture (tester_matching/fixtures); all tests base upon easy observations on the data
- Attached fixture to the project comes from the csv files; script that generates it doesn't produce primary keys in order - easy fix but it doesn't matter
- I've switched off timezones, because example data doesn't contain information about it and it disables warnings about "naivness"
- Function comments are free-style, if I'd be generating a documentation, then I'd conform to some standard (then why not doc-gen? It's one function basically, come one...)


# TODO
1. [x] Have the data stored in some convenient form, i.e. SQL database
1. [x] This suggest using something with ORM capabilities, let it be Django for simplicity
1. [x] Create a Django app for doing the business logic; this should be just a few SQL queries
1. [x] Simple API
1. [ ] Simple web interface
