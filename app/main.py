from flask import request, session
from app import app, db
import admin
import views
import models
import api
from entries.blueprint import entries
app.register_blueprint(entries, url_prefix='/entries')


if __name__ == '__main__':
	app.run()