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