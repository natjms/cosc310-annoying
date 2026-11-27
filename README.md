# Milestone 2+ Submission
Food Delivery application with a Svelte/Preact frontend and a FastAPI-based backend that uses .json for data persistence.

## Team Name
Our team name is simply 'Annoying Team'.

## Required Python version
The Python version needs to be >= 3.13.5

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
python -m venv .venv && source .venv/bin/activate
```

### Dependency installation
With the venv activated: `pip install -r requirements.txt`

### Configuration
This project uses a .env (dotenv) file for configuration. An example `.env` file is provided
at `example.env`. Before running the application you must copy this file to
`.env` at the repo root and edit it accordingly. On \*Nix:

```bash
cp example.env .env
```

To make development easier, the backend prints what data directory was passed to it on startup,
and `.env.dev` can be created to set the location of an alternative data directory, similar to `example.env` above.

Note: eventually the application will provide a way to generate initial representative data.
In the meantime, you will have to manually keep track of your changes, if any, to the repsentative data.


## How to start the application

###Backend:
-From the project root, run `python -m fastapi dev`
-Visit http://localhost:8000/docs

###Frontend: 
This is provided as a Vite application. There are 2 front-ends, one that uses 
Preact and one that uses Svelte. The instructions are similar between both, and currently
the Svelte frontend is the one that is served by default.

```
cd web
npm install
npm run dev
```
This starts the frontend. 

A .env file must be located at `web/.env` with the following contents for the frontend to work properly:
```
VITE_API_BASE_URL='http://localhost:8000/api/'
```
Change the above URL as necessary, and ensure data is present in `data/`. Refer to the backend env instructions above.


## API endpoint paths (top-level; see design/ for further details)
```bash
/docs
/api/
/api/health
```

## /docs path
It is exposed by default. The path is `127.0.0.1:8000/docs`

## Location of bundled data
Assuming '/' is the project root diretory: `/data/`

## How to run tests
run: `python -m pytest --doctest-modules` from the project root

## Brief repository structure
We decided to not deviate much from the conventional root structure for layered FastAPI projects. A top level overview of the project root is present below:

```bash
root/app <- contains the backend (api, repositories, schemas/models, services) 
root/tests <- houses the tests along with their data
root/scrum <- has team agreement, scrum and other project planning related data
```

The output of the `ls -R` command on Linux (see: `tree` command on Windows) is attached below. This recursively lists the directories that descend from the current directory below:

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
