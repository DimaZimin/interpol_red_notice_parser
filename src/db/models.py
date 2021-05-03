from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, Sequence, Date, ForeignKey, Text
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
        return "<Country(name='%s', code='%s', population='%s', total_notices='%s')>" % (
            self.name, self.code, self.population, self.total_notices
        )


class Notice(Base):
    __tablename__ = 'notice'

    id = Column('id', Integer, Sequence('notice_id_seq'), primary_key=True)
    entity_id = Column('entity_id', String(100), unique=True)
    date_of_birth = Column('date_of_birth', Date)
    nationalities = relationship(Country, secondary='nationality')
    country = Column('country', String(200))
    sex = Column('sex', String(10))
    place_of_birth = Column('place_of_birth', String(200))
    charge = Column('charge', Text)


class Nationality(Base):
    __tablename__ = 'nationality'
    nationality_id = Column(Integer, ForeignKey('country.id'), primary_key=True)
    notice_id = Column(Integer, ForeignKey('notice.id'), primary_key=True)


Base.metadata.create_all(bind=engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
