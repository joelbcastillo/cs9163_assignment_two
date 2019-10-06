# -*- coding: utf-8 -*-
from spell_check.app import create_app
from tests import settings


def test_config():
    assert not create_app().testing
    assert create_app(settings).testing
