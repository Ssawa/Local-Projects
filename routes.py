from flask import Blueprint, render_template
import db

routes = Blueprint('routes', __name__)

@routes.route('/')
def tokens():
    return render_template('tokens.html', tokens=db.getTokens())
