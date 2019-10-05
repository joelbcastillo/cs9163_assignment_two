# -*- coding: utf-8 -*-
"""Click commands."""
import os
import sys
from glob import glob
from subprocess import call

import click
from flask import current_app
from flask.cli import with_appcontext
from werkzeug.exceptions import MethodNotAllowed, NotFound


COV = None
if os.environ.get("FLASK_COVERAGE"):
    import coverage

    COV = coverage.coverage()
    COV.start()
    print("Coverage started")

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, "tests")


@click.command()
@click.option("--test-name", help="Specify tests (file, class, or specific test)")
@click.option(
    "--coverage/--no-coverage",
    "use_coverage",
    default=False,
    help="Run tests under code coverage.",
)
@click.option("--verbose", is_flag=True, default=False, help="pytest verbose mode")
def test(test_name: str = None, use_coverage: bool = False, verbose: bool = False):
    """Run the unit tests using pytest.

    Args:
        test_name (str, optional): Specify tests (file, class, or specific test). Defaults to None.
        use_coverage (bool, optional): Run tests under code coverage.. Defaults to False.
        verbose (bool, optional): Use pytest verbose mode. Defaults to False.
    """
    import pytest
    from sys import exit, argv

    if use_coverage and not os.environ.get("FLASK_COVEERAGE"):
        import subprocess

        os.environ["FLASK_COVERAGE"] = "1"
        exit(subprocess.call(argv))

    command = []

    if verbose:
        command.append("-v")

    if test_name:
        command.append("tests/{test_name}".format(test_name=test_name))
    else:
        command.append("tests/")

    pytest.main(command)

    if COV:
        COV.stop()
        COV.save()
        print("Coverage Summary:")
        COV.report()
        basedir = PROJECT_ROOT
        covdir = os.path.join(basedir, "tmp/coverage")
        COV.html_report(directory=covdir)
        print("HTML version: file://{covdir}/index.html".format(covdir=covdir))
        COV.erase()


@click.command()
def lint():
    """Lint and check code style with black and isort."""
    skip = ["node_modules", "requirements"]
    root_files = glob("*.py")
    root_directories = [
        name for name in next(os.walk("."))[1] if not name.startswith(".")
    ]
    files_and_directories = [
        arg for arg in root_files + root_directories if arg not in skip
    ]

    def execute_tool(description, *args):
        """Execute a checking tool with its arguments."""
        command_line = list(args) + files_and_directories
        click.echo("{}: {}".format(description, " ".join(command_line)))
        rv = call(command_line)
        if rv != 0:
            exit(rv)

    execute_tool("Checking code style", "black", "--check")


@click.command()
def clean():
    """Remove *.pyc and *.pyo files recursively starting at current directory.
    Borrowed from Flask-Script, converted to use Click.
    """
    for dirpath, dirnames, filenames in os.walk("."):
        for filename in filenames:
            if filename.endswith(".pyc") or filename.endswith(".pyo"):
                full_pathname = os.path.join(dirpath, filename)
                click.echo("Removing {}".format(full_pathname))
                os.remove(full_pathname)


@click.command()
@click.option("--url", default=None, help="Url to test (ex. /static/image.png)")
@click.option(
    "--order", default="rule", help="Property on Rule to order by (default: rule)"
)
@with_appcontext
def urls(url, order):
    """Display all of the url matching routes for the project.
    Borrowed from Flask-Script, converted to use Click.
    """
    rows = []
    column_length = 0
    column_headers = ("Rule", "Endpoint", "Arguments")

    if url:
        try:
            rule, arguments = current_app.url_map.bind("localhost").match(
                url, return_rule=True
            )
            rows.append((rule.rule, rule.endpoint, arguments))
            column_length = 3
        except (NotFound, MethodNotAllowed) as e:
            rows.append(("<{}>".format(e), None, None))
            column_length = 1
    else:
        rules = sorted(
            current_app.url_map.iter_rules(), key=lambda rule: getattr(rule, order)
        )
        for rule in rules:
            rows.append((rule.rule, rule.endpoint, None))
        column_length = 2

    str_template = ""
    table_width = 0

    if column_length >= 1:
        max_rule_length = max(len(r[0]) for r in rows)
        max_rule_length = max_rule_length if max_rule_length > 4 else 4
        str_template += "{:" + str(max_rule_length) + "}"
        table_width += max_rule_length

    if column_length >= 2:
        max_endpoint_length = max(len(str(r[1])) for r in rows)
        # max_endpoint_length = max(rows, key=len)
        max_endpoint_length = max_endpoint_length if max_endpoint_length > 8 else 8
        str_template += "  {:" + str(max_endpoint_length) + "}"
        table_width += 2 + max_endpoint_length

    if column_length >= 3:
        max_arguments_length = max(len(str(r[2])) for r in rows)
        max_arguments_length = max_arguments_length if max_arguments_length > 9 else 9
        str_template += "  {:" + str(max_arguments_length) + "}"
        table_width += 2 + max_arguments_length

    click.echo(str_template.format(*column_headers[:column_length]))
    click.echo("-" * table_width)

    for row in rows:
        click.echo(str_template.format(*row[:column_length]))


@click.command()
@click.option(
    "-f",
    "--fix-imports",
    default=False,
    is_flag=True,
    help="Fix imports using isort, before formatting",
)
def blacken(fix_imports):
    """Reformat code using black and isort."""
    skip = ["node_modules", "requirements"]
    root_files = glob("*.py")
    root_directories = [
        name for name in next(os.walk("."))[1] if not name.startswith(".")
    ]
    files_and_directories = [
        arg for arg in root_files + root_directories if arg not in skip
    ]

    def execute_tool(description, *args):
        """Execute a checking tool with its arguments."""
        command_line = list(args) + files_and_directories
        click.echo("{}: {}".format(description, " ".join(command_line)))
        rv = call(command_line)
        if rv != 0:
            exit(rv)

    if fix_imports:
        execute_tool("Fixing import order", "isort", "-rc")
    execute_tool("Formatting project", "black")
