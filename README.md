# Ding Lab Logo Proposal

A serious website to handle the logo competition in a professional way, that
is, strictly following the NIH grant application process.


## Getting Started

### Requirements

- Git
- Python 3.5+

### Set up a Python Virtual Environment

#### Built-in `venv`

Create the virtual environment at `<repo>/venv`:

    python3 -m venv venv

To activate it:

    . venv/bin/activate

Or on Windows, use

    . venv\Scripts\activate.bat

### Install Dependencies

Use pip:

    pip install -r requirements.txt


### Set up Local Environment Variables and Database

Settings are stored in environment variables via [django-environ]. The
quickiest way to start is to copy `local.sample.env` into `local.env`:

    cp src/logo_proposal/settings/local.sample.env src/logo_proposal/settings/local.env

Then edit the `SECRET_KEY` line in `local.env`, replacing `{{ secret_key }}` into any [Django Secret Key] value. An example:

    SECRET_KEY=n04w~h1[GRQbbgLPRaAmKz^_F)pH40dytHRQ)49

After that, just run the migration.


### Go Develop

Change to the `src` directory:

    cd src

Then run the database migration.

    python manage.py migrate

Run the development server

    python manage.py runserver

and a local SMTP server so all email sending will be captured

    fab start_smtp


## License

Release under MIT License. A great portion of code is adapted from [PyCon Taiwan 2016 website]'s source code under license MIT.


[django-environ]: http://django-environ.readthedocs.org/en/latest/
[Django Secret Key]: http://www.miniwebtool.com/django-secret-key-generator/
[PyCon Taiwan 2016 website]: https://github.com/pycontw/pycontw2016
