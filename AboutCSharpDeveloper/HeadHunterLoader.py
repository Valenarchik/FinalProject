import requests
import json
import pandas as pd
from datetime import datetime, date
from multiprocessing import Pool

datetime_format = "%Y-%m-%dT%H:%M:%S"
count_requests = 10


def get(dict_, key):
    try:
        return dict_.get(key)
    except:
        return None


def load_all_data_for_vac(url):
    all_vac = json.loads(get_request_or_exception(url).text)
    skills = list(map(lambda x: x['name'], get(all_vac, 'key_skills')))
    pub_at = datetime.strptime(get(all_vac, 'published_at'), '%Y-%m-%dT%H:%M:%S+%f')
    return {'name': get(all_vac, 'name'),
            'description': get(all_vac, 'description'),
            'skills_are_there': len(skills) > 0,
            'key_skills': skills,
            'employer_name': get(get(all_vac, 'employer'), 'name'),
            'salary_from': get(get(all_vac, 'salary'), 'from'),
            'salary_to': get(get(all_vac, 'salary'), 'to'),
            'salary_currency': get(get(all_vac, 'salary'), 'currency'),
            'area_name': get(get(all_vac, 'area'), 'name'),
            'published_at': pub_at}


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


def load_page(per_page: int, page: int, date_from: datetime,
              date_to: datetime) -> pd.DataFrame:
    if date_from > date_to or date_to > datetime.today():
        raise Exception
    date_from = date_from.strftime(datetime_format)
    date_to = date_to.strftime(datetime_format)
    https = (f"https://api.hh.ru/vacancies?"
             f"specialization=1&"
             f"per_page={per_page}&page={page}&"
             f"date_from={date_from}&date_to={date_to}&"
             f"only_with_salary=true&"
             f"search_field=name&"
             f"text=c%23 OR с%23 OR шарп OR .net OR 'c sharp'")
    response = get_request_or_exception(https)
    items = json.loads(response.text)['items']
    return pd.DataFrame(items)


def load_book(date_from: datetime, date_to: datetime) -> pd.DataFrame:
    data = [(100, page, date_from, date_to) for page in range(20)]
    with Pool(20) as pool:
        frames = pool.starmap(load_page, data)
    return pd.concat(frames, ignore_index=True)


def get_c_sharp_vacs(date: date) -> pd.DataFrame:
    date_from = datetime(date.year, date.month, date.day, 0, 0, 0)
    date_to = datetime(date.year, date.month, date.day, 23, 59, 59)
    df_result = load_page(10, 0, date_from=date_from, date_to=date_to)
    with Pool(10) as pool:
        temp = list(pool.map(load_all_data_for_vac, list(df_result['url'])))
    df_result = pd.DataFrame(temp)
    func = lambda x: __merge_salary(x['salary_from'], x['salary_to'])
    return df_result \
        .assign(salary=df_result.apply(func, axis=1)) \
        .drop(['salary_from', 'salary_to'], axis=1)


def __merge_salary(salary_from, salary_to):
    if pd.isnull(salary_from):
        return int(salary_to)
    if pd.isnull(salary_to):
        return int(salary_from)
    return int((salary_from + salary_to) / 2)
