from ..database import db

class BaseRepository:
    def getAll(self):
        raise NotImplementedError

    def get(self, id):
        raise NotImplementedError

    def post(self, request):
        raise NotImplementedError

    def update(self, id, request):
        raise NotImplementedError

    def delete(self, id):
        try:
            model = self.get(id)
            db.session.delete(model)
            db.session.commit()
            return model
        except Exception as error:
            db.session.rollback()

    def close(self):
        db.session.rollback()
