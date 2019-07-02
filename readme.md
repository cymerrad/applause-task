# How to run the project
Python virtual env, frozen reqs, migrations
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

# Quick links
1. [views.py](the_platform/tester_matching/views.py)
1. [models.py](the_platform/tester_matching/models.py)
1. [tests.py](the_platform/tester_matching/tests.py)

# Rationales and caveats
Woven into the code, are comments about possible extensions or solutions to potential problems, that might arise with further development.

These are general forewarnings for the reader:
- Function comments are free-style. If I'd be generating a documentation, then I'd conform to some doc-gen standard. Also I don't have a team to share a common coding style with.
- Comments generally describe my thought process and choices; they may be lenghty.

I've made some bold assumptions about the task. These are:
- Bare-bones Django - I'm not using any frameworks or packages that would introduce unnecessary dependencies
- Keeping it minimal - I expose only one endpoint that solves the task and I'm doing just basic input validation on POST requests
- Database choice should be transparent, so all the operations performed on the database are done with the most generic Django's ORM methods
- Database choice shouldn't matter for this exercise (small size of data), so I stick with SQLite3
- Table schemas won't change anytime soon, so they are _mostly_ hardcoded - however, I've left some notes in the views.py file on how I'd solve the issue of hardcoded strings
- CSV files represent database structure **exactly** and I should conform to that, so field names are sometimes misleading, e.g. 'deviceId' in models.Bug should be just a 'device'
- Crux of the task is one SQL query, so I haven't bothered with separating views from the business logic - this way everything is contained inside one 150-ish LoC file.
- Tests are performed on the constant fixture (tester_matching/fixtures); all tests base upon easy observations on the data
- Attached fixture to the project comes from the CSV files; script that generates it doesn't produce primary keys in order - easy fix but it doesn't matter
- I've switched off timezones, because example data doesn't contain information about it and it disables warnings about "naivness"
- Return data has enough information to extract 'Experience' of the Testers, but I chose to hold the data in an unordered map - said operation can be always done on the front-end


# TODO
1. [x] Have the data stored in some convenient form, i.e. SQL database
1. [x] This suggest using something with ORM capabilities, let it be Django for simplicity
1. [x] Create a Django app for doing the business logic; this should be just a few SQL queries
1. [x] Simple API
