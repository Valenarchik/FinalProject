import requests
import json
import pandas as pd
from datetime import datetime
from multiprocessing import Pool

datetime_format = "%Y-%m-%dT%H:%M:%S"
count_requests = 10


def load_all_data_for_vac(url):
    all_vac = json.loads(get_request_or_exception(url).text)
    return {'name': get(all_vac, 'name'),
            'description': get(all_vac, 'description'),
            'key_skills': list(map(lambda x: x['name'], get(all_vac, 'key_skills'))),
            'salary_from': get(get(all_vac, 'salary'), 'from'),
            'salary_to': get(get(all_vac, 'salary'), 'to'),
            'salary_currency': get(get(all_vac, 'salary'), 'currency'),
            'area_name': get(get(all_vac, 'area'), 'name'),
            'published_at': get(all_vac, 'published_at')}


def get(dict_, key):
    try:
        return dict_.get(key)
    except:
        return None


def get_request_or_exception(https_requests: str):
    response = None
    for i in range(count_requests):
        temp = requests.get(https_requests)
        if temp.status_code == 403:
            print(temp.text)
            raise Exception
        if temp.status_code == 200:
            response = temp
            break
    if response is None:
        raise Exception
    return response


def get_it_vacancies_from_hh_in_data_range_in_page(per_page: int, page: int, date_from: datetime,
                                                   date_to: datetime) -> pd.DataFrame:
    if date_from > date_to or date_to > datetime.today():
        raise Exception
    date_from = date_from.strftime(datetime_format)
    date_to = date_to.strftime(datetime_format)
    https = (f"https://api.hh.ru/vacancies?"
             f"specialization=1&"
             f"per_page={per_page}&page={page}&"
             f"date_from={date_from}&date_to={date_to}&"
             f"only_with_salary=true")
    response = get_request_or_exception(https)
    items = json.loads(response.text)['items']
    with Pool(24) as pool:
        result = list(pool.map(load_all_data_for_vac, list(map(lambda vac: get(vac, 'url'), items))))
    return pd.DataFrame(result)


def get_it_vacancies_from_hh_in_data_range(date_from: datetime, date_to: datetime) -> pd.DataFrame:
    for page in range(20):
        frame = get_it_vacancies_from_hh_in_data_range_in_page(100, page, date_from, date_to)
        yield frame
        if frame.shape[0] < 100:
            return


def get_c_sharp_vacs(year: int, month: int, day: int):
    searchfor = ['c#', 'c sharp', 'шарп', '.net', 'с#']
    searchfor = ' or '.join([f"name.str.contains('{item}', case=False, regex=False)" for item in searchfor])
    result = []
    i = 0
    for df in get_it_vacancies_from_hh_in_data_range(date_from=datetime(year, month, day, 0, 0, 0),
                                                     date_to=datetime(year, month, day, 23, 59, 59)):
        df = df.query(searchfor, engine='python')
        result.append(df)
        i += df.shape[0]
        if i > 10: break
    return pd.concat(result, ignore_index=True).head(10).to_dict()

