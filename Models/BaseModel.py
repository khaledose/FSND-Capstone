from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BaseModel:
    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.insert()
    '''
    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as error:
            print("An error occured while inserting " + self + "with error " + error)
            db.session.rollback()
        finally:
            db.session.close()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.delete()
    '''
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as error:
            print("An error occured while deleting " + self + "with error " + error)
            db.session.rollback()
        finally:
            db.session.close()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink.query.filter(Drink.id == id).one_or_none()
            drink.title = 'Black Coffee'
            drink.update()
    '''
    def update(self):
        try:
            db.session.commit()
        except Exception as error:
            print("An error occured while updating " + self + "with error " + error)
            db.session.rollback()
        finally:
            db.session.close()