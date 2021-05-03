from db.models import Country, Notice, session
from sqlalchemy import desc, func
import datetime


class Stats:
    def __init__(self, db_session):
        self.session = db_session

    def notice_ordered_per_country(self):
        all_countries = self.session.query(Country)
        ordered_list = all_countries.order_by(desc(Country.total_notices)).all()
        data = {}
        for country in ordered_list:
            data[country.name] = country.total_notices
        return data

    @property
    def total_notices(self):
        total = self.session.query(func.sum(Country.total_notices)).one()
        return int(total[0])

    def notice_per_hundred_thousand_people(self):
        data = {}
        for country in self.session.query(Country).all():
            try:
                data[country.code] = round((int(country.total_notices) * 1_000_000) / int(country.population), 2)
            except TypeError:
                data[country.code] = -1

        data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
        return data

    def notices_percentage_per_country(self):
        data = {}
        for country, notices in self.notice_ordered_per_country().items():
            data[country] = f"{round(int(notices) / int(self.total_notices), 2) * 100} %"
        return data

    def gender_ratio(self, country=None):
        if not country:
            male = self.session.query(Notice.sex).filter(Notice.sex == 'M').count()
            female = self.session.query(Notice.sex).filter(Notice.sex == 'F').count()

        else:
            male = self.session.query(Notice.sex).filter(Notice.sex == 'M', Notice.country == country).count()
            female = self.session.query(Notice.sex).filter(Notice.sex == 'F', Notice.country == country).count()

        total = male + female
        male_ratio = "{} %".format(round((male / total) * 100, 2))
        female_ratio = "{} %".format(round((female / total) * 100, 2))
        return {
            "Male": male_ratio,
            "Female": female_ratio
        }

    @staticmethod
    def calculate_age(birth_date):
        today = datetime.date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age

    def average_age(self, query=None):
        if not query:
            dates = session.query(Notice.date_of_birth).all()
        else:
            dates = [(country.date_of_birth,) for country in query]
        ages = []
        for date in dates:
            if isinstance(date[0], datetime.date):
                ages.append(self.calculate_age(date[0]))
        avg = round(sum(ages) / len(ages))
        return avg

    def average_age_by_gender(self, gender):
        query = self.session.query(Notice.date_of_birth).filter(Notice.sex == gender).all()
        return self.average_age(query)

    def stats_by_country(self, country_code: str):
        country_code = country_code.upper()
        country = self.session.query(Country).filter(Country.code == country_code).first()
        query = self.session.query(Notice).filter(Notice.country == country_code).all()
        average_age = self.average_age(query)
        gender_ratio = self.gender_ratio(country_code)
        per_million_people = self.notice_per_hundred_thousand_people().get(country_code)
        percentage = self.notices_percentage_per_country().get(country.name)
        return {
            "country": country.name,
            "percentage": percentage,
            "total_notices": country.total_notices,
            "average_age": average_age,
            "gender_ratio": gender_ratio,
            "per_million_people": per_million_people,
        }
