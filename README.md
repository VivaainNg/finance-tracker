# Personal Finance Tracker

## Basic Requirements/Pre-requisites

- [Python3](https://www.python.org/downloads/)
- [git](https://git-scm.com/downloads)


### Installing

A step by step guide on how to setup your local Python environment for this project.

0: Once you've installed git in your system, clone this repo into your local:
```bash
$ git clone git@github.com:VivaainNg/finance-tracker.git
```


1: Create a local Python venv(virtualenv) based on your environment's name `<envName>`:

```bash
$ python3 -m venv <envName>
```

2: Activate the `<envName>` virtual environment that you've just created from step above:

```
# On Windows (Command Prompt):
> <envName>\Scripts\activate

# On Windows (Powershell):
> .\<envName>\Scripts\Activate.ps1

# On Unix (Linux/macOS):
$ source <envName>/bin/activate
```

3: Install all the modules listed within requirements.txt in this repo into your newly-created virtual environment:

```bash
# <project_root> refers to the topmost folder right after cloning this repository
$ cd <project_root>
$ pip install -r requirements.txt
```

## Setup pre-commit
1: I use pre-commit to normalize the linters, formatters in this repo. Go ahead with:
```bash
$ pre-commit install # Only need to run once
$ pre-commit run --all-files
```


## Running Django web application on your local system:
1: Sync database based on latest DB's migration files (courtesy of Django's out-of-the-box ORM):

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

2: Jumpstart the Django web on your local:
```bash
$ python manage.py runserver
```

At this point, the app runs at `http://127.0.0.1:8000/`.

> Note: To use the app, please access the registration page and create a new user. After authentication, the app will unlock the private pages.

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
   |    |-- charts
   |    |-- dyn_api                      # APP Routing
   |    |-- dyn_dt                       # APP Models
   |    |-- pages                        # Tests
   |
   |-- requirements.txt                  # Project Dependencies
   |
   |-- env.sample                        # ENV Configuration (default values)
   |-- manage.py                         # Start the app - Django default start script
   |
   |-- ************************************************************************
```

<br />
<!---->
<!-- ## Deploy on [Render](https://render.com/) -->
<!---->
<!-- - Create a Blueprint instance -->
<!--   - Go to https://dashboard.render.com/blueprints this link. -->
<!-- - Click `New Blueprint Instance` button. -->
<!-- - Connect your `repo` which you want to deploy. -->
<!-- - Fill the `Service Group Name` and click on `Update Existing Resources` button. -->
<!-- - After that your deployment will start automatically. -->
<!---->
<!-- At this point, the product should be LIVE. -->
<!---->
<!-- <br /> -->
<!---->

## Resources

- **Black Dashboard Django's**
   - Repository: <https://github.com/creativetimofficial/black-dashboard-django>
   - Documentation: <https://demos.creative-tim.com/black-dashboard-django/docs/1.0/getting-started/getting-started-django.html>
- Django: <https://www.djangoproject.com/>
- DRF (for exposing RESTful API): <https://www.django-rest-framework.org/>

<br />

---

### TODO lists:

* [X] Guides on setting up on local (pre-requisites, etc...).

* [X] Create a requirements.txt to list out all the necessary Python modules.

* [ ] Implement unit-testing for views (using [APITestCase](https://www.django-rest-framework.org/api-guide/testing/#api-test-cases) from DRF).

* [ ] Implement documentations/steps on how to utilize the DRF's exposed API (preferably Swagger)

* [ ] Implement HTMX at frontend.

* [ ] Implement [DRF Router](https://www.django-rest-framework.org/api-guide/routers/) for mapping of URL with views.

* [ ] Setup CI/CD to automate workflows via [Github Actions YAML file](.github/workflows/github-actions-ci.yml).

* [ ] Add codecoverage tools in Github Action's workflow.

* [ ] Implement service layer (Based on Two Scoops of Django).

* [ ] Change from pip to [uv](https://astral.sh/blog/uv).

---

## Licensing

- Copyright 2019 - present [Creative Tim](https://www.creative-tim.com/)
- Licensed under [Creative Tim EULA](https://www.creative-tim.com/license)
