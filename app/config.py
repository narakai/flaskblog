import os


class Configuration(object):
	APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
	DEBUG = True
	# dialect+driver://username:password@host:port/database
	SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/blog.db' % APPLICATION_DIR
