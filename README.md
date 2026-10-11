# Milestone0 Submission
## Team Name
Our team name is simply 'Annoying Team'.

## Required Python version
The Python version is >= 3.13.5

## Setup instructions
Make sure you have the Python Headers installed (package name is `python-dev` on debian, ubuntu and so on) 

### Virtual-environment instructions
For Windows:

```
python -m venv .venv
.venv\Scripts\Activate.ps1
```

For \*Nix/Mac:

```
python -m venv .venv && .venv/bin/activate
```

### Dependency installation
With the venv activated: `pip install -r requirements.txt`

### Configuration

This project uses dotenv for configuration. An example `.env` file is provided
at `example.env`. Before running the application you must copy this file to
`.env` at the repo root and edit it accordingly. On \*Nix:

```
cp example.env .env
```

Note: eventually the application will provide ways to create data. For early
stages of development, you may use the existing `test/data/` folder which should
include enough example data to support basic usages. To use this in a way that
doesn't mess with the test suite, you should copy this directory to e.g.
`data/` and set that as your `DATA_DIR` in the env file.

## How to start the application
run: `python -m fastapi dev`
## API endpoint paths
/docs
/api/restaurants
/api/health

## /docs path
It is exposed by default. The path is `127.0.0.1:8000/docs`

## Location of representative data
Assuming '/' is the project root diretory: `/data/`

## How to run tests
run: `python -m pytest` from the project root

## Brief repository structure
We decided to not deviate much from the example root structure:

```
root/app <- contains the code (api, repositories, schemas, services)
root/app/api <- has the api routes 
root/data <- .json data
root/tests <- houses the tests
root/scrum <- has team agreement
```
