# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

from spell_check.utils import flash_errors

blueprint = Blueprint("main", __name__, static_folder="../static", static_url_path="/")


@blueprint.route("/")
def main():
    return render_template('main/home.html')