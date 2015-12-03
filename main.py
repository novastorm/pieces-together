"""
main.py --
"""

__author__ = 'adland@4mfd.com (Adland Lee)'

from flask import Flask

from routes.courses import courses as course_bp


app = Flask(__name__)
app.config['DEBUG'] = True

app.register_blueprint(course_bp, url_prefix='/courses')

@app.route('/')
def showHome():
    """Return Home view"""
    return 'Home View'
