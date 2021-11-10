from ..database import db
from sqlalchemy import Column, String, Integer

class Book(db.Model):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(80), unique=True)
    description = Column(String(300))
    author = Column(String(80))

    def __repr__(self) -> str:
        return str(self.to_dict())

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'author': self.author
        }