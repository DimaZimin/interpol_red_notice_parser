import requests
import itertools
import collections
from bs4 import BeautifulSoup


URL_NOTICE = "https://ws-public.interpol.int/notices/v1/red?resultPerPage=20&page=2"
URL_NOTICE_BY_COUNTRY = "https://ws-public.interpol.int/notices/v1/red?nationality=RO&resultPerPage=20&page=2"


class SiteParser:

    SITE_URL = "https://www.interpol.int/en/How-we-work/Notices/View-Red-Notices"

    def __init__(self):
        self.markup = requests.request("GET", url=self.SITE_URL).text
        self.soup = BeautifulSoup(self.markup, 'html.parser')
        self.__countries_select = list(filter(lambda x: x.get('value') is not None, self.soup.find_all('option')))

    def countries_dict(self):
        return {country.text: country['value'] for country in self.__countries_select}


class RedNoticeParser:

    API_SOURCE = "https://ws-public.interpol.int/notices/v1/red"

    def __init__(self, per_page: int = 20, page: int = 1):
        self.result_per_page = per_page
        self.page = page
        self.source = f"{self.API_SOURCE}?resultPerPage={self.result_per_page}&page={self.page}"

    def get_full_data(self):
        response = requests.request("GET", self.source)
        return response.json()

    def get_total(self):
        return self.get_full_data().get("total")

    def _get_query_info(self):
        return self.get_full_data().get("query")

    def _get_embedded(self):
        return self.get_full_data().get("_embedded")

    def _get_notices(self):
        return self._get_embedded().get("notices")

    def notices(self):
        return self._get_notices()

    def nationalities(self):

        collection = [
            item.get("nationalities") for item in self.notices() if item.get("nationalities")
        ]

        flatten = itertools.chain(*collection)
        distinct = list(set(list(flatten)))
        return sorted(distinct)

    def nationalities_counter(self):
        counter = collections.Counter(self.nationalities())
        return counter

    def nationality_total(self, nationality):
        source = f"{self.API_SOURCE}?nationality={nationality}"
        response = requests.request("GET", source)
        return response.json().get("total")
