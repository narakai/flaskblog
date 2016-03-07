import datetime, re
from app import db


# A post about Flask -> a-post-about-flask
def slugify(s):
	return re.sub('[^\w]+', '-', s).lower()


class Entry(db.Model):
	# set for us automatically by the database
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	# The URL-friendly representation of the title
	slug = db.Column(db.String(100), unique=True)
	body = db.Column(db.Text)
	created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
	modified_timestamp = db.Column(
		db.DateTime,
		default=datetime.datetime.now,
		onupdate=datetime.datetime.now)

	def __init__(self, *args, **kwargs):
		super(Entry, self).__init__(*args, **kwargs)  # Call parent constructor.
		self.generate_slug()

	def generate_slug(self):
		self.slug = ''
		if self.title:
			self.slug = slugify(self.title)

	def __repr__(self):
		return '<Entry: %s>' % self.title
