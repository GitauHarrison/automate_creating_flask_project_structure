#!/usr/bin/env python3
"""Interactive helper to scaffold a starter Flask project.

This script assumes you already:
- Use pyenv to manage your default Python version.
- Optionally use pyenv-virtualenv for virtual environments.
- Optionally use Poetry for dependency management.

It does NOT install pyenv, pyenv-virtualenv or Poetry for you.
Instead, it checks for them and, if missing, points you to the
appropriate guides and helper repositories.
"""

import os
import sys
import textwrap
import platform
import shutil
from pathlib import Path
import subprocess

HOME = Path.home()


def print_header() -> None:
    print("=" * 72)
    print("Automated Flask Project Scaffold")
    print("=" * 72)
    print(
        textwrap.dedent(
            """
            This helper will create a new Flask project in your home directory,
            with a clean, opinionated structure and starter code.

            It supports two workflows:
              1) pyenv + Poetry
              2) pyenv + pyenv-virtualenv + requirements.txt

            IMPORTANT:
            - This script assumes you already configured Git & GitHub,
              installed pyenv, and selected a default Python version.
            - It will NOT install or configure those tools for you.
            - Dependency installation (Flask, Flask-Login, etc.) must be
              done manually in your active virtual environment after the
              scaffold is created.
            """
        ).strip()
    )
    print("\n")


def detect_platform() -> str:
    """Return one of: macos, ubuntu, windows, wsl, other."""
    system = platform.system().lower()
    # Detect WSL explicitly
    if "microsoft" in platform.release().lower() or os.environ.get("WSL_DISTRO_NAME"):
        return "wsl"
    if system == "darwin":
        return "macos"
    if system == "linux":
        # Best-effort detection of Ubuntu
        try:
            with open("/etc/os-release", "r", encoding="utf-8") as f:
                data = f.read().lower()
            if "ubuntu" in data:
                return "ubuntu"
        except OSError:
            pass
        return "linux"
    if system == "windows":
        return "windows"
    return "other"


def have_command(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def check_pyenv() -> bool:
    return have_command("pyenv")


def check_pyenv_virtualenv() -> bool:
    if not check_pyenv():
        return False
    # Best-effort: pyenv virtualenvs should succeed when plugin is installed
    try:
        proc = subprocess.run(
            ["pyenv", "virtualenvs"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return proc.returncode == 0
    except OSError:
        return False


def check_poetry() -> bool:
    return have_command("poetry")


def show_prereq_instructions(option: str) -> None:
    """Explain what is missing and where to go next."""
    print("\nPrerequisite check failed for option:", option)
    print("\nBefore using this scaffold, please ensure that you have:")
    print("  1. Git & GitHub configured (SSH keys, per-account gitconfig, etc.)")
    print("  2. A default Python version set via pyenv.")
    if option == "1":
        print("  3. Poetry installed and on your PATH.")
    elif option == "2":
        print("  3. pyenv-virtualenv installed and working.")

    print("\nYou can use these guides and helper repositories:")
    print("- Git & GitHub configuration (scripts + guide):")
    print("  https://github.com/GitauHarrison/git_github_configurations")
    print("  https://github.com/GitauHarrison/notes_on_general_topics/blob/main/02_automate_git_and_github_setup.md")
    print("- Python version & pyenv / pyenv-virtualenv setup helper:")
    print("  https://github.com/GitauHarrison/install_new_python_version_in_your_os?tab=readme-ov-file#python-version--pyenv-virtualenv-setup-helper")
    print("- Manual guide for newer Python + virtualenv on macOS:")
    print("  https://github.com/GitauHarrison/notes_on_general_topics/blob/main/01_new_python_version_macOS_virtualenv.md")
    print("- Working with virtual environments in Flask:")
    print("  https://github.com/GitauHarrison/notes_on_general_topics/blob/main/03_working_with_virtual_envs_in_flask.md")


def ensure_prereqs(option: str) -> bool:
    """Return True if environment is ready for the chosen option."""
    has_pyenv = check_pyenv()
    has_pyenv_venv = check_pyenv_virtualenv()
    has_poetry = check_poetry()

    ok = True
    if not has_pyenv:
        print("- pyenv not found on PATH.")
        ok = False

    if option == "1":  # pyenv + Poetry
        if not has_poetry:
            print("- Poetry not found on PATH.")
            ok = False
    elif option == "2":  # pyenv + pyenv-virtualenv
        if not has_pyenv_venv:
            print("- pyenv-virtualenv plugin does not appear to be installed.")
            ok = False

    if not ok:
        show_prereq_instructions(option)
    else:
        print("Environment checks passed.")
    return ok


def prompt_choice(prompt: str, choices: dict) -> str:
    """Prompt until the user selects one of the given keys."""
    while True:
        print(prompt)
        for key, label in choices.items():
            print(f"  {key}) {label}")
        value = input("Enter choice: ").strip()
        if value in choices:
            return value
        print("Invalid choice, please try again.\n")


def prompt_with_default(prompt: str, default: str) -> str:
    value = input(f"{prompt} [{default}]: ").strip()
    return value or default


def ensure_project_dir(project_name: str) -> Path:
    project_root = HOME / project_name
    if project_root.exists():
        if any(project_root.iterdir()):
            print(f"\nDirectory {project_root} already exists and is not empty.")
            answer = input("Do you want to abort and choose a different project name? [Y/n]: ").strip().lower()
            if answer in {"", "y", "yes"}:
                sys.exit(1)
        else:
            print(f"Using existing empty directory: {project_root}")
    else:
        project_root.mkdir(parents=True, exist_ok=True)
        print(f"Created project directory: {project_root}")
    return project_root


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip("\n") + "\n", encoding="utf-8")
    print(f"  - Created {path.relative_to(HOME)}")


def scaffold_top_level_files(project_root: Path, project_name: str, description: str, author: str, use_poetry: bool) -> None:
    # .flaskenv
    write_text(
        project_root / ".flaskenv",
        textwrap.dedent(
            f"""
            FLASK_APP=main.py
            FLASK_ENV=development
            FLASK_DEBUG=1
            """
        ),
    )

    # .env (placeholder for secrets)
    write_text(
        project_root / ".env",
        textwrap.dedent(
            """
            # Environment variables for your Flask app
            # Fill these in as needed. See comments in config.py for details.

            SECRET_KEY=
            DATABASE_URL=

            MAIL_SERVER=
            MAIL_PORT=
            MAIL_USE_TLS=
            MAIL_USERNAME=
            SENDGRID_API_KEY=
            MAIL_DEFAULT_SENDER=
            ADMINS=
            TECH_ADMIN=

            LOG_TO_STDOUT=
            UPLOAD_FOLDER=

            RECAPTCHA_PUBLIC_KEY=
            RECAPTCHA_PRIVATE_KEY=
            """
        ),
    )

    # .gitignore
    write_text(
        project_root / ".gitignore",
        textwrap.dedent(
            """
            __pycache__/
            *.py[cod]
            *.pyo
            *.pyd
            .Python
            env/
            venv/
            .venv/
            .mypy_cache/
            .pytest_cache/
            .DS_Store
            .env
            instance/
            *.sqlite3
            *.db
            .idea/
            .vscode/
            """
        ),
    )

    # .gitattributes
    write_text(
        project_root / ".gitattributes",
        textwrap.dedent(
            """
            * text=auto
            *.py diff=python
            """
        ),
    )

    # LICENSE (MIT by default)
    year = str(platform.python_version())  # not ideal for year, but avoids extra imports
    license_text = textwrap.dedent(
        f"""
        MIT License

        Copyright (c) {author}

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        SOFTWARE.
        """
    )
    write_text(project_root / "LICENSE", license_text)

    # README
    readme = textwrap.dedent(
        f"""
        # {project_name}

        {description}

        This repository contains a Flask web application with a blueprint-based
        structure (`main`, `auth`, `admin`, `errors`). It is intended as a
        practical starting point for real projects: you can run it immediately,
        then modify or replace any part of it to suit your needs.

        ## What you get

        Note: This starter uses Flask blueprints, which are a slightly more
        advanced concept in Flask. If you are new to blueprints, you may want
        to skim the official Flask documentation on them alongside this
        scaffold.

        - A Flask application structured with blueprints (`main`, `auth`, `admin`, and `errors`).
        - A `User` model and basic authentication-related forms and templates.
        - Anonymous pages (e.g. home page) and authenticated pages (e.g. dashboard) with
          different layouts using Bootstrap.
        - A ready-to-extend structure for templates, static assets, utilities, and email
          handling.

        ## Learning resources (strongly recommended)

        If you want a deeper understanding of the tools this scaffold assumes,
        walk through these guides first:

        - Git & GitHub configuration (scripts + guide):
          - https://github.com/GitauHarrison/git_github_configurations
          - https://github.com/GitauHarrison/notes_on_general_topics/blob/main/02_automate_git_and_github_setup.md
        - Python version & pyenv / pyenv-virtualenv setup helper:
          - https://github.com/GitauHarrison/install_new_python_version_in_your_os?tab=readme-ov-file#python-version--pyenv-virtualenv-setup-helper
        - Manual guide for newer Python + virtualenv on macOS:
          - https://github.com/GitauHarrison/notes_on_general_topics/blob/main/01_new_python_version_macOS_virtualenv.md
        - Working with virtual environments in Flask:
          - https://github.com/GitauHarrison/notes_on_general_topics/blob/main/03_working_with_virtual_envs_in_flask.md

        After you are comfortable with these topics, this scaffold should feel
        much more intuitive.

        ## Blueprint structure overview

        This starter organizes your application into several blueprints:

        - `main`: public-facing pages (home, contact) and the authenticated
          dashboard.
        - `auth`: authentication-related routes (login, register, logout) and
          forms.
        - `admin`: a placeholder for admin-only routes and views.
        - `errors`: central error handlers that render different templates for
          anonymous vs authenticated users.

        Understanding how blueprints work will make it easier to extend this
        structure as your application grows.

        ## How to work with this repo

        ### What the script did

        When you ran `create_flask_project.py`, it:

        - Created this project folder in your home directory.
        - Generated the Flask application package (`app/`), configuration,
          templates, static assets, and supporting files (README, LICENSE,
          CONTRIBUTING, CODE_OF_CONDUCT, etc.).
        - Optionally created a `pyproject.toml` (if you chose Poetry) or a
          `requirements.txt` (if you chose the pyenv-virtualenv workflow).
        - If you selected Poetry, it may have added a convenience alias
          `pf='poetry run flask'` to your shell startup file (`~/.zshrc` or
          `~/.bashrc`). You are free to remove or change this alias.

        The script does *not* modify any other global configuration. All other
        files it creates live inside this project directory.

        ### Day-to-day usage

        1. Create or activate a virtual environment using your preferred workflow
           (pyenv + pyenv-virtualenv or pyenv + Poetry).
        2. If you chose **Poetry**, from the project root, add the core dependencies
           in one go:

           `poetry add flask flask-sqlalchemy flask-migrate flask-login flask-wtf flask-mail flask-moment python-dotenv email-validator pyjwt`

           This will update `pyproject.toml` and let Poetry generate a valid
           `poetry.lock` the first time you run `poetry add` or `poetry lock`.
           The scaffold intentionally does not create a placeholder lock file to
           avoid the "lock file does not have a metadata entry" error that
           occurs if `poetry.lock` is not generated by Poetry itself.

           If you manually edit `pyproject.toml` later, run `poetry lock` to
           regenerate `poetry.lock` so it stays in sync.

        3. If you chose **requirements.txt**, create a virtualenv and run:

           `pip install -r requirements.txt`

           Whenever you install or upgrade packages in that virtualenv, update
           `requirements.txt` with `pip3 freeze > requirements.txt`.

        4. Set your environment variables in `.env` and `.flaskenv` as needed.
        5. Run the app in development mode and start building features.

        ### After the first run: what to do next

        - Review the generated files and delete or rename anything you do not
          need. This scaffold is a starting point, not a constraint.
        - Customize blueprints, templates, and configuration to match your
          real application.
        - Keep your dependency declarations (`pyproject.toml` or
          `requirements.txt`) in sync with your virtual environment as you add
          or remove packages.

        ## Next steps (high level)

        1. Create or activate a virtual environment using your preferred workflow
           (pyenv + pyenv-virtualenv or pyenv + Poetry).
        2. If you chose **Poetry**, from the project root, add the core dependencies
           in one go:

           `poetry add flask flask-sqlalchemy flask-migrate flask-login flask-wtf flask-mail flask-moment python-dotenv email-validator pyjwt`

           This will update `pyproject.toml` and let Poetry generate a valid
           `poetry.lock` the first time you run `poetry add` or `poetry lock`.
           The scaffold intentionally does not create a placeholder lock file to
           avoid the "lock file does not have a metadata entry" error that
           occurs if `poetry.lock` is not generated by Poetry itself.

           If you manually edit `pyproject.toml` later, run `poetry lock` to
           regenerate `poetry.lock` so it stays in sync.

        3. If you chose **requirements.txt**, create a virtualenv and run:

           `pip install -r requirements.txt`

           Whenever you install or upgrade packages in that virtualenv, update
           `requirements.txt` with `pip3 freeze > requirements.txt`.

        4. Set your environment variables in `.env` and `.flaskenv` as needed.
        5. Run the app in development mode and start building features.
        """
    )
    write_text(project_root / "README.md", readme)

    # CONTRIBUTING
    contributing = textwrap.dedent(
        """
        # Contributing

        Thank you for your interest in contributing!

        This project aims to provide a clear, opinionated starting point for
        Flask applications. Contributions that improve clarity, robustness,
        documentation, or developer experience are welcome.

        ## Ways to contribute

        - Report bugs or confusing behavior by opening an issue.
        - Improve documentation, comments, and inline explanations.
        - Add small, focused features that align with the goal of being a
          teaching-friendly starter project.
        - Refine structure or configuration to follow best practices.

        ## Contribution guidelines

        1. **Discuss large changes first**
           - For significant features or refactors, open an issue to describe
             what you would like to change and why.

        2. **Keep changes focused**
           - Prefer small, self-contained pull requests that are easy to review.
           - Avoid mixing unrelated changes (e.g. style fixes and new features)
             in the same PR.

        3. **Code style and structure**
           - Follow the existing structure (blueprints, separation of concerns).
           - Use clear naming and add docstrings or comments where behavior
             might not be obvious to someone new to Flask.

        4. **Testing and manual verification**
           - Where possible, add or update tests when you change behavior.
           - At minimum, run the development server and manually exercise the
             changed flows (e.g. login, registration, error pages) before
             submitting a PR.

        5. **Commit messages and pull requests**
           - Use descriptive commit messages that explain *why* a change was
             made, not just *what* was changed.
           - In PR descriptions, include a short summary, any relevant issue
             links, and clear testing notes.

        By following these guidelines, you help keep this scaffold approachable
        for people who are learning Flask and modern Python workflows.
        """
    )
    write_text(project_root / "CONTRIBUTING.md", contributing)

    # CODE_OF_CONDUCT
    coc = textwrap.dedent(
        """
        # Code of Conduct

        This project is dedicated to providing a welcoming and harassment-free
        experience for everyone, regardless of background or experience level.

        We expect all contributors, maintainers, and users to:

        - Be respectful and considerate in all interactions.
        - Assume good faith and seek to understand before reacting.
        - Provide constructive feedback and avoid personal attacks.
        - Use inclusive language and be mindful of different backgrounds and
          experience levels.

        ## Unacceptable behavior

        Examples of behavior that will not be tolerated include, but are not
        limited to:

        - Harassment, discrimination, or derogatory comments.
        - Threats of violence or encouraging self-harm.
        - Public or private harassment, including repeated unwanted contact.
        - Publishing others' private information (doxxing) without consent.
        - Any conduct that would be reasonably considered inappropriate in a
          professional setting.

        ## Reporting concerns

        If you experience or witness behavior that violates this Code of
        Conduct:

        - Consider politely pointing out the issue, if you feel safe doing so.
        - Otherwise, or if the behavior continues, please contact the project
          maintainer privately using the contact information in the README or
          project metadata.

        All reports will be reviewed in good faith. The maintainers will take
        appropriate action, which may include warnings, temporary restrictions,
        or removal from participation in the project.

        By participating in this project, you agree to abide by this Code of
        Conduct and help foster a positive, supportive environment for
        everyone.
        """
    )
    write_text(project_root / "CODE_OF_CONDUCT.md", coc)


def scaffold_config_and_main(project_root: Path) -> None:
    # config.py
    config_py = textwrap.dedent(
        """
        import os

        basedir = os.path.abspath(os.path.dirname(__file__))


        class Config(object):
            '''All application configurations.

            Configure your environment variables in the .env file at the project root.
            If a value is missing there, sensible defaults are used for local
            development (for example, SQLite instead of Postgres).
            '''

            # Web form security
            SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-cannot-guess'

            # Database configurations
            # Prefer DATABASE_URL from the environment; fall back to a local SQLite file.
            SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                'sqlite:///' + os.path.join(basedir, 'app.db')
            SQLALCHEMY_TRACK_MODIFICATIONS = False

            # Email
            MAIL_SERVER = os.environ.get('MAIL_SERVER')
            MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
            MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
            MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
            MAIL_PASSWORD = os.environ.get('SENDGRID_API_KEY')
            MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
            ADMINS = os.environ.get('ADMINS', '').split(',') if os.environ.get('ADMINS') else []
            TECH_ADMIN = os.environ.get('TECH_ADMIN')

            # Deployment / logging
            LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
            UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')

            # reCAPTCHA configuration
            RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
            RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
        """
    )
    write_text(project_root / "config.py", config_py)

    # app/__init__.py
    app_init = textwrap.dedent(
        """
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        from flask_login import LoginManager
        from flask_migrate import Migrate
        from flask_mail import Mail
        from flask_moment import Moment
        from flask_wtf import CSRFProtect
        from config import Config
        import logging
        from logging.handlers import SMTPHandler, RotatingFileHandler
        import os
        from sqlalchemy import MetaData


        convention = {
            "ix": 'ix_%(column_0_label)s',
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }

        metadata = MetaData(naming_convention=convention)

        db = SQLAlchemy(metadata=metadata)
        migrate = Migrate()
        login_manager = LoginManager()
        moment = Moment()
        mail = Mail()
        csrf = CSRFProtect()


        def create_app(config_class: type[Config] = Config) -> Flask:
            '''Application factory.

            This factory wires extensions, logging and routes together.
            The application is structured using blueprints (main, auth, admin,
            errors) to keep concerns separated.
            '''
            app = Flask(__name__)
            app.config.from_object(config_class)

            db.init_app(app)
            migrate.init_app(app, db, render_as_batch=True)
            login_manager.init_app(app)
            login_manager.login_view = 'auth.login'
            login_manager.login_message = app.config.get('LOGIN_MESSAGE', 'Please sign in to access this page.')
            login_manager.login_message_category = app.config.get('LOGIN_MESSAGE_CATEGORY', 'info')
            mail.init_app(app)
            moment.init_app(app)
            csrf.init_app(app)

            # Register blueprints
            from app.errors import bp as errors_bp
            app.register_blueprint(errors_bp)

            from app.auth import bp as auth_bp
            app.register_blueprint(auth_bp, url_prefix='/auth')

            from app.admin import bp as admin_bp
            app.register_blueprint(admin_bp, url_prefix='/admin')

            from app.main import bp as main_bp
            app.register_blueprint(main_bp)

            # Import models so that tools like Flask-Migrate can discover them.
            from app import models  # noqa: F401

            if not app.debug and not app.testing:
                if app.config['MAIL_SERVER']:
                    auth = None
                    if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                        auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
                    secure = None
                    if app.config['MAIL_USE_TLS']:
                        secure = ()
                    mail_handler = SMTPHandler(
                        mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                        fromaddr=app.config['MAIL_DEFAULT_SENDER'],
                        toaddrs=[app.config.get('TECH_ADMIN')] if app.config.get('TECH_ADMIN') else [],
                        subject=f"{app.name} failure",
                        credentials=auth,
                        secure=secure,
                    )
                    mail_handler.setLevel(logging.ERROR)
                    app.logger.addHandler(mail_handler)

                if app.config.get('LOG_TO_STDOUT'):
                    stream_handler = logging.StreamHandler()
                    stream_handler.setLevel(logging.INFO)
                    app.logger.addHandler(stream_handler)
                else:
                    if not os.path.exists('logs'):
                        os.mkdir('logs')
                    file_handler = RotatingFileHandler(
                        'logs/app.log', maxBytes=10240, backupCount=10,
                    )
                    file_handler.setFormatter(
                        logging.Formatter(
                            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
                        )
                    )
                    file_handler.setLevel(logging.INFO)
                    app.logger.addHandler(file_handler)

                app.logger.setLevel(logging.INFO)
                app.logger.info('%s startup', app.name)

            return app
        """
    )
    write_text(project_root / "app" / "__init__.py", app_init)

    # main.py
    main_py = textwrap.dedent(
        """
        '''Entry point for running the Flask development server.'''

        from app import create_app, db
        from app.models import User

        app = create_app()


        @app.shell_context_processor
        def make_shell_context() -> dict:
            return {"db": db, "User": User}


        if __name__ == "__main__":
            app.run()
        """
    )
    write_text(project_root / "main.py", main_py)


def scaffold_models_forms_email_errors(project_root: Path) -> None:
    # models.py
    models_py = textwrap.dedent(
        """
        from datetime import datetime
        from hashlib import md5

        from flask_login import UserMixin
        from werkzeug.security import generate_password_hash, check_password_hash

        from app import db, login_manager


        class User(UserMixin, db.Model):
            '''User account model.

            This example keeps the fields intentionally small, but includes helpers
            for password hashing and avatar URLs.
            '''

            id = db.Column(db.Integer, primary_key=True)
            username = db.Column(db.String(64), unique=True, index=True, nullable=False)
            email = db.Column(db.String(120), unique=True, index=True, nullable=False)
            password_hash = db.Column(db.String(256), nullable=False)
            created_at = db.Column(db.DateTime, default=datetime.utcnow)

            def __repr__(self) -> str:  # pragma: no cover - debug helper
                return f"<User {self.username!r}>"

            def set_password(self, password: str) -> None:
                '''Hash and store the given plaintext password.'''
                self.password_hash = generate_password_hash(password)

            def check_password(self, password: str) -> bool:
                '''Return True if the given password matches the stored hash.'''
                return check_password_hash(self.password_hash, password)

            def avatar(self, size: int = 128) -> str:
                # Return a gravatar URL based on the user's email address.
                digest = md5(self.email.lower().encode("utf-8")).hexdigest()
                return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"


        @login_manager.user_loader
        def load_user(user_id: str) -> "User | None":  # pragma: no cover - thin wrapper
            return User.query.get(int(user_id))
        """
    )
    write_text(project_root / "app" / "models.py", models_py)

    # auth/forms.py
    auth_forms_py = textwrap.dedent(
        """
        from flask_wtf import FlaskForm
        from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
        from wtforms.validators import DataRequired, Email, EqualTo, Length


        class LoginForm(FlaskForm):
            email = StringField("Email", validators=[DataRequired(), Email()])
            password = PasswordField("Password", validators=[DataRequired()])
            remember_me = BooleanField("Remember me")
            submit = SubmitField("Sign in")


        class RegistrationForm(FlaskForm):
            username = StringField("Username", validators=[DataRequired(), Length(min=3, max=64)])
            email = StringField("Email", validators=[DataRequired(), Email()])
            password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
            password2 = PasswordField(
                "Repeat Password",
                validators=[DataRequired(), EqualTo("password", message="Passwords must match.")],
            )
            submit = SubmitField("Create account")


        class RequestResetPasswordForm(FlaskForm):
            email = StringField("Email", validators=[DataRequired(), Email()])
            submit = SubmitField("Send password reset link")


        class ResetPasswordForm(FlaskForm):
            password = PasswordField("New password", validators=[DataRequired(), Length(min=8)])
            password2 = PasswordField(
                "Repeat Password",
                validators=[DataRequired(), EqualTo("password", message="Passwords must match.")],
            )
            submit = SubmitField("Reset password")


        class ContactForm(FlaskForm):
            name = StringField("Name", validators=[DataRequired(), Length(min=2, max=64)])
            email = StringField("Email", validators=[DataRequired(), Email()])
            message = TextAreaField("Message", validators=[DataRequired(), Length(min=10, max=1000)])
            submit = SubmitField("Send message")
        """
    )
    write_text(project_root / "app" / "auth" / "forms.py", auth_forms_py)

    # main/forms.py (for public-facing contact form)
    main_forms_py = textwrap.dedent(
        """
        from flask_wtf import FlaskForm
        from wtforms import StringField, TextAreaField, SubmitField
        from wtforms.validators import DataRequired, Email, Length


        class ContactForm(FlaskForm):
            name = StringField("Name", validators=[DataRequired(), Length(min=2, max=64)])
            email = StringField("Email", validators=[DataRequired(), Email()])
            message = TextAreaField("Message", validators=[DataRequired(), Length(min=10, max=1000)])
            submit = SubmitField("Send message")
        """
    )
    write_text(project_root / "app" / "main" / "forms.py", main_forms_py)

    # email.py
    email_py = textwrap.dedent(
        """
        from threading import Thread

        from flask import current_app
        from flask_mail import Message

        from app import mail


        def send_async_email(app, msg):
            '''Send email in a background thread.'''
            with app.app_context():
                mail.send(msg)


        def send_email(subject, sender, recipients, text_body, html_body):
            '''Send an email asynchronously using Flask-Mail and threading.'''
            msg = Message(subject, sender=sender, recipients=recipients)
            msg.body = text_body
            msg.html = html_body
            Thread(
                target=send_async_email,
                args=(current_app._get_current_object(), msg),
            ).start()
        """
    )
    write_text(project_root / "app" / "email.py", email_py)

    # errors blueprint package
    errors_init = textwrap.dedent(
        """
        from flask import Blueprint

        bp = Blueprint('errors', __name__)

        from app.errors import handlers  # noqa: E402,F401
        """
    )
    write_text(project_root / "app" / "errors" / "__init__.py", errors_init)

    errors_handlers = textwrap.dedent(
        """
        from flask import render_template
        from flask_login import current_user

        from app import db
        from app.errors import bp


        @bp.app_errorhandler(404)
        def page_not_found(error):
            '''Render different 404 pages depending on authentication status.'''
            if current_user.is_authenticated:
                return (
                    render_template('errors/404_dashboard.html', title='Page Not Found Error'),
                    404,
                )
            return (
                render_template('errors/404_public.html', title='Page Not Found Error'),
                404,
            )


        @bp.app_errorhandler(500)
        def internal_server_error(error):
            '''Render different 500 pages and roll back the session if needed.'''
            db.session.rollback()
            if current_user.is_authenticated:
                return (
                    render_template('errors/500_dashboard.html', title='Internal Server Error'),
                    500,
                )
            return (
                render_template('errors/500_public.html', title='Internal Server Error'),
                500,
            )
        """
    )
    write_text(project_root / "app" / "errors" / "handlers.py", errors_handlers)


def scaffold_utils(project_root: Path) -> None:
    utils_init = """"""
    write_text(project_root / "app" / "utils" / "__init__.py", utils_init)

    decorators_py = textwrap.dedent(
        """
        from functools import wraps

        from flask import redirect, url_for, flash
        from flask_login import current_user


        def redirect_if_authenticated(view_func):
            '''Redirect authenticated users away from auth-only pages (e.g. login/register).'''

            @wraps(view_func)
            def wrapper(*args, **kwargs):
                if current_user.is_authenticated:
                    flash("You are already signed in.", "info")
                    return redirect(url_for("dashboard"))
                return view_func(*args, **kwargs)

            return wrapper


        def login_required_with_message(view_func):
            # Simple wrapper around Flask-Login's behavior to add a flash message.

            @wraps(view_func)
            def wrapper(*args, **kwargs):
                if not current_user.is_authenticated:
                    flash("Please sign in to access this page.", "warning")
                    return redirect(url_for("login"))
                return view_func(*args, **kwargs)

            return wrapper
        """
    )
    write_text(project_root / "app" / "utils" / "decorators.py", decorators_py)


def scaffold_routes(project_root: Path) -> None:
    # main blueprint
    main_init = textwrap.dedent(
        """
        from flask import Blueprint

        bp = Blueprint('main', __name__)

        from app.main import routes  # noqa: E402,F401
        """
    )
    write_text(project_root / "app" / "main" / "__init__.py", main_init)

    main_routes = textwrap.dedent(
        """
        from flask import render_template, redirect, url_for, flash
        from flask_login import login_required

        from app.main import bp
        from app.main.forms import ContactForm
        from app.utils.decorators import redirect_if_authenticated, login_required_with_message


        @bp.route("/", methods=["GET", "POST"])
        @redirect_if_authenticated
        def index():
            form = ContactForm()
            if form.validate_on_submit():
                flash("Thank you for your message!", "success")
                return redirect(url_for("main.index"))
            return render_template("main/index.html", form=form)


        @bp.route("/contact", methods=["GET", "POST"])
        @redirect_if_authenticated
        def contact():
            form = ContactForm()
            if form.validate_on_submit():
                flash("Thank you for reaching out!", "success")
                return redirect(url_for("main.contact"))
            return render_template("main/contact.html", form=form)


        @bp.route("/dashboard")
        @login_required_with_message
        def dashboard():
            return render_template("dashboard/dashboard.html")
        """
    )
    write_text(project_root / "app" / "main" / "routes.py", main_routes)

    # auth blueprint
    auth_init = textwrap.dedent(
        """
        from flask import Blueprint

        bp = Blueprint('auth', __name__)

        from app.auth import routes  # noqa: E402,F401
        """
    )
    write_text(project_root / "app" / "auth" / "__init__.py", auth_init)

    auth_email_py = textwrap.dedent(
        """
        from flask import render_template, current_app

        from app.auth import bp
        from app.email import send_email


        def send_password_reset_email(user):
            '''Send a password reset email using the shared send_email helper.'''
            token = user.get_reset_password_token()
            send_email(
                '[Your Project] Reset Your Password',
                sender=current_app.config['ADMINS'][0] if current_app.config.get('ADMINS') else None,
                recipients=[user.email],
                text_body=render_template('emails/reset_password.txt', user=user, token=token),
                html_body=render_template('emails/reset_password.html', user=user, token=token),
            )
        """
    )
    write_text(project_root / "app" / "auth" / "email.py", auth_email_py)

    auth_routes = textwrap.dedent(
        """
        from flask import render_template, redirect, url_for, flash
        from flask_login import login_user, logout_user, login_required

        from app import db
        from app.auth import bp
        from app.auth.forms import LoginForm, RegistrationForm
        from app.models import User
        from app.utils.decorators import redirect_if_authenticated, login_required_with_message


        @bp.route("/login", methods=["GET", "POST"])
        @redirect_if_authenticated
        def login():
            form = LoginForm()

            # Dummy user for demonstration purposes. In a real app, you would
            # look this information up from the database and verify the stored
            # password hash.
            dummy = User(
                username="test",
                email="test@email.com",
                password_hash="test12345",
            )

            if form.validate_on_submit():
                if form.email.data == dummy.email and form.password.data == "test12345":
                    login_user(dummy, remember=form.remember_me.data)
                    flash("You are now logged in.", "success")
                    return redirect(url_for("main.dashboard"))
                flash("Invalid email or password.", "danger")
            return render_template("auth/login.html", form=form)


        @bp.route("/register", methods=["GET", "POST"])
        @redirect_if_authenticated
        def register():
            form = RegistrationForm()
            if form.validate_on_submit():
                flash("Registration is disabled in this starter project.", "info")
            return render_template("auth/register.html", form=form)


        @bp.route("/logout")
        @login_required_with_message
        def logout():
            logout_user()
            flash("You have been logged out.", "info")
            return redirect(url_for("main.index"))
        """
    )
    write_text(project_root / "app" / "auth" / "routes.py", auth_routes)

    # admin blueprint (placeholder)
    admin_init = textwrap.dedent(
        """
        from flask import Blueprint

        bp = Blueprint('admin', __name__)

        from app.admin import routes  # noqa: E402,F401
        """
    )
    write_text(project_root / "app" / "admin" / "__init__.py", admin_init)

    admin_routes = textwrap.dedent(
        """
        from flask import render_template
        from flask_login import login_required

        from app.admin import bp
        from app.utils.decorators import login_required_with_message


        @bp.route("/")
        @login_required_with_message
        def index():
            '''Simple admin landing page placeholder.'''
            return render_template("admin/index.html")
        """
    )
    write_text(project_root / "app" / "admin" / "routes.py", admin_routes)


def scaffold_templates(project_root: Path) -> None:
    templates_root = project_root / "app" / "templates"

    base_html = textwrap.dedent(
        """<!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>{% block title %}Flask Starter{% endblock %}</title>
            <link
              href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
              rel="stylesheet"
              integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"
              crossorigin="anonymous"
            >
            <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
            {% block extra_css %}{% endblock %}
          </head>
          <body>
            {% include 'partials/_flash_messages.html' %}
            {% block navbar %}{% endblock %}

            <main class="container py-4">
              {% block content %}{% endblock %}
            </main>

            {% include 'partials/_footer.html' %}

            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
                    integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"
                    crossorigin="anonymous"></script>
            <script src="{{ url_for('static', filename='js/main.js') }}"></script>
            {% block extra_js %}{% endblock %}
          </body>
        </html>
        """
    )
    write_text(templates_root / "base.html", base_html)

    # Partials
    flash_messages = textwrap.dedent(
        """{% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
          <div class="container mt-3">
            {% for category, message in messages %}
              <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
              </div>
            {% endfor %}
          </div>
        {% endif %}
        {% endwith %}
        """
    )
    write_text(templates_root / "partials" / "_flash_messages.html", flash_messages)

    footer = textwrap.dedent(
        """<footer class="border-top py-3 mt-5 text-center text-muted">
          <small>&copy; {{ config.SITE_NAME if config and config.SITE_NAME else 'Flask Starter' }}</small>
        </footer>
        """
    )
    write_text(templates_root / "partials" / "_footer.html", footer)

    public_navbar = textwrap.dedent(
        """<nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom mb-4">
          <div class="container-fluid">
            <a class="navbar-brand" href="{{ url_for('main.index') }}">Flask Starter</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarPublic"
                    aria-controls="navbarPublic" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarPublic">
              <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                <li class="nav-item">
                  <a class="nav-link" href="{{ url_for('main.index') }}">Home</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="{{ url_for('main.contact') }}">Contact</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="{{ url_for('auth.login') }}">Sign in</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="{{ url_for('auth.register') }}">Register</a>
                </li>
              </ul>
            </div>
          </div>
        </nav>
        """
    )
    write_text(templates_root / "partials" / "_public_navbar.html", public_navbar)

    dashboard_navbar = textwrap.dedent(
        """<nav class="navbar navbar-expand-lg navbar-dark bg-dark border-bottom mb-4">
          <div class="container-fluid">
            <a class="navbar-brand" href="{{ url_for('main.dashboard') }}">Dashboard</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarDashboard"
                    aria-controls="navbarDashboard" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarDashboard">
              <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                <li class="nav-item">
                  <a class="nav-link" href="{{ url_for('main.index') }}">Public site</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="{{ url_for('auth.logout') }}">Log out</a>
                </li>
              </ul>
            </div>
          </div>
        </nav>
        """
    )
    write_text(templates_root / "partials" / "_dashboard_navbar.html", dashboard_navbar)

    # Main pages
    index_html = textwrap.dedent(
        """{% extends 'base.html' %}
        {% block title %}Home - Flask Starter{% endblock %}
        {% block navbar %}{% include 'partials/_public_navbar.html' %}{% endblock %}
        {% block content %}
        <div class="row justify-content-center">
          <div class="col-md-8">
            <h1 class="mb-3">Welcome</h1>
            <p class="lead">This is your anonymous landing page.</p>
            <p class="mb-4">Use this page for marketing copy, feature highlights, or a public
              view of your product.</p>

            <hr>

            <h2>Contact us</h2>
            <form method="post" novalidate>
              {{ form.hidden_tag() }}
              <div class="mb-3">
                {{ form.name.label(class_='form-label') }}
                {{ form.name(class_='form-control') }}
                {% for error in form.name.errors %}
                  <div class="text-danger small">{{ error }}</div>
                {% endfor %}
              </div>
              <div class="mb-3">
                {{ form.email.label(class_='form-label') }}
                {{ form.email(class_='form-control') }}
                {% for error in form.email.errors %}
                  <div class="text-danger small">{{ error }}</div>
                {% endfor %}
              </div>
              <div class="mb-3">
                {{ form.message.label(class_='form-label') }}
                {{ form.message(class_='form-control', rows=4) }}
                {% for error in form.message.errors %}
                  <div class="text-danger small">{{ error }}</div>
                {% endfor %}
              </div>
              {{ form.submit(class_='btn btn-primary') }}
            </form>
          </div>
        </div>
        {% endblock %}
        """
    )
    write_text(templates_root / "main" / "index.html", index_html)

    contact_html = textwrap.dedent(
        """{% extends 'base.html' %}
        {% block title %}Contact - Flask Starter{% endblock %}
        {% block navbar %}{% include 'partials/_public_navbar.html' %}{% endblock %}
        {% block content %}
        <div class="row justify-content-center">
          <div class="col-md-8">
            <h1 class="mb-3">Contact</h1>
            <p>Use this page for a dedicated contact form or additional information.</p>
          </div>
        </div>
        {% endblock %}
        """
    )
    write_text(templates_root / "main" / "contact.html", contact_html)

        # Auth templates
    login_html = textwrap.dedent(
        """{% extends 'base.html' %}
        {% block title %}Sign in{% endblock %}
        {% block navbar %}{% include 'partials/_public_navbar.html' %}{% endblock %}
        {% block content %}
        <div class="row justify-content-center">
          <div class="col-md-6 col-lg-4">
            <h1 class="mb-3">Sign in</h1>
            <form method="post" novalidate>
              {{ form.hidden_tag() }}
              <div class="mb-3">
                {{ form.email.label(class_='form-label') }}
                {{ form.email(class_='form-control') }}
                {% for error in form.email.errors %}
                  <div class="text-danger small">{{ error }}</div>
                {% endfor %}
              </div>
              <div class="mb-3">
                {{ form.password.label(class_='form-label') }}
                {{ form.password(class_='form-control') }}
                {% for error in form.password.errors %}
                  <div class="text-danger small">{{ error }}</div>
                {% endfor %}
              </div>
              <div class="form-check mb-3">
                {{ form.remember_me(class_='form-check-input') }}
                {{ form.remember_me.label(class_='form-check-label') }}
              </div>
              {{ form.submit(class_='btn btn-primary w-100') }}
            </form>
          </div>
        </div>
        {% endblock %}
        """
    )
    write_text(templates_root / "auth" / "login.html", login_html)

    register_html = textwrap.dedent(
        """{% extends 'base.html' %}
        {% block title %}Register{% endblock %}
        {% block navbar %}{% include 'partials/_public_navbar.html' %}{% endblock %}
        {% block content %}
        <div class="row justify-content-center">
          <div class="col-md-6 col-lg-4">
            <h1 class="mb-3">Register</h1>
            <p class="text-muted">Registration is disabled in this starter project. Adapt this
              template when you wire up real user creation.</p>
          </div>
        </div>
        {% endblock %}
        """
    )
    write_text(templates_root / "auth" / "register.html", register_html)

    request_reset_html = textwrap.dedent(
        """{% extends 'base.html' %}
        {% block title %}Request password reset{% endblock %}
        {% block navbar %}{% include 'partials/_public_navbar.html' %}{% endblock %}
        {% block content %}
        <div class="row justify-content-center">
          <div class="col-md-6 col-lg-4">
            <h1 class="mb-3">Reset password</h1>
            <p>Enter the email address associated with your account.</p>
          </div>
        </div>
        {% endblock %}
        """
    )
    write_text(templates_root / "auth" / "request_password_reset.html", request_reset_html)

    reset_password_html = textwrap.dedent(
        """{% extends 'base.html' %}
        {% block title %}Choose a new password{% endblock %}
        {% block navbar %}{% include 'partials/_public_navbar.html' %}{% endblock %}
        {% block content %}
        <div class="row justify-content-center">
          <div class="col-md-6 col-lg-4">
            <h1 class="mb-3">Choose a new password</h1>
          </div>
        </div>
        {% endblock %}
        """
    )
    write_text(templates_root / "auth" / "reset_password.html", reset_password_html)

    # Dashboard
    dashboard_html = textwrap.dedent(
        """{% extends 'base.html' %}
        {% block title %}Dashboard{% endblock %}
        {% block navbar %}{% include 'partials/_dashboard_navbar.html' %}{% endblock %}
        {% block content %}
        <div class="row">
          <div class="col-12">
            <h1 class="mb-3">Dashboard</h1>
            <p class="lead">This is an example of an authenticated-only area of your application.</p>

            <div class="row g-3">
              <div class="col-md-4">
                <div class="card h-100">
                  <div class="card-body">
                    <h5 class="card-title">Metric A</h5>
                    <p class="card-text">Placeholder content for analytics or key metrics.</p>
                  </div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="card h-100">
                  <div class="card-body">
                    <h5 class="card-title">Metric B</h5>
                    <p class="card-text">Highlight something important for signed-in users.</p>
                  </div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="card h-100">
                  <div class="card-body">
                    <h5 class="card-title">Metric C</h5>
                    <p class="card-text">Use this area for actions or shortcuts.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        {% endblock %}
        """
    )
    write_text(templates_root / "dashboard" / "dashboard.html", dashboard_html)

    # Errors - public vs dashboard variants
    error_404_public = textwrap.dedent(
        """{% extends 'base.html' %}
        {% block title %}Page not found{% endblock %}
        {% block navbar %}{% include 'partials/_public_navbar.html' %}{% endblock %}
        {% block content %}
        <div class="text-center py-5">
          <h1 class="display-4">404</h1>
          <p class="lead">The page you are looking for does not exist.</p>
        </div>
        {% endblock %}
        """
    )
    write_text(templates_root / "errors" / "404_public.html", error_404_public)

    error_404_dashboard = textwrap.dedent(
        """{% extends 'base.html' %}
        {% block title %}Page not found{% endblock %}
        {% block navbar %}{% include 'partials/_dashboard_navbar.html' %}{% endblock %}
        {% block content %}
        <div class="text-center py-5">
          <h1 class="display-4">404</h1>
          <p class="lead">The page you are looking for does not exist.</p>
        </div>
        {% endblock %}
        """
    )
    write_text(templates_root / "errors" / "404_dashboard.html", error_404_dashboard)

    error_500_public = textwrap.dedent(
        """{% extends 'base.html' %}
        {% block title %}Server error{% endblock %}
        {% block navbar %}{% include 'partials/_public_navbar.html' %}{% endblock %}
        {% block content %}
        <div class="text-center py-5">
          <h1 class="display-4">500</h1>
          <p class="lead">An unexpected error occurred. Please try again later.</p>
        </div>
        {% endblock %}
        """
    )
    write_text(templates_root / "errors" / "500_public.html", error_500_public)

    error_500_dashboard = textwrap.dedent(
        """{% extends 'base.html' %}
        {% block title %}Server error{% endblock %}
        {% block navbar %}{% include 'partials/_dashboard_navbar.html' %}{% endblock %}
        {% block content %}
        <div class="text-center py-5">
          <h1 class="display-4">500</h1>
          <p class="lead">An unexpected error occurred. Please try again later.</p>
        </div>
        {% endblock %}
        """
    )
    write_text(templates_root / "errors" / "500_dashboard.html", error_500_dashboard)

    # Email templates
    reset_txt = textwrap.dedent(
        """Hello {{ user.username }},

        To reset your password, visit the following link:

        {{ url_for('reset_password', token=token, _external=true) }}

        If you did not request this email, you can ignore it.
        """
    )
    write_text(templates_root / "emails" / "reset_password.txt", reset_txt)

    reset_html = textwrap.dedent(
        """<!doctype html>
        <html>
          <body>
            <p>Hello {{ user.username }},</p>
            <p>To reset your password, click the link below:</p>
            <p><a href="{{ url_for('reset_password', token=token, _external=true) }}">Reset password</a></p>
            <p>If you did not request this email, you can ignore it.</p>
          </body>
        </html>
        """
    )
    write_text(templates_root / "emails" / "reset_password.html", reset_html)


def scaffold_static(project_root: Path) -> None:
    static_root = project_root / "app" / "static"

    main_css = textwrap.dedent(
        """html,
        body {
          height: 100%;
        }

        body {
          min-height: 100%;
          display: flex;
          flex-direction: column;
        }

        main {
          flex: 1 0 auto;
        }

        footer {
          flex-shrink: 0;
        }

        .navbar-brand {
          font-weight: 600;
        }
        """
    )
    write_text(static_root / "css" / "main.css", main_css)

    dashboard_css = textwrap.dedent(
        """body {
          background-color: #f5f5f5;
        }

        .card {
          box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
        }
        """
    )
    write_text(static_root / "css" / "dashboard.css", dashboard_css)

    main_js = textwrap.dedent(
        """document.addEventListener('DOMContentLoaded', () => {
          // Place global JavaScript for your Flask project here.
        });
        """
    )
    write_text(static_root / "js" / "main.js", main_js)

    dashboard_js = textwrap.dedent(
        """document.addEventListener('DOMContentLoaded', () => {
          // Place dashboard-specific JavaScript code here.
        });
        """
    )
    write_text(static_root / "js" / "dashboard.js", dashboard_js)

    # Keep img/ present but empty using a placeholder file
    write_text(static_root / "img" / ".gitkeep", "")


def write_requirements(project_root: Path) -> None:
    requirements = textwrap.dedent(
        """flask
        python-dotenv
        email-validator
        flask-login
        flask-migrate
        flask-sqlalchemy
        flask-moment
        flask-mail
        flask-wtf
        pyjwt
        """
    )
    write_text(project_root / "requirements.txt", requirements)


def write_poetry_files(
    project_root: Path,
    poetry_name: str,
    poetry_version: str,
    poetry_description: str,
    author_name: str,
    author_email: str,
    license_id: str,
    requires_python: str,
) -> None:
    """Write a pyproject.toml for a Poetry-managed application using PEP 621 fields."""

    authors_field = f"{{name = \"{author_name}\", email = \"{author_email}\"}}" if author_email else f"{{name = \"{author_name}\"}}"

    pyproject = textwrap.dedent(
        f"""[project]
        name = "{poetry_name}"
        version = "{poetry_version}"
        description = "{poetry_description}"
        authors = [
            {authors_field}
        ]
        license = {{file = "LICENSE"}}
        readme = "README.md"
        requires-python = "{requires_python}"
        dependencies = []


        [build-system]
        requires = ["poetry-core>=2.0.0,<3.0.0"]
        build-backend = "poetry.core.masonry.api"

        [tool.poetry]
        package-mode = false
        """
    )
    write_text(project_root / "pyproject.toml", pyproject)


def ensure_poetry_alias() -> None:
    """Append alias pf='poetry run flask' to shell rc if not present.

    This check is tolerant of small differences in quoting, so we do not add
    duplicate pf aliases if one already exists.
    """
    system = detect_platform()
    if system in {"macos", "ubuntu", "wsl", "linux"}:
        shell = os.environ.get("SHELL", "")
        if shell.endswith("zsh"):
            rc_path = Path.home() / ".zshrc"
        else:
            rc_path = Path.home() / ".bashrc"
    else:
        # For plain Windows users running this via WSL-like environment, this may be unused.
        rc_path = Path.home() / ".bashrc"

    alias_line = "alias pf='poetry run flask'"

    if rc_path.exists():
        content = rc_path.read_text(encoding="utf-8")
        # Consider any line starting with "alias pf=" as an existing alias,
        # regardless of quote style used.
        for line in content.splitlines():
            if line.strip().startswith("alias pf="):
                print(f"Alias 'pf' already present in {rc_path}.")
                return
    else:
        content = ""

    new_content = content.rstrip("\n") + "\n" + alias_line + "\n"
    rc_path.write_text(new_content, encoding="utf-8")
    print(f"Added alias 'pf' to {rc_path}. You may need to reload your shell.")


def main() -> None:
    print_header()

    option = prompt_choice(
        "Choose your environment workflow:",
        {
            "1": "pyenv + Poetry (pyproject.toml)",
            "2": "pyenv + pyenv-virtualenv + requirements.txt",
            "q": "Quit",
        },
    )

    if option == "q":
        print("Aborting.")
        sys.exit(0)

    if not ensure_prereqs(option):
        sys.exit(1)

    project_name = prompt_with_default("Project folder name (will be created in your home directory)", "flask_project")
    description = prompt_with_default("Short project description", "A starter Flask application.")
    author = prompt_with_default("Author / owner name", "Your Name")

    project_root = ensure_project_dir(project_name)

    print("\nScaffolding Flask project structure...\n")

    use_poetry = option == "1"

    scaffold_top_level_files(project_root, project_name, description, author, use_poetry)
    scaffold_config_and_main(project_root)
    scaffold_models_forms_email_errors(project_root)
    scaffold_utils(project_root)
    scaffold_routes(project_root)
    scaffold_templates(project_root)
    scaffold_static(project_root)

    if use_poetry:
        # Prompt for Poetry/PEP 621 metadata similar to `poetry init`.
        print("\nPoetry configuration (these values will go into pyproject.toml):")
        poetry_name = prompt_with_default("Project name", project_name)
        poetry_version = prompt_with_default("Version", "0.1.0")
        poetry_description = prompt_with_default("Description", description)
        author_name = prompt_with_default("Author name", author)
        author_email = prompt_with_default("Author email", "you@example.com")
        license_id = prompt_with_default("License identifier (used alongside LICENSE file)", "MIT")
        requires_python = prompt_with_default("Required Python version (PEP 440 range)", ">=3.10,<4.0")

        write_poetry_files(
            project_root,
            poetry_name,
            poetry_version,
            poetry_description,
            author_name,
            author_email,
            license_id,
            requires_python,
        )
        ensure_poetry_alias()
    else:
        write_requirements(project_root)

    print("\nDone!\n")
    print(f"Your new Flask project is at: {project_root}")
    print("\nNext steps (summary):")
    print("  1. Create/activate a virtual environment for this project.")
    if use_poetry:
        print("  2. Run `cd", project_root, "&& poetry add \\")
        print("         flask flask-sqlalchemy flask-migrate flask-login flask-wtf flask-mail flask-moment python-dotenv email-validator pyjwt`.")
        print("     This will update pyproject.toml and generate a valid poetry.lock file.")
        print("     If you manually change pyproject.toml later, run `poetry lock` to refresh poetry.lock.")
        print("  3. Start the dev server with `pf run` (alias for `poetry run flask`).")
    else:
        print("  2. Run `cd", project_root, "&& pip install -r requirements.txt`.")
        print("  3. Whenever you change dependencies in that virtualenv, run `pip3 freeze > requirements.txt`.")
        print("  4. Start the dev server with `flask run` (inside the active virtualenv).")


if __name__ == "__main__":
    main()
