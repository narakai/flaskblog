from app import app


@app.route('/')
def homapage():
	return 'Home Page'
