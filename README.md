# Personal Finance Tracker
[![Django CI](https://github.com/VivaainNg/finance-tracker/actions/workflows/django-ci.yml/badge.svg)](https://github.com/VivaainNg/finance-tracker/actions/workflows/django-ci.yml)

## Basic Requirements/Pre-requisites

- [Python3](https://www.python.org/downloads/) (Version 3.12+ preferably, in my case I'm specifically using [version 3.12.2](https://www.python.org/downloads/release/python-3122/))
- [git](https://git-scm.com/downloads)


### Installing

A step by step guide on how to setup your local Python environment for this project.

1. Once you've installed git in your system, clone this repo into your local:
```bash
$ git clone git@github.com:VivaainNg/finance-tracker.git
```

<br />


2. Create a local Python venv(virtualenv) based on your environment's name `<envName>`:

```bash
$ python3 -m venv <envName>
```

<br />

3. Activate the `<envName>` virtual environment that you've just created from step above:

```
# On Windows (Command Prompt):
> <envName>\Scripts\activate

# On Windows (Powershell):
> .\<envName>\Scripts\Activate.ps1

# On Unix (Linux/macOS):
$ source <envName>/bin/activate
```

<br />

4. Install all the modules listed within requirements.txt in this repo into your newly-created virtual environment:

```bash
# <project_root> refers to the topmost folder right after cloning this repository
$ cd <project_root>
$ pip install -r requirements.txt
```

<br />

## Running Django web application on your local system:
5. Sync database based on latest DB's migration files (courtesy of Django's out-of-the-box ORM):

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

> Run the following script to populate DB with some Categories.

```bash
$ python manage.py initialize_category -c
```

<br />

6. Jumpstart the Django web on your local:
```bash
$ python manage.py runserver
```

At this point, the app runs at `http://127.0.0.1:8000/`.

> Note: To use the app, please access the registration page and create a new user. After authentication, the app will unlock the private pages.


<br />

## Run unit tests over the REST API:
- To simply run a overall test:
```bash
$ python manage.py test apps.api -v 2
```

<br />

## Continuous Integration (CI)
- For continuous integration, a [Github Action](https://github.com/features/actions) configuration `.github/workflows/django-ci.yml` is included.

<br />

## Setup Linters/formatters/code styles
- I use pre-commit to standardize the linters, formatters in this repo. Go ahead with:
```bash
$ pre-commit install # Only need to run once
$ pre-commit run --all-files
```

- To standardize the Django templates format across the HTML files via `.djlintrc`, run:
```bash
$ djlint templates/ --reformat
```
<br />

## File Structure
Within the download you'll find the following directories and files:

```bash
< PROJECT ROOT >
   |
   |-- config/
   |    |-- settings.py                  # Project Configuration
   |    |-- urls.py                      # Project Routing
   |
   |-- apps/
   |    |-- charts                       # Serve Charts
   |    |-- apis                         # API endpoints & scripts
   |    |-- pages                        # Serve UI pages and storing app models
   |
   |-- requirements.txt                  # Project Dependencies
   |
   |-- env.sample                        # ENV Configuration (default values)
   |-- manage.py                         # Start the app - Django default start script
   |
   |-- ************************************************************************
```

<br />

## Resources

- [Black Dashboard Django](https://github.com/creativetimofficial/black-dashboard-django): The main inspiration & template themes that I've been using for this project.
- [Django](https://github.com/django/django): Base framework for the backend of this project.
- [django-rest-framework](https://github.com/encode/django-rest-framework): For exposing RESTful API on top of Django framework.
- [drf-spectacular](https://github.com/tfranzel/drf-spectacular): For generating OpenAPI 3 schema on top of DRF.
- [ruff](https://github.com/astral-sh/ruff) with [pre-commit](https://github.com/pre-commit/pre-commit): To standardize proper linting/formatting code styles.
- [django-tables2](https://github.com/jieter/django-tables2): For ease of generating HTML datatables on the front-end templates.

<br />

---

### TODO lists:

* [X] Guides on setting up on local (pre-requisites, etc...).

* [X] Create a requirements.txt to list out all the necessary Python modules.

* [X] Implement unit-testing for views (using [APITestCase](https://www.django-rest-framework.org/api-guide/testing/#api-test-cases) from DRF).

* [X] Implement documentations/steps on how to utilize the DRF's exposed API (preferably Swagger-like docs).

* [ ] Update to proper graphs/charts in dashboard.

* [X] Implement proper CBV to replace current FBV when rendering dynamic tables.

* [ ] Resolve corrupt session data issues.

* [ ] Implement "forget password" features.

* [X] Implement [DRF Router](https://www.django-rest-framework.org/api-guide/routers/) for mapping of URL with views.

* [X] Setup CI to automate workflows via [Github Actions YAML file](.github/workflows/github-actions-ci.yml).

* [ ] Change from pip to [uv](https://astral.sh/blog/uv).

---

## Licensing

- Copyright 2019 - present [Creative Tim](https://www.creative-tim.com/)
- Licensed under [Creative Tim EULA](https://www.creative-tim.com/license)
