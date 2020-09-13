from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base


class Sqlite():
    def __init__(self):
        self.engine = create_engine('sqlite:///database/data.db', echo=True)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def create_db(self):
        return Base.metadata.create_all(bind=self.engine)

    def query(self,model,**kwargs):
        var = self.session.query(model).filter_by(**kwargs).first()
        self.close()
        return var

    def query_all(self,model):
        var = self.session.query(model).all()
        self.close()
        return var

    def create(self,model,**kwargs):
        var = model(**kwargs)
        self.session.add(var)
        self.session.commit()
        self.close()

    def update(self,model,model_id,**kwargs):
        self.session.query(model).filter_by(id=model_id).update(kwargs)
        self.session.commit()

    def delete(self,model,id):
        self.session.query(model).filter_by(id=id).delete()
        self.session.commit()
        self.close()
    def close(self):
        return self.session.close()

# a = Sqlite().create_db()