from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Geolocation(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True,unique=True,autoincrement=False,nullable=False)
    name_geolocation = Column(String(50),nullable=False,unique=True)
    longtitude = Column(Float)
    latitude = Column(Float)
    hashtag1 = Column(String(255))
    hashtag2 = Column(String(255))

    def __repr__(self):
        return "<(name='%s', id='%s')>" % (
            self.name_geolocation, self.id)



