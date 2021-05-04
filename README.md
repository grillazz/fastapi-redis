#fastapi-redis

[![license](https://img.shields.io/github/license/grillazz/fastapi-redis)](https://github.com/grillazz/fastapi-redis/blob/main/LICENSE)

###Project Description
Purpose of this showcase project is integrate modenrs NoSQL backend Redis with Async Python Framework as API for 

Data set is comming from pub chem 


There is so mamy chem compud set but we all are noe in times where COVID-19 Pandemy is out there
and we all want to knwo as much as possibile about cure... so that is my project background.
Show power and robusteness of Redis with speed of FastAPI and funcinality of RDKit to deliver api 
which allow quicky analyze chem molecules.

For puprose of this hackatoon i added only two cases to load checm molecules to redis cache and to compare 
all moelcule which we alredy have with new one.

This can be really quickly integrate with other projects with REST API and extended to deliver desired chem compound bakery.

You can download example from COVID-19 Disease Map here on this link: https://pubchem.ncbi.nlm.nih.gov/#query=covid-19

Project as whole is build on python asyncio including REST, Redis connection and transactions and unit tests.


###How to Setup
To build , run and test and more ... use magic of make help to play with this project.
```shell
make help
```
and you receive below list:
```text
black                apply black in project code
build                Build project with compose
clean                Reset project containers with compose
down                 Stop project containers with compose
flake8               run flake8 checks on project code
help                 Show this help
isort                sort imports in project code
lock                 Refresh pipfile.lock
mypy                 run flake8 checks on project code
requirements         Refresh requirements.txt from pipfile.lock
test-cov             Run project unit tests with coverage
up                   Run project with compose
```
###How to Play

###Backbone
Beside of using latest and greatest version of [Redis](https://redis.io/) with it robustness, powerfulness and speed
there is [FastAPI](https://fastapi.tiangolo.com/) (modern, fast (high-performance), 
web framework for building APIs with Python 3.6+ based on standard Python type hints.) already reviewed
on [thoughtworks](https://www.thoughtworks.com/radar/languages-and-frameworks?blipid=202104087)


