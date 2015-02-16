from flask import Flask
from flask import render_template
import os

from routes import routes

app = Flask(__name__)
app.register_blueprint(routes)

if __name__ == '__main__':
    # Heroku handles the binding of ports itself and will pass
    # us what port it will use with the $PORT enviroment variable.
    # However, we still want to use the default port 5000 when testing
    # locally.
    port = int(os.environ.get("PORT", 5000))
    debug =  True if os.getenv("DEBUG") == 'True' else False
    app.run(host='0.0.0.0', port=port, debug=debug)
