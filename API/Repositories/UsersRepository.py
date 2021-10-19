from Models.User import User
from Repositories.BaseRepository import BaseRepository
from database import db

class UsersRepository(BaseRepository):
    def getAll(self):
        return User.query.all()

    def get(self, id):
        return User.query.get(id)

    def post(self, request):
        try:
            response = request.get_json()
            newUser = User(username=response.get('username', None),
                        email=response.get('email', None))
            db.session.add(newUser)
            db.session.commit()
            return newUser
        except Exception as error:
            db.session.rollback()

    def update(self, id, request):
        try:
            user = self.get(id)
            response = request.get_json()
            user.username = response.get('username', None)
            user.email  = response.get('email', None)
            db.session.commit()
            return user
        except Exception as error:
            db.session.rollback()
