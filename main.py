"""
main.py --
"""

__author__ = 'adland@4mfd.com (Adland Lee)'

from flask import Flask

from routes.course import course


app = Flask(__name__)
app.config['DEBUG'] = True

app.register_blueprint(course)

@app.route('/')
def showHome():
    """Return Home view"""
    return 'Home View'
