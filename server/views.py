from flask import Blueprint, render_template, request, redirect, url_for
from flask_sqlalchemy.pagination import QueryPagination
from .models import Cafe
from .forms import CafeForm

from . import db


views = Blueprint('views', __name__)


@views.route('/', methods=('GET',))
def home():
    page = request.args.get('page', 1, int)
    pagination: QueryPagination = Cafe.query.paginate(page=page, per_page=12)
    return render_template('index.html', pagination=pagination)


@views.route('/cafe-view/<int:cafe_id>', methods=('GET',))
def view_cafe(cafe_id):
    cafe = Cafe.query.filter_by(id=cafe_id).first()
    return render_template('cafe_view.html', cafe=cafe)


@views.route('/cafe', methods=('GET', 'POST'))
def create_cafe():
    # Returning a form with radio defaults interferes with front-end js validation,
    # So we must use a normal form for POST requests.
    form = CafeForm() if request.method == 'POST' else CafeForm.with_radio_defaults()
    if form.validate_on_submit():
        cafe = Cafe.create_from(form)
        db.session.add(cafe)
        db.session.commit()
        return redirect(url_for('views.view_cafe', cafe_id=cafe.id))
    return render_template('cafe_edit.html', form=form)


@views.route('/edit-cafe/<int:cafe_id>', methods=('GET', 'POST'))
def edit_cafe(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    form = CafeForm.populated_from(cafe)
    if form.validate_on_submit():
        cafe.update_from(form)
        db.session.commit()
        return redirect(url_for('views.view_cafe', cafe_id=cafe.id))
    return render_template('cafe_edit.html', form=form)


@views.route('/delete-cafe/<int:cafe_id>', methods=('GET',))
def delete_cafe(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('views.home'))
