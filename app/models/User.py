from ..database import db
from sqlalchemy import Column, String, Integer

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(80), unique=True, nullable=False)

    def __repr__(self) -> str:
        return str(self.to_dict())

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }