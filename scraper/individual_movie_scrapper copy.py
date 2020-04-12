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
import sqlalchemy as db
from sqlalchemy import create_engine
import pandas as pd
import re
import logging

from fuzzywuzzy import fuzz
from fuzzywuzzy import process


engine = create_engine('mysql://scott:tiger@localhost/foo')
mainTable = 'infobox vevent'  # table, class
logging.basicConfig(level=logging.DEBUG)


class Movie:
    id = None
    wikiUrl = None
    title = None
    studio = None
    castCrew = None
    genre = None
    medium = None
    director = None
    producers = []
    writer = []
    writer1 = []
    starring = []
    musicBy = []
    cinematography = None
    editedbBy = None
    productionCo = None
    distributer = None
    screenplay = None
    runningTime = 0  # in minutes
    country = []
    language = []
    boxOffice = 0
    releaseDate = None
    budget = None

    def __str__(self):
        # return self.title, self.director, self.producers, self.writer, self.boxOffice
        return """
        Title: {}
        Director: {}
        Studio: {}
        Genre: {}
        Staring: {}
        Writer: {}
        Language: {}
        Running Time: {}
        Box Office: {}
        Release Date: {}
        Producers: {}
        Screenplay: {}
        Music By: {}
        Cinematography: {}
        Production Co: {}
                """.format(self.title, self.director, self.studio, self.genre, self.starring, self.writer, self.language, self.runningTime, self.boxOffice, self.releaseDate, self.producers, self.screenplay, self.musicBy, self.cinematography, self.productionCo)

    def __repr__(self):
        return self.name


def funct(url):
    movie = Movie()
    f = open("testFile0.html", 'w')

    # initialize BS4
    print("* "*60)
    print("begin requesting page...")
    url = url.split('?', 1)[0]
    page_response = requests.get(url, timeout=10)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    print("Successful page response from: \n{}".format(url))

    # begin parsing content
    # !Main Tables!
    table = page_content.find_all('table', attrs={'class': mainTable})
    x = table[0].find_all('tr')
    for i in x:
        f.write(str(i))
        f.write('~ '*30)

    testDictionary = {}
    testDict = {}
    movieDict = {}
    for i in x:
        y = {i.find('th'): i.find('td')}
        testDictionary.update(y)

    # !Main Function(s)!
    for i in x:
        try:
            th = i .find('th').text
            td = i.find('td').text

            fuzzRating = fuzz.ratio('Starring', th)
            if fuzzRating > 90:
                actorResultSet = i.find_all('a')
                starringList = []
                for i in actorResultSet:
                    starringList.append(i.text)
                y = {'Starring2': starringList}
                movieDict.update(y)
            y = {th: td}
            movieDict.update(y)
        except Exception as ex:
            print(ex)

    for i in x:
        try:
            data = i.find_all('li')
            th = i.find('th').text
            listValues= [i.text for i in data]

            z = {th:listValues}
            # z = {th:data}
            if listValues:
                print("anything")
                movieDict.update(z) 
            print('! '*40)
            print(len(listValues))
            print(type(listValues))
            print(listValues)
            print('! '*40)
        except:
            pass

    print('~ '*30)
    # print('MOVIE DICTIONARY')
    # for i, j in movieDict.items():
    #     print(i, ':', j)
    #     print(type(i))
    #     print(type(j))

    title = page_content.title.text.split('-', 1)[0]
    movie.title = title
    movie.director = movieDict["Directed by"]
    movie.producers = movieDict['Produced by']
    movie.starring = movieDict['Starring2']
    movie.musicBy = movieDict['Music by']
    movie.cinematography = movieDict['Cinematography']
    movie.editedbBy = movieDict['Edited by']
    movie.productionCo = movieDict['Productioncompanies ']
    movie.distributer = movieDict['Distributed by']
    movie.releaseDate = movieDict['Release date']
    movie.country = movieDict['Country']
    movie.country = movieDict['Country']
    movie.runningTime = movieDict['Running time']
    movie.language = movieDict['Language']
    movie.budget = movieDict['Budget']
    movie.boxOffice = movieDict['Box office']
    movie.musicBy = movieDict['Music by']
    try: 
        movie.writer = movieDict['Written by']
    except:
        pass
    try:
        movie.screenplay = movieDict['Screenplay by']
    except:
        pass




    print('! '*30)
    print(movie)
    print('! '*30)

    f.close()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('url', help='yelp bussiness url')
    args = argparser.parse_args()
    url = args.url
    funct(url)
