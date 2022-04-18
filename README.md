# fastapi-redis


[![developer](https://img.shields.io/badge/Dev-grillazz-green?style)](https://github.com/grillazz)
![language](https://img.shields.io/badge/language-python-blue?style)
[![license](https://img.shields.io/github/license/grillazz/fastapi-redis)](https://github.com/grillazz/fastapi-redis/blob/main/LICENSE)
![visitors](https://visitor-badge.laobi.icu/badge?page_id=grillazz.fastapi-redis")
[![CI](https://img.shields.io/github/workflow/status/grillazz/fastapi-redis/Unit%20Tests/main)](https://github.com/grillazz/fastapi-redis/actions/workflows/build-and-test.yml)

![fastapi-redis](/static/mols.jpg)

### Project Description
Purpose of this showcase is integrate modern NoSQL backend Redis with FastAPI Python ASGI Framework
as API for chemical compounds extended analyze with [RDKit](https://github.com/rdkit/rdkit) Library.

Data set coming from pub chem database, and you can download example from COVID-19 Disease Map here on this link: https://pubchem.ncbi.nlm.nih.gov/#query=covid-19

Pydantic schema was created for PubChem Compounds. You can replace it with your own schema to accept other source of SMILES.

There is many chemical compound sets. Now we are all in days when COVID-19 Pandemic is out there.
We all want to know as much as possible about best cure..., and it is my project background.
Show power and robustness of Redis with speed of FastAPI and functionality of RDKit to deliver api 
which allow fast analyze chem molecules.

This showcase can be quickly integrated with other services via REST API and extended to deliver desired chem compound bakery.

Project as whole is build on FastAPI framework, Python 3.10, Redis.


### How to Setup
To build, run and test and more... use magic of make.
```shell
make help
```
and you receive below list:
```text
build                Build project with compose
clean                Reset project containers with compose
down                 Stop project containers with compose
format               Format project code.
help                 Show this help
lint                 Lint project code.
lock                 Refresh pipfile.lock
requirements         Refresh requirements.txt from pipfile.lock
safety               Check project and dependencies with safety https://github.com/pyupio/safety
test                 Run project unit tests with coverage
up                   Run project with compose
```
### How to Play
1. Download sample JSON from PubChem database i.e. COVID-19 Disease Map here on this link:
   https://pubchem.ncbi.nlm.nih.gov/#query=covid-19
   
2. Add SMILES to Redis Hash with `/smiles/add-to-hash` endpoint
    ```shell
    curl --location --request POST 'http://0.0.0.0:8080/smiles/add-to-hash?redis_hash=covid-19-canonical' \
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
   'http://0.0.0.0:8080/smiles/compare-to-hash?compound=CCC(CC)COC(=O)C(C)NP(=O)(OCC1C(C(C(O1)(C%23N)C2=CC=C3N2N=CN=C3N)O)O)OC4=CC=CC=C4&redis_hash=covid-19-canonical'
   ```
   and get response like below with `200 OK`
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
4. For REST API Documentation please use: `http://0.0.0.0:8080/docs`
    
5. Finally, you can use postman collection here [Postman Collection](https://github.com/grillazz/fastapi-redis/blob/main/postman/fastapi-redis.postman_collection.json)

### Backbone
Beside of using latest and greatest version of [Redis](https://redis.io/) with it robustness, powerfulness and speed
there is [FastAPI](https://fastapi.tiangolo.com/) (modern, fast (high-performance), 
web framework for building APIs with Python 3.10+ based on standard Python type hints.) already reviewed
on [thoughtworks](https://www.thoughtworks.com/radar/languages-and-frameworks?blipid=202104087).
[Aioredis 2.0](https://aioredis.readthedocs.io/en/latest/) is already implemented as redis client python async library.
Special thanks going to maintainers of [rdkit-pypi](https://github.com/kuelumbus/rdkit-pypi).

Hope you enjoy it.

### Change Log
- 16 APR 2022 aioredis replaced with redis.asyncio