# Anu

Predicting interactions among protein, DNA and RNA.

## Getting Started


## Developing

### Create a python virtual env

```bash
python -m venv venv     # create python environment
. ./venv/bin/activate    # activate python enviroment
```

### Install poetry

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```
or

```bash
pipx install poetry
```

### Install nox

```bash
pip install nox
```
### Nox

Run tests, lint check, type check, doc tests, coverage
```bash
nox
```
