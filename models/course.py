from google.appengine.ext import ndb

from protorpc import messages

class Course(ndb.Model):
    label = ndb.StringProperty()
    description = ndb.TextProperty()

    @property
    def serialize(self):
        return {
            'id': self.key,
            'label': self.label,
            'description': self.description
        }

class CourseForm(messages.Message):
    label = messages.StringField(1)
    description = messages.StringField(2)
    websafeKey = messages.StringField(3)

class CourseForms(messages.Message):
    """CourseForms -- multiple Course outbound form message"""
    courses = messages.MessageField(CourseForm, 1, repeated=True)

