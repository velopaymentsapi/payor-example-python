from api.database import db
from sqlalchemy.dialects.postgresql import JSON, UUID

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    api_key = db.Column(UUID(as_uuid=True))
    is_active = db.Column(db.Boolean())

    def __init__(self, username, password, api_key, is_active):
        self.username = username
        self.password = password
        self.api_key = api_key
        self.is_active = is_active

    def __repr__(self):
        return '<username {}>'.format(self.username)
