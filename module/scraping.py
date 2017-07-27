#!/usr/bin/env python3.6

import requests
from bs4 import BeautifulSoup

def insultron():
    page = requests.get("http://insultron.fr/")
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup.find_all('p')[0].get_text()
