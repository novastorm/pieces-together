from flask import Blueprint
from flask import abort
from flask import flash
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import session as login_session
from flask import url_for

from google.appengine.api import memcache
from google.appengine.api import taskqueue
from google.appengine.ext import ndb

from models import Course
from models import Profile
from models import Role

from settings import WEB_CLIENT_ID

course = Blueprint('course', __name__)

@course.route('/courses')
def showCourseMasterDetail():
    courses = Course.query()
    return jsonify(Courses=[course.serialize for course in courses.fetch()])