'''
This module provides functions for scraping news article data from inshorts.com.
'''
import os
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = 'https://inshorts.com/en/read'
SECTIONS = ['business', 'sports', 'technology', 'entertainment']

def get_all_sections():

    for section in SECTIONS:
        
        # Make a request for the given section and processes all the articles in it
        url = f'{BASE_URL}/{section}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, features='lxml')

        # CREATE A LIST OF DICTIONARIES:
        # Iterating through all of the relevant articles, extract the title and content
        # Also add the category to the dictionary.
        articles = []

        for article in soup.find_all(class_='news-card'):
            this_entry = {
                        'title': article.find(class_='news-card-title').find('a').text.strip(),
                        'content': (article.find(class_='news-card-content')
                                    .find('div', attrs={'itemprop': 'articleBody'})
                                    .text.strip()),
                        'category': section
                        }
            articles.append(this_entry)
    return articles


def get_news_articles(use_cache=True):
    if use_cache and os.path.exists('news_articles.json'):
        articles = json.load(open('news_articles.json'))
    else:
        articles = get_all_sections()
        json.dump(articles, open('news_articles.json', 'w'))
    return articles

def get_news_data():
    '''
    Returns all the articles from all the sections as a pandas DataFrame
    '''
    return pd.DataFrame(get_all_sections())


articles = get_news_data()
articles