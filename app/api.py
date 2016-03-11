from app import api
from flask.ext.restless import ProcessingException
from models import Comment
from entries.forms import CommentForm


def post_preprocessor(data, **kwargs):
	form = CommentForm(data=data)
	if form.validate():
		return form.data
	else:
		raise ProcessingException(
			description='Invalid form submission.',
			code=400)


api.create_api(Comment, include_columns=['id', 'name', 'url', 'body', 'created_timestamp'],
			   include_methods=['gravatar'],
			   methods=['GET', 'POST'], preprocessors={'POST': [post_preprocessor]})
