import requests
from bs4 import BeautifulSoup
import pandas as pd
import io
from datetime import datetime
from collections import defaultdict


FSS_ROOT = 'http://fss.ru'


def get_page_html():
    page = requests.get('http://fss.ru/ru/fund/disabilitylist/501923/503049.shtml')
    return page.text


def get_url_from_html(html):
    parsed_html = BeautifulSoup(html, 'html.parser')
    for link in parsed_html.find_all(href=True):
        if (link.get('href').endswith('.xlsx')):
            return FSS_ROOT + link.get('href')


def get_table(table_url):
    table_data = requests.get(get_url_from_html(get_page_html()))
    file = io.BytesIO(table_data.content)
    return pd.read_excel(file)


def find_district(table):
    for district in table['Unnamed: 2']:
        if isinstance(district, str):
            if district.find('моленск') != -1:
                return True

    return False


def check_district():
    table_url = get_url_from_html(get_page_html())
    table = get_table(table_url)
    return find_district(table)


def parse_datetime(column_data):
    if (isinstance(column_data, datetime)):
        return [str(column_data).split()[0],]
    else:
        return column_data.split()


def get_processed_districts():
    table_url = get_url_from_html(get_page_html())
    table = get_table(table_url)
    to_date_column = table.columns[-1]

    districts_map = defaultdict(str)
    for index in range(1, table.shape[0]):
        if isinstance(table['Unnamed: 2'][index], str):
            to_date = parse_datetime(table[to_date_column][index])
            districts_map[table['Unnamed: 2'][index]] = to_date[-1]
    
    district_index = 1
    districts_info = ''
    for key in districts_map:
        districts_info += '{}. {}: {}\n'.format(district_index, key, districts_map[key])
        district_index += 1
    
    return district_index, districts_info


if __name__ == '__main__':
    print(get_processed_districts())
