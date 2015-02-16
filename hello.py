import os
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello World!'


if __name__ == '__main__':
	# Heroku handles the binding of ports itself and will pass
	# us what port it will use with the $PORT enviroment variable.
	# However, we still want to use the default port 5000 when testing
	# locally.
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
