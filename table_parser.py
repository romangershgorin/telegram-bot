import requests
from bs4 import BeautifulSoup
import pandas as pd
import io
from datetime import datetime
from collections import defaultdict
import logging
from typing import Tuple, DefaultDict, List, Union, Sequence


FSS_ROOT: str = 'http://fss.ru'
FSS_TABLE_PAGE: str = 'http://fss.ru/ru/fund/disabilitylist/501923/503049.shtml'


def get_page_html() -> str:
    page = requests.get(FSS_TABLE_PAGE)
    return page.text


def get_url_from_html(html: str) -> str:
    '''
    Retrieve href url from html page.
    Throw FileExistsError otherwise.
    '''
    parsed_html = BeautifulSoup(html, 'html.parser')
    for link in parsed_html.find_all(href=True):
        if (link.get('href').endswith('.xlsx')):
            return FSS_ROOT + link.get('href')
    
    raise FileExistsError('Table href is missing on the page')


def get_table(table_url):
    '''
    Download excel page from fss site.
    Throw FileExistsError otherwise.
    '''
    url = get_url_from_html(get_page_html())
    logging.info('Found table url: {}'.format(url))
    table_data = requests.get(url)
    file = io.BytesIO(table_data.content)
    return pd.read_excel(file)


def parse_datetime(column_data) -> List[str]:
    '''
    Table contains two kinds of date data.
    1. Simple date with time
    2. Several dates
    Function eather splits dates into separate strings or 
    creates list with single date without time and returns it
    '''
    if (isinstance(column_data, datetime)):
        return [str(column_data).split()[0],]
    else:
        return column_data.split()


def get_processed_districts() -> Union[Tuple[int, str], None]:
    try:
        table_url = get_url_from_html(get_page_html())
        table = get_table(table_url)
        to_date_column = table.columns[-1]

        districts_map: DefaultDict[str, str] = defaultdict(str)
        for index in range(1, table.shape[0]):
            if isinstance(table['Unnamed: 2'][index], str):
                to_date: List[str] = parse_datetime(table[to_date_column][index])
                districts_map[table['Unnamed: 2'][index]] = to_date[-1]
        
        district_index: int = 1
        districts_info: str = ''
        for key in districts_map:
            districts_info += '{}. {}: {}\n'.format(district_index, key, districts_map[key])
            district_index += 1
        
        return district_index, districts_info

    except Exception as error:
        logging.error('Caught error {}'.format(repr(error)))
        return None


if __name__ == '__main__':
    print(get_processed_districts())
