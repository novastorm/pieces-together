import endpoints

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

from google.net.proto.ProtocolBuffer import ProtocolBufferDecodeError

from models.course import Course

from protorpc import messages
from protorpc import message_types
from protorpc import remote

from settings import WEB_CLIENT_ID

courses = Blueprint('courses', __name__)

def _getCourseIndex():
    return "Show Course Index"

def _getCourseList():
    return Course.query().fetch()

def _showCourse(form):
    """Show course object, return CourseRequest"""
    course_wsk = getattr(form, 'websafeCourseKey')
    try:
        aCourse = ndb.Key(urlsafe=course_wsk).get()
    except (TypeError) as e:
        raise endpoints.NotFoundException(
            'Invalid input course key string: [%s]' % course_wsk)
    except (ProtocolBufferDecodeError) as e:
        raise endpoints.NotFoundException(
            'No course found with key: [%s]' % course_wsk)
    except Exception as e:
        raise endpoints.NotFoundException('%s: %s' % (e.__class__.__name__, e))

    return aCourse

def _createCourse():
    return "Show Create Course"

def _storeCourse():
    return "Store Course"
    """Store course object, return CourseForm."""

    if not request.label:
        raise endpoints.BadRequestException(
            "Course 'label' field required")

    data = {field.name: getattr(request, field.name) for field in request.all_fields()}
    del data['websafeKey']

    Course(**data).put()
    return request

def _editCourse():
    return "Show edit course"

def _updateCourse():
    return "Update Course"

def _deleteCourse():
    return "Show delete course"

def _destroyCourse():
    return "Destroy course"


###############################################################################
#
# web routes
#

@courses.route('/')
def showCourseIndex():
    return _getCourseIndex()

@courses.route('/<string:course_label>')
def showCourse(course_label):
    # data = request.values.to_dict()
    # data['websafeCourseKey'] = course_label
    setattr(request, 'websafeCourseKey', course_label)
    return _showCourse(request)

@courses.route('/create', methods=['GET', 'POST'])
def createCourse():
    if request.method == 'POST':
        return _storeCourse(request)

    return _createCourse()

@courses.route('/<string:course_label>/edit', methods=['GET', 'POST'])
def editCourse(course_label):
    if request.method == 'POST':
        return _updateCourse()

    return _editCourse()

@courses.route('/<string:course_label>/delete', methods=['GET', 'POST'])
def deleteCourse(course_label):
    if request.method == 'POST':
        return _destroyCourse()

    return _deleteCourse()


###############################################################################
#
# API routes
#

EMAIL_SCOPE = endpoints.EMAIL_SCOPE
API_EXPLORER_CLIENT_ID = endpoints.API_EXPLORER_CLIENT_ID

class CourseRequest(messages.Message):
    label = messages.StringField(1)
    description = messages.StringField(2)

class CourseResponse(messages.Message):
    label = messages.StringField(1)
    description = messages.StringField(2)
    websafeKey = messages.StringField(3)

class CourseListResponse(messages.Message):
    """CourseListResponse -- multiple Course outbound form message"""
    courses = messages.MessageField(CourseResponse, 1, repeated=True)

COURSE_SHOW_REQUEST = endpoints.ResourceContainer(
    message_types.VoidMessage,
    websafeCourseKey=messages.StringField(1))

COURSE_EDIT_REQUEST = endpoints.ResourceContainer(
    CourseRequest,
    websafeCourseKey=messages.StringField(1))

COURSE_DELETE_REQUEST = COURSE_SHOW_REQUEST

@endpoints.api(
    name='courses',
    version='v1',
    allowed_client_ids=[WEB_CLIENT_ID],
    scopes=[EMAIL_SCOPE])
class CoursesAPI(remote.Service):
    """Pieces Together API v0.1"""

    def _copyToCourseResponse(self, course):
        """Copy relevant field from Course to CourseRequest."""
        response = CourseResponse()
        for field in response.all_fields():
            if hasattr(course, field.name):
                setattr(response, field.name, getattr(course, field.name))
            elif field.name == "websafeKey":
                setattr(response, field.name, course.key.urlsafe())
        response.check_initialized()
        return response

    def _createCourseObject(self, form):
        """Create course object, return CourseRequest."""

        if not form.label:
            raise endpoints.BadRequestException(
                "Course 'label' field required")

        data = {field.name: getattr(form, field.name) for field in form.all_fields()}
        del data['websafeKey']

        Course(**data).put()
        return form

    # def _showCourseObject(self, form):
    #     """Show course object, return CourseRequest"""
    #     try:
    #         a_course = ndb.Key(urlsafe=form.websafeCourseKey).get()
    #     except (TypeError) as e:
    #         raise endpoints.NotFoundException(
    #             'Invalid input course key string: [%s]' % form.websafeCourseKey)
    #     except (ProtocolBufferDecodeError) as e:
    #         raise endpoints.NotFoundException(
    #             'No course found with key: [%s]' % form.websafeCourseKey)
    #     except Exception as e:
    #         raise endpoints.NotFoundException('%s: %s' % (e.__class__.__name__, e))

    #     return self._copyToCourseResponse(a_course)

    def _updateCourseObject(self, form):
        """Update course object, return CourseRequest"""

        try:
            a_course = ndb.Key(urlsafe=form.websafeCourseKey).get()
        except (TypeError) as e:
            raise endpoints.NotFoundException(
                'Invalid input course key string: [%s]' % form.websafeCourseKey)
        except (ProtocolBufferDecodeError) as e:
            raise endpoints.NotFoundException(
                'No course found with key: [%s]' % form.websafeCourseKey)
        except Exception as e:
            raise endpoints.NotFoundException('%s: %s' % (e.__class__.__name__, e))

        data = {field.name: getattr(form, field.name) for field in form.all_fields()}

        for field in form.all_fields():
            data = getattr(form, field.name)
            if data == "":
                delattr(a_course, field.name)
            elif data not in (None, []):
                setattr(a_course, field.name, data)
        a_course.put()

        return self._copyToCourseResponse(a_course)

    def _deleteCourseObject(self, form):
        """delete course object, return CourseRequest"""

        try:
            a_course_key = ndb.Key(urlsafe=form.websafeCourseKey)
            a_course = a_course_key.get()
        except (TypeError) as e:
            raise endpoints.NotFoundException(
                'Invalid input course key string: [%s]' % form.websafeCourseKey)
        except (ProtocolBufferDecodeError) as e:
            raise endpoints.NotFoundException(
                'No course found with key: [%s]' % form.websafeCourseKey)
        except Exception as e:
            raise endpoints.NotFoundException('%s: %s' % (e.__class__.__name__, e))

        a_course_key.delete()

        return self._copyToCourseResponse(a_course)

    @endpoints.method(message_types.VoidMessage, CourseListResponse,
        path='courses',
        http_method='GET',
        name='list')
    def listCourses(self, form):
        """Get list of courses"""
        records = _getCourseList()
        return CourseListResponse(
            courses=[self._copyToCourseResponse(record) for record in records]
        )

    @endpoints.method(COURSE_SHOW_REQUEST, CourseResponse,
        path='courses/{websafeCourseKey}',
        http_method='GET',
        name='show')
    def showCourse(self, form):
        """Show course detail (by websafeCourseKey)"""
        record = _showCourse(form)
        return self._copyToCourseResponse(record)

    @endpoints.method(CourseRequest, CourseResponse,
        path='courses',
        http_method='POST',
        name='store')
    def storeCourse(self, form):
        """Create new course"""
        return _storeCourse(form)

    @endpoints.method(COURSE_EDIT_REQUEST, CourseResponse,
        path='courses/{websafeCourseKey}',
        http_method='PUT',
        name='update')
    def updateCourse(self, form):
        """Update course detail (by websafeCourseKey)"""
        return _updateCourse(form)

    @endpoints.method(COURSE_DELETE_REQUEST, CourseResponse,
        path='courses/{websafeCourseKey}',
        http_method='DELETE',
        name='destroy')
    def destroyCourse(self, form):
        """Destroy course (by websafeCourseKey)"""
        return _destroyCourse(form)
