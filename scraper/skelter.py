# from flask import Flask, request, Response
import logging
import re
from bs4 import BeautifulSoup
import requests
import argparse
import sys
import json
import os
import uuid
import types
import csv
from random import choice
import json
import uuid
import random
import sqlalchemy as db
from sqlalchemy import create_engine
import pandas as pd
engine = create_engine('mysql://scott:tiger@localhost/foo')


regex = '.*'
allTablesDiv = 'wikitable sortable jquery-tablesorter'  # table, class
wiki = 'https://en.wikipedia.org'
logging.basicConfig(level=logging.DEBUG)


class Movie:
    id = None
    url = None
    title = None
    studio = None
    castCrew = None
    genre = None
    medium = None

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.name


def funct(url):
    movie = Movie()
    f = open("testFile.html", 'w')

    # initialize BS4
    print("* "*60)
    print("begin requesting page...")
    url = url.split('?', 1)[0]
    page_response = requests.get(url, timeout=10)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    print("Successful page response from: \n{}".format(url))

    # begin parsing content
    # !All Tables!
    tables = page_content.find_all(
        'table', attrs={'class': 'wikitable sortable'})
    pd_tables = []
    tables_list = []
    all_trs1 = []
    for i in tables:
        tables_list.append(i.find_all('tr'))
        f.write(i.prettify())
        f.write('~ '*30)

    for i in tables_list:
        for j in i:
            all_trs1.append(j)

    print('~ '*30)
    print("TABLES:")
    print(type(tables))
    print(len(tables))
    print("\nTable List:")
    print(type(tables_list))
    print(len(tables_list))
    print("\nALL TRs1:")
    print(type(all_trs1))
    print(type(all_trs1[0]))
    print(len(all_trs1))
    f.close()

    for i in range(0, 5):
        print('-'*50)
        print(all_trs1[i])

    movieResultSet = []
    movieLinks = []

    anything = re.compile(".*")
    for i in all_trs1:
        y = i.find('a', attrs={'title': anything})
        movieResultSet.append(y)

    for i in movieResultSet:
        try:
            x = i.get('href')
            url = wiki + x
            movieLinks.append(url)
        except:
            pass

    print('\n')
    print('- '*30)
    print(len(movieLinks))
    print(movieLinks[53])
    print(len(movieResultSet))
    print(type(movieResultSet[1]))
    print(movieResultSet[1])
    with open('urls.txt', 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(movieLinks)

    with open('urls.txt', 'w') as filehandle:
        for i in movieLinks:
            filehandle.write('{}\n'.format(i))

    print('- '*30)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('url', help='yelp bussiness url')
    args = argparser.parse_args()
    url = args.url
    funct(url)
