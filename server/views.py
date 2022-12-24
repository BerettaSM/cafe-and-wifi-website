from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user

from . import db
from .forms import CafeForm, UserForm, CommentForm
from .models import Cafe, User, Comment
from sqlalchemy import desc, asc, or_

from .custom_decorators import admin_only, anonymous_only


views = Blueprint('views', __name__)


@views.route('/', methods=('GET',))
def home():
    page = request.args.get('page', 1, int)
    per_page = request.args.get('per_page', 12, int)
    pagination = db.paginate(db.select(Cafe).order_by(asc(Cafe.id)), page=page, per_page=per_page )
    return render_template('index.html', pagination=pagination)


@views.route('/search', methods=('GET',))
def search_for():
    page = request.args.get('page', 1, int)
    per_page = request.args.get('per_page', 12, int)
    search_term = request.args.get('search_term', '')
    if search_term == '':
        return redirect(url_for('views.home'))
    pagination = db.paginate(
        db.select(Cafe).filter(
            or_(
                Cafe.name.like('%' + search_term + '%'),
                Cafe.location.like('%' + search_term + '%')
            )
        ).order_by(asc(Cafe.id)), page=page, per_page=per_page
    )
    return render_template('index.html', pagination=pagination, search_term=search_term)


@views.route('/cafe-view/<int:cafe_id>', methods=('GET',))
def view_cafe(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    # cafe = db.session.execute(db.select(Cafe).filter_by(id=cafe_id))
    # cafe.comments.order_by(desc(Comment.comment_author.username))
    form = CommentForm()
    return render_template('cafe_view.html', cafe=cafe, form=form)


@views.route('/cafe-create', methods=('GET', 'POST'))
@admin_only
def create_cafe():
    # Returning a form with radio defaults interferes with front-end js validation,
    # So we must use a normal form for POST requests.
    form = CafeForm() if request.method == 'POST' else CafeForm.with_radio_defaults()
    if form.validate_on_submit():
        cafe = Cafe.create_from(form)
        db.session.add(cafe)
        db.session.commit()
        return redirect(url_for('views.view_cafe', cafe_id=cafe.id))
    return render_template('cafe_form.html', form=form)


@views.route('/edit-cafe/<int:cafe_id>', methods=('GET', 'POST'))
@admin_only
def edit_cafe(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    form = CafeForm.populated_from(cafe)
    if form.validate_on_submit():
        cafe.update_from(form)
        db.session.commit()
        return redirect(url_for('views.view_cafe', cafe_id=cafe.id))
    return render_template('cafe_form.html', form=form)


@views.route('/delete-cafe/<int:cafe_id>', methods=('GET',))
@admin_only
def delete_cafe(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    Comment.query.filter_by(cafe_id=cafe_id).delete()
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('views.home'))


@views.route('/sign-up', methods=('GET', 'POST'))
@anonymous_only
def sign_up():
    form = UserForm()
    if form.validate_on_submit():
        new_user = User.create_from(form)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash(f'Welcome {new_user.username}.', category='success')
        return redirect(url_for('views.home'))
    return render_template('sign-up-view.html', form=form)
