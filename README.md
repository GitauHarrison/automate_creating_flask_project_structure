# Automated Flask Project Structure Helper

This folder contains an **executable helper script** that builds a ready-to-use Flask project structure for you, so you can start coding features instead of worrying about boilerplate and layout.

The script assumes you already understand Flask basics. Its goal is to automate project setup while keeping a clean separation of concerns and **uses blueprints by default** (`main`,`auth`, `admin`, `errors`).

Blueprints are a slightly more advanced concept in Flask. If you have little or no familiarity with blueprints, you should first read the official Flask blueprints documentation or a short tutorial, then come back to this helper so that the generated structure makes sense.

## Table of Contents

- [Overview](#overview)
- [What this helper does](#what-this-helper-does)
- [What this helper does *not* do](#what-this-helper-does-not-do)
- [Prerequisites](#prerequisites)
  - [1. Git & GitHub configuration](#1-git--github-configuration)
  - [2. Python version and pyenv / pyenv-virtualenv](#2-python-version-and-pyenv--pyenv-virtualenv)
  - [3. Poetry (if you choose the Poetry workflow)](#3-poetry-if-you-choose-the-poetry-workflow)
- [Supported workflows](#supported-workflows)
  - [Workflow A: pyenv + Poetry](#workflow-a-pyenv--poetry)
  - [Workflow B: pyenv + pyenv-virtualenv + requirements.txt](#workflow-b-pyenv--pyenv-virtualenv--requirementstxt)
- [How to use this helper](#how-to-use-this-helper)
  - [1. Clone this repository](#1-clone-this-repository)
  - [2. Run the script](#2-run-the-script)
  - [3. Choose your workflow](#3-choose-your-workflow)
  - [4. Answer the prompts](#4-answer-the-prompts)
- [Project structure generated](#project-structure-generated)
  - [Top-level layout](#top-level-layout)
  - [The `app/` package](#the-app-package)
  - [Templates](#templates)
  - [Static files](#static-files)
- [Installing dependencies](#installing-dependencies)
  - [Common dependency list](#common-dependency-list)
  - [If you chose pyenv + pyenv-virtualenv](#if-you-chose-pyenv--pyenv-virtualenv)
  - [If you chose pyenv + Poetry](#if-you-chose-pyenv--poetry)
- [Using the app](#using-the-app)
  - [Running the development server](#running-the-development-server)
  - [Database and migrations](#database-and-migrations)
- [After the scaffold](#after-the-scaffold)

## Overview

The main entrypoint is:

- `create_flask_project.py`

When you run it, it will interactively create a new Flask project folder in your **home directory** with a recommended structure and some starter code.

You can choose one of two environments:

1. **pyenv + Poetry**
2. **pyenv + pyenv-virtualenv + `requirements.txt`**

The project it generates follows **separation of concerns** using
blueprints:

- Application configuration in `config.py`.
- App package in `app/` with blueprints:
  - `app/main/` – public pages and the authenticated dashboard.
  - `app/auth/` – authentication routes, forms, and related helpers.
  - `app/admin/` – placeholder for admin-only views.
  - `app/errors/` – error handlers and error templates.
- Database models in `app/models.py`.
- Cross-cutting helpers in `app/utils/` (e.g. decorators).
- HTML templates in `app/templates/`.
- Static assets in `app/static/`.

## What this helper does

At a high level, running `create_flask_project.py` will:

- Prompt you for a project name, description and author.
- Create a new Flask project folder in your **home directory** with that name.
- Generate a blueprint-based Flask application inside `app/` (`main`, `auth`,
  `admin`, `errors`) plus configuration, templates, and static assets.
- Create documentation files (`README.md`, `CONTRIBUTING.md`,
  `CODE_OF_CONDUCT.md`, `LICENSE`) **for the generated project**, not for this
  automation script.
- Optionally create either a `pyproject.toml` (Poetry workflow) or a
  `requirements.txt` (pyenv-virtualenv workflow) inside the new project.
- Optionally add a small shell alias (`pf='poetry run flask'`) to your
  `~/.zshrc` or `~/.bashrc` if you choose the Poetry workflow.

The rest of this document explains these steps in more detail so that you know
exactly what is happening and can trust the automation.

- Detects your platform (macOS, Ubuntu, Windows, WSL) for light shell config
  decisions.
- Asks which workflow you want to use:
  - **Workflow A:** pyenv + Poetry.
  - **Workflow B:** pyenv + pyenv-virtualenv + `requirements.txt`.
- Checks prerequisites for your choice:
  - pyenv available on your `PATH`.
  - For Workflow A: `poetry` available on your `PATH`.
  - For Workflow B: `pyenv-virtualenv` available (via `pyenv virtualenvs`).
- If prerequisites are **not** met, it **does not proceed**. Instead, it points you to existing tutorials and automation repos to get ready.
- If prerequisites are met, it:
  - Prompts you for a project name (default: `flask_project`).
  - Prompts you for a short description.
  - Prompts you for the author name (used in LICENSE and docs).
  - Creates the project folder under your home directory.
  - Creates a full Flask starter structure (files and folders listed below).
  - For Poetry users: creates a `pyproject.toml` and an empty `poetry.lock` and appends an alias `pf='poetry run flask'` to your shell rc (`~/.zshrc` or `~/.bashrc`).
  - For `requirements.txt` users: creates a `requirements.txt` with the recommended baseline dependencies.

## What this helper does *not* do

- It does **not** install pyenv, pyenv-virtualenv, or Poetry for you.
- It does **not** configure Git or GitHub for you.
- It does **not** create or activate virtual environments.
- It does **not** install Python packages (no `pip install` or `poetry add`).

You stay in control of your environment. The script only scaffolds the Flask project **once your environment is ready**.

## Prerequisites

### 1. Git & GitHub configuration

First, ensure Git and GitHub are configured the way you like, especially if yo use multiple accounts. You can use:

- **[Automation] Git & GitHub configuration scripts:**  
  [`https://github.com/GitauHarrison/git_github_configurations`](https://github.com/GitauHarrison/git_github_configurations)
- **[Do it yourself] Guide: Stop Re-Typing Your Git & GitHub Config: Automate It on macOS and Linux:**  
  [`https://github.com/GitauHarrison/notes_on_general_topics/blob/main/02_automate_git_and_github_setup.md`](https://github.com/GitauHarrison/notes_on_general_topics/blob/main/02_automate_git_and_github_setup.md)

### 2. Python version and pyenv / pyenv-virtualenv

Set up a default Python version using `pyenv`, and optionally `pyenv-virtualenv` for virtual environments. You can use:

- **[Interactive script] Python Version & pyenv-virtualenv Setup Helper:**  
  [`https://github.com/GitauHarrison/install_new_python_version_in_your_osr`](https://github.com/GitauHarrison/install_new_python_version_in_your_os)
- **[Do it yourself] Guide: Install A Different Version Of Python From The Default in macOS And Work With Virtual Environments:**  
  [`https://github.com/GitauHarrison/notes_on_general_topics/blob/main/01_new_python_version_macOS_virtualenv.md`](https://github.com/GitauHarrison/notes_on_general_topics/blob/main/01_new_python_version_macOS_virtualenv.md)

### 3. Poetry (if you choose the Poetry workflow)

If you want to use **pyenv + Poetry**, install Poetry first and ensure the `poetry` command is on your `PATH`. Learn how to work with `poetry` [here](https://github.com/GitauHarrison/notes_on_general_topics/blob/main/03_working_with_virtual_envs_in_flask.md).

The script checks for `poetry` before proceeding with the Poetry option.

## Supported workflows

### Workflow A: pyenv + Poetry

- Python version management via `pyenv`.
- Dependency and virtualenv management via `Poetry`.
- The helper generates:
  - `pyproject.toml` with initial project metadata.
- It does **not** create a `poetry.lock` file; that file will be created by
  Poetry itself the first time you run `poetry add ...` or `poetry lock`. This
  avoids the "lock file does not have a metadata entry" error that happens
  when using a hand-written placeholder.
- It also appends this alias to your shell rc (`~/.zshrc` or `~/.bashrc`):

  ```bash
  alias pf='poetry run flask'
  ```

  This lets you run Flask commands as:

  - `pf run` → `poetry run flask run`
  - `pf db init` → `poetry run flask db init`

### Workflow B: pyenv + pyenv-virtualenv + `requirements.txt`

- Python and virtualenv management via `pyenv` + `pyenv-virtualenv`.
- Dependencies tracked in a traditional `requirements.txt`.
- You create/activate the virtual environment with pyenv (or pyenv-virtualenv), then install dependencies with `pip`.

## How to use this helper

### 1. Clone this repository

From wherever you keep your personal projects (for example `~/software_development/personal`):

```bash
cd ~/software_development/personal
# clone the repo that contains this folder, then:
cd 03_automate_creating_flask_project_structure
```

### 2. Run the script

You can either run it with Python:

```bash
python create_flask_project.py
```

Or, if it is marked executable:

```bash
./create_flask_project.py
```

### 3. Choose your workflow

The script will ask:

- `1) pyenv + Poetry (pyproject.toml)`
- `2) pyenv + pyenv-virtualenv + requirements.txt`
- `q) Quit`

Pick the option that matches how you already manage virtual environments and dependencies. The script then performs automatic checks:

- `pyenv` must be available.
- For **Option 1 (Poetry)**: `poetry` must be available.
- For **Option 2 (pyenv-virtualenv)**: `pyenv-virtualenv` must be installed
  (detected via `pyenv virtualenvs`).

If something is missing, the script stops and prints links to the guides and helper repositories listed above. It does **not** try to fix your environment for you.

### 4. Answer the prompts

You will be asked for:

1. **Project folder name** (default: `flask_project`)  
   The project will be created in your **home directory**, e.g.
   `~/flask_project`.
2. **Short project description**  
   Used to fill the generated `README.md`.
3. **Author / owner name**  
   Used in the generated `LICENSE` and docs.

The script then generates the project.

## Project structure generated

### Top-level layout

The resulting project (assuming `flask_project`) looks like this:

```text
flask_project/
  main.py
  config.py
  .flaskenv
  .env
  .gitignore
  .gitattributes
  README.md
  CONTRIBUTING.md
  CODE_OF_CONDUCT.md
  LICENSE
  requirements.txt            # if you chose pyenv + pyenv-virtualenv
  pyproject.toml              # if you chose pyenv + Poetry
  app/
    __init__.py
    routes.py
    models.py
    email.py
    forms.py
    errors.py
    utils/
      __init__.py
      decorators.py
    templates/
      base.html
      partials/
        _footer.html
        _flash_messages.html
        _public_navbar.html
        _dashboard_navbar.html
      auth/
        login.html
        register.html
        request_password_reset.html
        reset_password.html
      errors/
        404.html
        500.html
      emails/
        reset_password.html
        reset_password.txt
      main/
        index.html
        contact.html
      dashboard/
        dashboard.html
    static/
      css/
        main.css
        dashboard.css
      js/
        main.js
        dashboard.js
      img/
        .gitkeep
```

### The `app/` package

- `app/__init__.py`  
  Creates the Flask application instance (application factory), configures extensions such as SQLAlchemy, Flask-Login, Flask-Migrate, Flask-Mail, Flask-Moment, and CSRF protection.

- `app/models.py`  
  Contains a **`User`** model:
  - `username`, `email`, `password_hash`, `created_at`.
  - Uses `email` to generate a Gravatar avatar URL.
  - Integrated with `Flask-Login` via `UserMixin` and a `user_loader`.

- `app/routes.py`  
  Defines core routes:
  - `/` and `/contact` for anonymous public pages.
  - `/login`, `/register`, `/logout`.
  - `/dashboard` as an authenticated-only page.
  - Uses a dummy user (`username: test`, `email: test@email.com`, `password: test12345`) to demonstrate login flow without wiring a real database yet.

- `app/forms.py`  
  Prepopulated WTForms-based classes:
  - `LoginForm`
  - `RegistrationForm`
  - `RequestResetPasswordForm`
  - `ResetPasswordForm`
  - `ContactForm`

- `app/email.py`  
  Helper functions to send emails (e.g. password reset email) using `Flask-Mail`, with HTML and text versions of templates.

- `app/errors.py`  
  Functions to register handlers for `404` and `500` errors.

- `app/utils/decorators.py`  
  Reusable decorators such as:
  - `redirect_if_authenticated` – redirects authenticated users away from pages like login/register to the dashboard.
  - `login_required_with_message` – simple example that wraps access control with a helpful flash message.

You can extend `app/utils/` with more helpers, for example:

- Decorators for role-based access control.
- Decorators to enforce email verification.
- Helper functions for pagination or API responses.

### Templates

- `base.html`  
  Uses the latest Bootstrap via CDN. Defines a clean layout with blocks for title, navbar, content, and extra CSS/JS.

- `partials/_public_navbar.html`  
  Navbar for anonymous areas (home, contact, login, register).

- `partials/_dashboard_navbar.html`  
  Dark-themed navbar for authenticated dashboard sections.

- `partials/_footer.html` and `partials/_flash_messages.html`  
  Reusable footer and flash-message block.

- `auth/` templates (`login.html`, `register.html`, etc.)  
  Minimal but styled forms using Bootstrap.

- `main/index.html`  
  Anonymous landing page plus a sample contact form section.

- `main/contact.html`  
  Placeholder contact page.

- `dashboard/dashboard.html`  
  Authenticated-only page with a layout that visibly differs from `index.html` to emphasize the separation between public and private areas.

- `errors/404.html`, `errors/500.html`  
  Simple, user-friendly error pages.

- `emails/reset_password.html`, `emails/reset_password.txt`  
  Templates used by `app/email.py` for password reset emails.

### Static files

- `static/css/main.css`  
  Basic layout tweaks and overrides.

- `static/css/dashboard.css`  
  Dashboard-specific styling.

- `static/js/main.js` / `static/js/dashboard.js`  
  Placeholders for your global and dashboard-specific JavaScript.

- `static/img/.gitkeep`  
  Keeps the `img/` directory in version control, ready for you to add assets.

## Installing dependencies

### Common dependency list

Regardless of workflow, you should install at least:

- `flask`
- `python-dotenv`
- `email-validator`
- `flask-login`
- `flask-migrate`
- `flask-sqlalchemy`
- `flask-moment`
- `flask-mail`
- `flask-wtf`
- `pyjwt`

The scaffold either writes them to `requirements.txt` or `pyproject.toml` so that you can install them with your chosen tool.

### If you chose pyenv + pyenv-virtualenv

1. **Create and activate a virtual environment** (example):

   ```bash
   # Choose a Python version that pyenv manages
   pyenv virtualenv 3.12.0 flask-starter-env

   cd ~/flask_project           # or your chosen project name
   pyenv local flask-starter-env
   # Now, whenever you `cd` into this folder, the env is active.
   ```

2. **Install dependencies** inside the active virtualenv:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run Flask commands** (ensure `.flaskenv` is present so FLASK_APP is set):

   ```bash
   flask run
   # or
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

### If you chose pyenv + Poetry

1. **Ensure pyenv has set your global / local Python version** as desired.

2. **From your project directory** (e.g. `~/flask_project`):

   ```bash
   poetry install
   ```

   This reads `pyproject.toml` and installs dependencies into Poetry's managed
   virtual environment.

3. **Reload your shell** (or source your rc file) so the alias is available:

   ```bash
   source ~/.zshrc    # or ~/.bashrc, depending on your shell
   ```

4. Install your dependancies:

    ```python
    poetry add flask flask-mail # etc
    ```

5. **Use the `pf` alias** for Flask commands:

   ```bash
   pf run                     # poetry run flask run
   pf db init                 # poetry run flask db init
   pf db migrate -m "Init"    # poetry run flask db migrate -m "Init"
   pf db upgrade              # poetry run flask db upgrade
   ```

6. Should you make any manual changes to your `pyproject.toml` file, remember to update the `poetry.lock` file by running:

    ```python
    poetry lock
    ```

If you prefer to skip the alias, you can always run:

```bash
poetry run flask run
```

## Using the app

### Running the development server

After installing dependencies and configuring your virtual environment:

- **Workflow B (pyenv + pyenv-virtualenv):**

  ```bash
  cd ~/flask_project
  # ensure your pyenv/virtualenv is active here
  flask run
  ```

- **Workflow A (pyenv + Poetry):**

  ```bash
  cd ~/flask_project
  poetry install      # if you haven't already
  pf run              # or: poetry run flask run
  ```

The app will use `FLASK_APP=main.py` and `FLASK_ENV=development` from `.flaskenv`.

### Database and migrations

The scaffold wires in `Flask-Migrate` and `SQLAlchemy` so you can quickly add a
real database.

Typical steps (once dependencies and configuration are in place):

```bash
# Inside an active virtualenv for this project
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

or, with Poetry:

```bash
pf db init
pf db migrate -m "Initial migration"
pf db upgrade
```

## After the scaffold

Once the script has created the project for you, typical next steps are:

1. **Activate your virtualenv** (pyenv-virtualenv or Poetry-managed).
2. **Install the dependencies** (`pip install -r requirements.txt` or
   `poetry install`).
3. **Configure environment variables** in `.env`:
   - `SECRET_KEY`
   - `DATABASE_URL` (for a real database)
   - Mail server settings for password reset emails.
4. **Customize the `User` model** for your needs (profile fields, roles, etc.).
5. **Wire up real authentication logic** (hashing passwords, registration,
   password reset, email verification).
6. **Extend templates, static assets, and utilities** to match your product.

This helper gets you to a consistent, opinionated starting point quickly, so you can focus on building features instead of assembling boilerplate each time you start a new Flask project.
