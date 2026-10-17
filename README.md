# Milestone 1 Submission
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

Visit http://localhost:8000/web/

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
We decided to not deviate much from the example root structure. I have attached a top level overview from the project root below:

```bash
root/app <- contains the backend (api, repositories, schemas/models, services) 
root/tests <- houses the tests along with their data
root/scrum <- has team agreement, scrum and other project planning related data
```

I have also attached the output of the `ls -R` command on Linux which is similar to the `tree` command on Windows, and recursively lists the directories descending from the current directory below:

```bash
. (aka Project Root)
app/  example.env  README.md  requirements.txt  scrum/  tests/

./app:
api/  exceptions.py  __init__.py  main.py  models/  repositories/  services/

./app/api:
__init__.py  routes/

./app/api/routes:
health.py  __init__.py  menu.py  restaurant.py

./app/models:
__init__.py  menu.py  restaurant.py

./app/repositories:
__init__.py  restaurant.py

./app/services:
__init__.py  restaurant.py

./scrum:
design.md  media/  team-agreement.md

./scrum/media:
entity-relationship-diagram.png  menu-data-flow-diagram.png  order-data-flow-diagram.png  restaurant-data-flow-diagram.png

./tests:
data/  repositories/

./tests/data:
cuisines.json  deliveries.json  orders.json  restaurants.json  users.json

./tests/repositories:
test_get_repository_data_file_path.py

```
