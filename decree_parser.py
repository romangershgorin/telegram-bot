import requests
from bs4 import BeautifulSoup
import pandas as pd
import io
from datetime import datetime
from collections import defaultdict
import logging
from typing import Tuple, DefaultDict, List, Union, Sequence
import re


ADMIN_SMOLENSK: str = 'https://www.admin-smolensk.ru/koronavirus/'


def get_decree_dates() -> List[str]:
    '''
    Retreave dates of all decrees
    '''
    page = requests.get(ADMIN_SMOLENSK)

    dates: List[str] = list()
    parsed_html = BeautifulSoup(page.text, 'html.parser')
    for link in parsed_html.find_all('a'):
        if isinstance(link.string, str) and link.string.startswith('Указ Губернатора Смоленской'):
            match = re.search(r"(\d{2}.\d{2}.\d{4})", link.string)
            dates.append(match.group())

    return dates


if __name__ == '__main__':
    print(get_decree_dates())
