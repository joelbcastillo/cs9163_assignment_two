# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""

import pytest
from webtest import TestApp

from spell_check.app import create_app


@pytest.fixture
def app():
    """An application for the tests."""
    _app = create_app("tests.settings")
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def testapp(app):
    """A Webtest app."""
    return TestApp(app)
