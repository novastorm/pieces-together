"""
main.py --
"""

__author__ = 'adland@4mfd.com (Adland Lee)'

from flask import Flask
from flask import render_template

from routes.courses import courses as course_bp


app = Flask(__name__)
app.config['DEBUG'] = True

app.register_blueprint(course_bp, url_prefix='/courses')

@app.route('/')
@app.route('/home')
def showHome():
    """Return Home view"""
    template_file = 'home_view.j2'
    return render_template(template_file)
