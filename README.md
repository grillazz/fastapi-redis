# fastapi-redis
Working example for FastAPI with Redis.

## Install pipenv for manage venvs and packages

You can find pipenv guide here: https://realpython.com/pipenv-guide/

Some advanced pipenv techniques you can find here: https://pipenv-fork.readthedocs.io/en/latest/advanced.html
```bash
pip3 install pipenv
```
#### To activate the virtual environment type
```bash
pipenv shell
```
#### Install default packages
```bash
pipenv install
```
#### Install dev packages
```bash
pipenv install --dev
```
#### add local .env file and update it to align to your local env if necessary
```bash
cp .env.example .env
```
#### Build project from docker
```bash
make build
```

#### run project
```bash
make up
```

#### refresh requirements.txt from pipfile.lock
```bash
pipenv lock -r > requirements.txt
```

#### for testing
just run `pytest`

## License

This project is licensed under the terms of the MIT license.

Using latest and greatest version of redis

Data set is comming from pub chem 

fast api what it is https://www.thoughtworks.com/radar/languages-and-frameworks?blipid=202104087

There is so mamy chem compud set but we all are noe in times where COVID-19 Pandemy is out there
and we all want to knwo as much as possibile about cure... so that is my project background.
Show power and robusteness of Redis with speed of FastAPI and funcinality of RDKit to deliver api 
which allow quicky analyze chem molecules.

For puprose of this hackatoon i added only two cases to load checm molecules to redis cache and to compare 
all moelcule which we alredy have with new one.

This can be really quickly integrate with other projects with REST API and extended to deliver desired chem compound bakery.
