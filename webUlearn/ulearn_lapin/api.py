import re
import requests

class HH_Api:

    def __init__(self, search_text: str):
        self.text = search_text

    def __get_full_vacancies__(self, date: str, count_vac: int) -> list:
        url = 'https://api.hh.ru/vacancies'
        return requests.get(url, dict(text=self.text,
                                      specialization=1,
                                      date_from=f"{date}T00:00:00",
                                      date_to=f"{date}T23:00:00",
                                      per_page=count_vac,
                                      page=1)).json()["items"]

    def get_data_vacancies(self, date: str, count_vac: int):
        data = self.__get_full_vacancies__(date, count_vac)
        result_list = []
        for vac in data:
            url_vac = f'https://api.hh.ru/vacancies/{vac["id"]}'
            resp = requests.get(url_vac).json()
            if resp['salary']:
                description = ' '.join(re.sub(re.compile('<.*?>'), '', resp['description'])
                                       .strip()
                                       .split())
                description = description[:100] + '...' if len(description) >= 100 else description
                result_list.append({'name': resp['name'],
                                    'description': description,
                                    'key_skills': ', '.join(map(lambda x: x['name'], resp['key_skills'])),
                                    'employer': resp['employer']['name'],
                                    'salary': f"{resp['salary']['from'] or ''} - {resp['salary']['to'] or ''} {resp['salary']['currency']}",
                                    'area': resp['area']['name'],
                                    'published_at': resp['published_at'][:10],
                                    'alternate_url': resp['alternate_url']})

        return result_list