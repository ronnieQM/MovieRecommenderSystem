# from flask import Flask, request, Response
from bs4 import BeautifulSoup
import requests
import argparse
import sys
import os
import types
import csv
from random import choice
import json
import uuid
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

import re
import logging

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from sqlalchemy import *


logging.basicConfig(level=logging.DEBUG)

meta = MetaData()
engine = create_engine('sqlite:///foo.db', echo=True)
meta.bind = engine

Session = sessionmaker(bind=engine)

Base = declarative_base(metadata=meta)


class Film(Base):
    __tablename__ = 'film'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    wikiUrl = Column(String)
    studio = Column(String)
    castCrew = Column(String)
    genre = Column(String)
    medium = Column(String)
    director = Column(String)
    producers = Column(String)
    writer = Column(String)
    writer1 = Column(String)
    starring = Column(String)
    musicBy = Column(String)
    cinematography = Column(String)
    editedbBy = Column(String)
    productionCo = Column(String)
    distributer = Column(String)
    screenplay = Column(String)
    runningTime = Column(String)
    country = Column(String)
    language = Column(String)
    boxOffice = Column(String)
    releaseDate = Column(String)
    budget = Column(String)
    rating = Column(String)

    def __repr__(self):
        return "<Film(tile='{}', releaseYear='{}')>".format(self.name, self.releaseDate)

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    fname = Column(String, unique=True)
    lname = Column(String, unique=True)

class ProductionCo(Base):
    __tablename__ = 'production_co'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

Base.metadata.create_all()


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
    Session = sessionmaker()
    session = Session()
    mainTable = 'infobox vevent'  # table, class
    f = open("testFile0.html", 'w')
    movie = Movie()

    # initialize BS4
    print("* "*60)
    print("begin requesting page...")
    url = url.split('?', 1)[0]
    page_response = requests.get(url, timeout=10)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    print("Successful page response from: \n{}".format(url))

    # !Main Tables!
    table = page_content.find_all('table', attrs={'class': mainTable})
    x = table[0].find_all('tr')
    for i in x:
        f.write(str(i))
        f.write('~ '*30)

    movieDict = {}

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
            listValues = [i.text for i in data]

            z = {th: listValues}
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
    print('MOVIE DICTIONARY')
    for i, j in movieDict.items():
        print(i, ':', j)
        print(type(i))
        print(type(j))

    title = page_content.title.text.split('-', 1)[0]
    movie.title = title
    director = movieDict["Directed by"]
    producers = movieDict['Produced by']
    starring = movieDict['Starring2']
    cinematography = movieDict['Cinematography']
    editedbBy = movieDict['Edited by']
    try: 
        productionCo = movieDict['Productioncompanies ']
    except:
        pass
    try:
        productionCo = movieDict['Productioncompany']
    except:
        pass
    distributer = movieDict['Distributed by']
    releaseDate = movieDict['Release date']
    country = movieDict['Country']
    country = movieDict['Country']
    runningTime = movieDict['Running time']
    language = movieDict['Language']
    budget = movieDict['Budget']
    boxOffice = movieDict['Box office']
    musicBy = movieDict['Music by']
    try:
        movie.writer = movieDict['Written by']
    except:
        pass
    try:
        movie.screenplay = movieDict['Screenplay by']
    except:
        pass
    movie.title = title
    movie.director = movieDict["Directed by"]
    movie.producers = movieDict['Produced by']
    movie.starring = movieDict['Starring2']
    movie.musicBy = movieDict['Music by']
    movie.cinematography = movieDict['Cinematography']
    movie.editedbBy = movieDict['Edited by']
    try: 
        movie.productionCo = movieDict['Productioncompanies ']
    except: 
        pass
    try: 
        movie.productionCo = movieDict['Productioncompany']
    except: 
        pass
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

    newFilm = Film(title=title, director=director,
                   language=language, runningTime=runningTime,
                   
                   )
                   
    session.add(newFilm)
    session.commit()

def allMovies():
    filmList = []
    with open('urls.txt', 'r') as filehandle:
        for i in filehandle:
            i = line[:-1]
            filmList.append(i)
    print('!'*40)
    print(filmList)
    print('!'*40)
    
if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('url', help='yelp bussiness url')
    args = argparser.parse_args()
    url = args.url
    funct(url)

    
    

