from app import app
from flask import render_template, request


@app.route('/')
def homapage():
	name = request.args.get('name')
	number = request.args.get('number')
	return render_template('homepage.html', name=name, number=number)
