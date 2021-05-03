import datetime
from parsers import SiteParser, RedNoticeParser, RestCountry
from db.models import Country, Notice, Nationality, session
from time import sleep
from sqlalchemy import exc
interpol = SiteParser()
notices = RedNoticeParser()


def populate_countries_list():
    countries_dict = interpol.countries_dict()
    for name, code in countries_dict.items():
        session.add(Country(name=name, code=code))

    session.commit()


def get_country(code):
    country = session.query(Country).filter(Country.code == code).first()
    return country


def populate_countries_data():
    for country in session.query(Country).all():
        country.population = RestCountry(country.code).population
        country.total_notices = notices.nationality_total(country.code)
    session.commit()


def transform_date(string):
    if isinstance(string, str):
        if len(string.split('/')) == 3:
            return datetime.datetime.strptime(string, "%Y/%m/%d")
        else:
            return datetime.datetime.strptime(string[0:4], "%Y")


def populate_notices_data():
    countries = session.query(Country).all()[4:]
    for country in countries:

        for entity in notices.get_notices_for_nationality(country.code):

            entity_id = entity.get("entity_id")
            entity_data = notices.get_entity_data(entity_id)

            date_of_birth = transform_date(entity_data.get('date_of_birth'))
            try:
                obj = Notice(entity_id=entity_id,
                             date_of_birth=date_of_birth,
                             country=country.code,
                             sex=entity_data.get('sex'),
                             place_of_birth=entity_data.get('place_of_birth'),
                             charge=entity_data.get("charge")
                             )
                nationalities = entity_data.get('nationalities')
                print(country, entity_id)
                # for nation in nationalities:
                #     nation_obj = session.query(Country).filter(Country.code == nation).first()
                #     obj.nationalities.append(nation_obj)
                session.add(obj)
                session.commit()
            except exc.IntegrityError:
                session.rollback()
            sleep(1)


#
#
# populate_notices_data()

