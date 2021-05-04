# fastapi-redis

[![license](https://img.shields.io/github/license/grillazz/fastapi-redis)](https://github.com/grillazz/fastapi-redis/blob/main/LICENSE)

### Project Description
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


### How to Setup
To build , run and test and more ... use magic of make help to play with this project.
```shell
make help
```
and you receive below list:
```text
black                Apply black in project code
build                Build project with compose
clean                Reset project containers with compose
down                 Stop project containers with compose
flake8               Flake8 checks on project code
help                 Show this help
isort                Sort imports in project code
lock                 Refresh pipfile.lock
mypy                 Run mypy checks on project code
requirements         Refresh requirements.txt from pipfile.lock
test-cov             Run project unit tests with coverage
up                   Run project with compose
```
### How to Play
1. Download exmaple JSON form PubChem database i.e. COVID-19 Disease Map here on this link:
   https://pubchem.ncbi.nlm.nih.gov/#query=covid-19
   
2. Add SMILES to Redis Hash with `/api/smiles/add-to-hash` endpoint
    ```shell
    curl --location --request POST 'http://0.0.0.0:8080/api/smiles/add-to-hash?redis_hash=covid-19-canonical' \
    --header 'Content-Type: application/json' \
    --data-binary '@/fastapi-redis/PubChem_compound_text_covid-19_records.json'
    ```
    and get response like below with `201 Created`
    ```json
    {
        "number_of_inserted_keys": 2364,
        "hash_name": "covid-19-canonical"
    }
    ```
3. Compare SMILES code to list loaded in previous step on Redis Hash with `/api/smiles/compare-to-hash` endpoint
    ```shell
    curl --location --request GET 
   'http://0.0.0.0:8080/api/smiles/compare-to-hash?compound=CCC(CC)COC(=O)C(C)NP(=O)(OCC1C(C(C(O1)(C%23N)C2=CC=C3N2N=CN=C3N)O)O)OC4=CC=CC=C4&redis_hash=covid-19-canonical'
   ```
   and get response like below with `201 Created`
   ```json
   {
        "number_of_smiles_to_compare": 2364,
        "similarity": {
            "CCC(CC)COC(=O)[C@H](C)N[P@](=O)(OC[C@@H]1[C@H]([C@H]([C@](O1)(C#N)C2=CC=C3N2N=CN=C3N)O)O)OC4=CC=CC=C4": 1.0,
            "CCC(CC)COC(=O)C(C)NP(=O)(OCC1C(C(C(O1)(C#N)C2=CC=C3N2N=CN=C3N)O)O)OC4=CC=CC=C4": 1.0,
            "C1=C2C(=NC=NN2C(=C1)C3(C(C(C(O3)COP(=O)(O)O)O)O)C#N)N": 0.8964264082374318,
            "C1=C2C(=NC=NN2C(=C1)[C@]3([C@@H]([C@@H]([C@H](O3)COP(=O)(O)O)O)O)C#N)N": 0.8964264082374318,
            "C1=C2C(=NC=NN2C(=C1)[C@]3([C@@H]([C@@H]([C@H](O3)CO)O)O)C#N)N": 0.8740109555690809,
            "C1=C2C(=NC=NN2C(=C1)C3(C(C(C(O3)CO)O)O)C#N)N": 0.8740109555690809
       }
   }
   ```

### Backbone
Beside of using latest and greatest version of [Redis](https://redis.io/) with it robustness, powerfulness and speed
there is [FastAPI](https://fastapi.tiangolo.com/) (modern, fast (high-performance), 
web framework for building APIs with Python 3.6+ based on standard Python type hints.) already reviewed
on [thoughtworks](https://www.thoughtworks.com/radar/languages-and-frameworks?blipid=202104087)


