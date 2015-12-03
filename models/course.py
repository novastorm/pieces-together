from google.appengine.ext import ndb

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

