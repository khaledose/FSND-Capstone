from ..models.User import User
from .BaseRepository import BaseRepository
from ..database import db

class UsersRepository(BaseRepository):
    def getAll(self):
        return User.query.all()

    def get(self, id):
        return User.query.get(id)

    def getByEmail(self, email):
        return User.query.filter_by(email=email).first()

    def register(self, body):
        try:
            newUser = User(id=body.get('sub', None),
                        firstName=body.get('given_name', None),
                        lastName=body.get('family_name', None),
                        email=body.get('email', None))
            db.session.add(newUser)
            db.session.commit()
            return newUser
        except Exception as error:
            db.session.rollback()

    def update(self, body, id):
        try:
            user = self.get(id)
            user.firstName = body.get('given_name', user.firstName)
            user.lastName  = body.get('family_name', user.lastName)
            user.email  = body.get('email', user.email)
            db.session.commit()
            return user
        except Exception as error:
            db.session.rollback()
