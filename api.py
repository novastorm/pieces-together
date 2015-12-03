import endpoints

from routes.courses import CoursesAPI

api = endpoints.api_server([CoursesAPI])


