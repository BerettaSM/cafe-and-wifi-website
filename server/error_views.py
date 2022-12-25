from flask import render_template
from http import HTTPStatus


def page_not_found(e):
    return render_template('404.html'), HTTPStatus.NOT_FOUND


def resource_forbidden(e):
    return render_template('403.html'), HTTPStatus.FORBIDDEN

