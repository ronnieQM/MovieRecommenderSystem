# from flask import Flask, request, Response
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

import re
import logging

allTablesDiv = 'wikitable sortable jquery-tablesorter' # table, class
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

    # initialize BS4
    print("* "*60)
    print("begin requesting page...")
    url = url.split('?', 1)[0]
    page_response = requests.get(url, timeout=10)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    print("Successful page response from: \n{}".format(url))

    # !ID!
    # generate ID
    id = random.randint(1, 10000) 

    # begin parsing content
    # !All Tables! 
    tables = page_content.find_all('table')
    # tables = page_content.find_all('tbody')
    # z = 0
    # for i in tables:
    #     i.find('tr')
    #     print(i)
    #     z = z + 1
    #     print(z)
    print(tables)


    print("! "*20)
    print("! "*20)
    # !! 

    movie.title = ""
    movie.url = ""
    movie.title = ""
    movie.studio = ""
    movie.castCrew = ""
    movie.genre = ""
    movie.medium = ""
    print(movie)
    print("* "*60)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('url', help='yelp bussiness url')
    args = argparser.parse_args()
    url = args.url
    funct(url)