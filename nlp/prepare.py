# Preparation

from acquire_codeup_blog import get_blog_articles
import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd


def basic_clean(article):
    '''
    take in a string (article) and return it after applying some basic text cleaning to it:
        - lowercase everything
        - normalize unicode characters
        - replace anything that is not a letter, number, whitespace or a single quote
    '''
    new_article = article.lower()
    new_article = re.sub(r'\s', ' ', new_article)
    normalized = unicodedata.normalize('NFKD', new_article)                .encode('ascii', 'ignore')                .decode('utf-8')
    without_special_chars = re.sub(r'[^\w\s]', ' ', normalized)
    word_list = without_special_chars.split()
    word_list = ' '.join(word_list)
    return word_list


def tokenize(article):
    '''tokenize all the words in the string, article'''
    tokenizer = nltk.tokenize.ToktokTokenizer()
    new_article = tokenizer.tokenize(article, return_str=True)
    return new_article


def print_stop_words(article):
    '''accept some text, apply stemming to all of the words,
        and print a list of value counts for all the stemmed words'''
    # Create the nltk stemmer object, then use it
    ps = nltk.porter.PorterStemmer()
    stems = [ps.stem(word) for word in article.split()]
    print(pd.Series(stems).value_counts())


def stem(article):
    '''accept a string and return it after applying stemming to all the words'''
    ps = nltk.stem.PorterStemmer()
    article_stemmed = ''.join([ps.stem(word) for word in article])
    return article_stemmed


def lemmatize(article):
    '''accept a string and return it after applying lemmatization to each word.'''
    wnl = nltk.stem.WordNetLemmatizer()
    lemmatized_words = [wnl.lemmatize(word) for word in article]
    article_lemmatized = ''.join(lemmatized_words)
    return article_lemmatized


def remove_stopwords(article, extra_words = None, exclude_words = None):
    '''remove all the stopwords, including all the words in extra_words and excluding
    all the words in exclude list'''

    # get basic stopword list
    stopword_list = stopwords.words('english')

    # add extra words    
    if extra_words != None:
        stopword_list = stopword_list + extra_words
    # remove excluded words
    if exclude_words != None:
        stopword_list = [word for word in stopword_list if word not in exclude_words]
    
    without_stopwords = [word for word in article.split(' ') if word not in stopword_list]
    article_without_stopwords = ' '.join(without_stopwords)
    return article_without_stopwords


def prep_article(this_dict, extra_words = None, exclude_words = None):
    '''
    takes in a dictionary representing an article and returns a dictionary that 
    looks like this:
            {
             'title': 'the original title',
             'original': original,
             'stemmed': article_stemmed,
             'lemmatized': article_lemmatized,
             'clean': article_without_stopwords
            }
    Note that if the orignal dictionary has a title property, it will remain unchanged 
    (same goes for the category property).
    '''
    # put the content section into article and make a copy
#     article = articles['content'][article_index]    # needed for 
    article = this_dict['content']
    original = article

    '''
    apply some basic text cleaning to the string, article:
        - lowercase everything
        - normalize unicode characters
        - replace anything that is not a letter, number, whitespace or a single quote
    '''
    article = basic_clean(article)

    '''tokenize all the words in the string, article'''
    article = tokenize(article)

    '''applying stemming to all the words in the string, article'''
    article_stemmed = stem(article)
    
    ''''apply lemmatization to each word in the string, article'''
    article_lemmatized = lemmatize(article)
    
    '''remove all the stopwords, including all the words in extra_words and excluding
    all the words in exclude list'''
    article_without_stopwords = remove_stopwords(article, extra_words, exclude_words)

    keys = list(this_dict.keys())
    
    new_dict = {
         'title': this_dict['title'],
         'original': original,
         'category': [this_dict['category'] if 'category' in keys else 'blog'],
         'stemmed': article_stemmed,
         'lemmatized': article_lemmatized,
         'clean': article_without_stopwords
        }
    return new_dict


def prepare_article_data(articles, extra_words = None, exclude_words = None):
    # takes in the list of articles dictionaries, 
    # applies the prep_article function to each one, 
    # and returns the transformed data.
    transformed_articles = []

    for article_index in range(len(articles)):
        transformed_entry = prep_article(articles[article_index], extra_words, exclude_words)
        transformed_articles.append(transformed_entry.copy())

    return transformed_articles

def prep_news_article(this_dict, extra_words = None, exclude_words = None):
    '''
    takes in a dictionary representing an article and returns a dictionary that 
    looks like this:
            {
             'title': 'the original title',
             'original': original,
             'stemmed': article_stemmed,
             'lemmatized': article_lemmatized,
             'clean': article_without_stopwords
            }
    Note that if the orignal dictionary has a title property, it will remain unchanged 
    (same goes for the category property).
    '''
    # put the content section into article and make a copy
#     article = articles['content'][article_index]    # needed for 
    article = this_dict['content']
    original = article

    '''
    apply some basic text cleaning to the string, article:
        - lowercase everything
        - normalize unicode characters
        - replace anything that is not a letter, number, whitespace or a single quote
    '''
    article = basic_clean(article)

    '''tokenize all the words in the string, article'''
    article = tokenize(article)

    '''applying stemming to all the words in the string, article'''
    article_stemmed = stem(article)
    
    ''''apply lemmatization to each word in the string, article'''
    article_lemmatized = lemmatize(article)
    
    '''remove all the stopwords, including all the words in extra_words and excluding
    all the words in exclude list'''
    article_without_stopwords = remove_stopwords(article, extra_words, exclude_words)

    keys = list(this_dict.keys())
    
    new_dict = {
         'title': this_dict['title'],
         'original': original,
         'category': [this_dict['category'] if 'category' in keys else 'blog'],
         'stemmed': article_stemmed,
         'lemmatized': article_lemmatized,
         'clean': article_without_stopwords
        }
    return new_dict


def prepare_news_article_data(articles, extra_words = None, exclude_words = None):
    # takes in the list of articles dictionaries, 
    # applies the prep_article function to each one, 
    # and returns the transformed data.

    for article_index in range(len(articles)):
        transformed_entry = prep_news_article(articles[article_index], extra_words, exclude_words)
        transformed_articles.append(transformed_entry.copy())

    return transformed_articles

if __name__ == "__main__":
    '''create a list of extra words and another of words to exclude from the stoplist'''
    extra_words = ['codeup']
    exclude_words = ['']

    articles = get_blog_articles()
    transformed_data = prepare_article_data(articles, extra_words, exclude_words)
    print(transformed_data)