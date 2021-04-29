from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, Sequence
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///data.db', echo=True)
Base = declarative_base()


class Country(Base):

    __tablename__ = 'country'

    id = Column('id', Integer, Sequence('country_id_seq'), primary_key=True)
    name = Column('name', String(100), unique=True)
    code = Column('code', String(100), unique=True)
    population = Column('population', Integer)
    total_notices = Column('total_notices', Integer)

    def __repr__(self):
        return "<Country(name='%s', code='%s')>" % (self.name, self.code)


Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

