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

    def register(self, request):
        try:
            newUser = User(firstName=request.get('given_name', None),
                        lastName=request.get('family_name', None),
                        email=request.get('email', None))
            db.session.add(newUser)
            db.session.commit()
            return newUser
        except Exception as error:
            db.session.rollback()

    def update(self, request, profile):
        try:
            user = User.query.get(profile['id'])
            print(user)
            response = request.get_json()
            user.firstName = response.get('given_name', user.firstName)
            user.lastName  = response.get('family_name', user.lastName)
            user.email  = response.get('email', user.email)
            db.session.commit()
            return user
        except Exception as error:
            db.session.rollback()
