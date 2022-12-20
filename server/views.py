from flask import Blueprint, render_template, request
from flask_sqlalchemy.pagination import QueryPagination
from .models import Cafe


views = Blueprint('views', __name__)


@views.route('/', methods=('GET',))
def home():
    page = request.args.get('page', 1, int)
    pagination: QueryPagination = Cafe.query.paginate(page=page, per_page=12)
    return render_template('index.html', pagination=pagination)


@views.route('/cafe/<int:cafe_id>')
def view_cafe(cafe_id):
    cafe = Cafe.query.filter_by(id=cafe_id).first()
    return render_template('cafe_view.html', cafe=cafe)
