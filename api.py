import endpoints

from flask import Blueprint
from flask import abort
from flask import jsonify
from flask import session as login_session

from google.appengine.api import memcache
from google.appengine.api import taskqueue
from google.appengine.ext import ndb

from google.net.proto.ProtocolBuffer import ProtocolBufferDecodeError

from models.course import Course
from models.course import CourseForm
from models.course import CourseForms
# from models.profile import Profile
# from models.role import Role

from protorpc import messages
from protorpc import message_types
from protorpc import remote

from routes.courses import courses_api

# from settings import WEB_CLIENT_ID

# EMAIL_SCOPE = endpoints.EMAIL_SCOPE
# API_EXPLORER_CLIENT_ID = endpoints.API_EXPLORER_CLIENT_ID


# COURSE_GET_REQUEST = endpoints.ResourceContainer(
#     message_types.VoidMessage,
#     websafeCourseKey=messages.StringField(1))

# COURSE_POST_REQUEST = endpoints.ResourceContainer(
#     CourseForm,
#     websafeCourseKey=messages.StringField(1))

# courses_api = endpoints.api(
#     name='courses',
#     version='v1',
#     allowed_client_ids=[WEB_CLIENT_ID],
#     scopes=[EMAIL_SCOPE])
# @courses_api.api_class(resource_name='courses')
# class CoursesApi(remote.Service):
#     """Pieces Together API v0.1"""

# ###############################################################################
# #
# # Course API routes
# #

#     def _copyCourseToForm(self, course):
#         """Copy relevant field from Course to CourseForm."""
#         a_course_form = CourseForm()
#         for field in a_course_form.all_fields():
#             if hasattr(course, field.name):
#                 setattr(a_course_form, field.name, getattr(course, field.name))
#             elif field.name == "websafeKey":
#                 setattr(a_course_form, field.name, course.key.urlsafe())
#         a_course_form.check_initialized()
#         return a_course_form

#     def _createCourseObject(self, request):
#         """Create course object, return CourseForm."""

#         if not request.label:
#             raise endpoints.BadRequestException(
#                 "Course 'label' field required")

#         data = {field.name: getattr(request, field.name) for field in request.all_fields()}
#         del data['websafeKey']

#         Course(**data).put()
#         return request

#     def _showCourseObject(self, request):
#         """Show course object, return CourseForm"""
#         try:
#             a_course = ndb.Key(urlsafe=request.websafeCourseKey).get()
#         except (TypeError) as e:
#             raise endpoints.NotFoundException(
#                 'Invalid input course key string: [%s]' % request.websafeCourseKey)
#         except (ProtocolBufferDecodeError) as e:
#             raise endpoints.NotFoundException(
#                 'No course found with key: [%s]' % request.websafeCourseKey)
#         except Exception as e:
#             raise endpoints.NotFoundException('%s: %s' % (e.__class__.__name__, e))

#         return self._copyCourseToForm(a_course)

#     def _updateCourseObject(self, request):
#         """Update course object, return CourseForm"""

#         try:
#             a_course = ndb.Key(urlsafe=request.websafeCourseKey).get()
#         except (TypeError) as e:
#             raise endpoints.NotFoundException(
#                 'Invalid input course key string: [%s]' % request.websafeCourseKey)
#         except (ProtocolBufferDecodeError) as e:
#             raise endpoints.NotFoundException(
#                 'No course found with key: [%s]' % request.websafeCourseKey)
#         except Exception as e:
#             raise endpoints.NotFoundException('%s: %s' % (e.__class__.__name__, e))

#         data = {field.name: getattr(request, field.name) for field in request.all_fields()}

#         for field in request.all_fields():
#             data = getattr(request, field.name)
#             if data == "":
#                 delattr(a_course, field.name)
#             elif data not in (None, []):
#                 setattr(a_course, field.name, data)
#         a_course.put()

#         return self._copyCourseToForm(a_course)

#     def _deleteCourseObject(self, request):
#         """delete course object, return CourseForm"""

#         try:
#             a_course_key = ndb.Key(urlsafe=request.websafeCourseKey)
#             a_course = a_course_key.get()
#         except (TypeError) as e:
#             raise endpoints.NotFoundException(
#                 'Invalid input course key string: [%s]' % request.websafeCourseKey)
#         except (ProtocolBufferDecodeError) as e:
#             raise endpoints.NotFoundException(
#                 'No course found with key: [%s]' % request.websafeCourseKey)
#         except Exception as e:
#             raise endpoints.NotFoundException('%s: %s' % (e.__class__.__name__, e))

#         a_course_key.delete()

#         return self._copyCourseToForm(a_course)

#     @endpoints.method(message_types.VoidMessage, CourseForms,
#         path='courses',
#         http_method='GET',
#         name='listCourses')
#     def listCourses(self, request):
#         """Get list of courses"""
#         courses = Course.query().fetch()
#         return CourseForms(
#             courses=[self._copyCourseToForm(course) for course in courses]
#         )

#     @endpoints.method(CourseForm, CourseForm,
#         path='courses',
#         http_method='POST',
#         name='createCourse')
#     def createCourse(self, request):
#         """Create new course"""
#         return self._createCourseObject(request)

#     @endpoints.method(COURSE_GET_REQUEST, CourseForm,
#         path='courses/{websafeCourseKey}',
#         http_method='GET',
#         name='showCourse')
#     def showCourse(self, request):
#         """Show course detail (by websafeCourseKey)"""
#         return self._showCourseObject(request)

#     @endpoints.method(COURSE_POST_REQUEST, CourseForm,
#         path='courses/{websafeCourseKey}',
#         http_method='PUT',
#         name='updateCourse')
#     def updateCourse(self, request):
#         """Update course detail (by websafeCourseKey)"""
#         return self._updateCourseObject(request)

#     @endpoints.method(COURSE_GET_REQUEST, CourseForm,
#         path='courses/{websafeCourseKey}',
#         http_method='DELETE',
#         name='deleteCourse')
#     def deleteCourse(self, request):
#         """Delete course (by websafeCourseKey)"""
#         return self._deleteCourseObject(request)


api = endpoints.api_server([courses_api])
