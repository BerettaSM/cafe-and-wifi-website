from flask import Blueprint, url_for, redirect, request, flash
from flask_login import current_user

from . import db
from .custom_decorators import authenticated_only
from .forms import CommentForm
from .models import Comment


comments = Blueprint('comments', __name__)


@comments.route('/comment/<int:cafe_id>', methods=('POST',))
@authenticated_only
def add_comment(cafe_id):
    comment = CommentForm()
    if comment.validate_on_submit():
        new_comment = Comment(
            text=comment.text.data,
            author_id=current_user.id,
            cafe_id=cafe_id
        )
        db.session.add(new_comment)
        db.session.commit()
    else:
        flash('Your comment was not sent.', category='error')
    return redirect(url_for('views.view_cafe', cafe_id=cafe_id))


@comments.route('/delete-comment/<int:comment_id>', methods=('GET',))
@authenticated_only
def delete_comment(comment_id):
    comment_to_delete = Comment.query.get(comment_id)
    current_view = request.environ['HTTP_REFERER']
    if comment_to_delete.author_id == current_user.id or current_user.has_admin_privileges:
        db.session.delete(comment_to_delete)
        db.session.commit()
    return redirect(current_view)
