from google.appengine.ext import ndb

from protorpc import messages

from models.course import Course
from models.course import CourseForm
from models.course import CourseForms

class Profile(ndb.Model):
    """Profile -- User profile object"""
    display_name = ndb.StringProperty()
    email = ndb.StringProperty(repeated=True)
    roles = ndb.KeyProperty(kind="Role", repeated=True)

    @property
    def serialize(self):
        return {
            'id': self.key.id,
            'display_name': self.display_name,
            'email': self.email
        }

class Role(ndb.Model):
    """Role -- Privilege role object"""
    label = ndb.StringProperty()

    @property
    def members(self):
        """Get role members"""
        return Profile.query.filter()

    def add_member(self, profile):
        """Add role member"""
        self.members.append(profile.key)
        self.put()

class RoleMember(ndb.Model):
    pass

class Skill(ndb.Model):
    pass

class Exercise(ndb.Model):
    pass

class Quiz(ndb.Model):
    pass
