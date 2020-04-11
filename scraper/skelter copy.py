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

import socket 

businessName = "lemon--h1__373c0__2ZHSL heading--h1__373c0__1VUMO heading--no-spacing__373c0__1PzQP heading--inline__373c0__1F-Z6" # h1, class

# logging.basicConfig(level=logging.DEBUG)

class Business:
    def __init__(self):
        self.id = None
        self.url = None
        self.name = None 
        self.avgRating = None 
        self.numReviews = None 
        self.phone = None 
        self.address = None
        self.website = None 
        self.categories = None
        self.amenities = None
        self.reviews = []
        self.reviewCount = 0
        
    def allReviews(self):
        print("All Reviews_")
        return "All Reviews"
    
    def __str__(self):
        return "ID: {},\nURL: {}, \nName: {},\nAddress: {},\nNumber of Reviews: {}, \nAverage Rating: {}, \nPhone: {}, \nWebsite: {}, \nCategories: {}, \nAmenities: {}, \nReviews: {}".format(self.id, self.url, self.name, self.address, self.numReviews, self.avgRating, self.phone, self.website, self.categories, self.amenities, len(self.reviews))
    def __repr__(self):
        print("TODO")
        return "something?"

class Review:
    def __int__(self):
        self.user = None
        self.location = None 
        self.comment = None 
        self.rating = None 
        self.datePosted = None
    
    def __str__(self):
        return "\nUser: {}, \nCity: {}, \nDate: {}, \nRating: {}, \nComment:{}".format(self.user, self.location, self.datePosted, self.rating, self.comment)
        # print(self.user, self.location, self.datePosted, self.rating, self.comment)

    def __repr__(self):
        # print(self.user, self.location, self.datePosted, self.rating, self.comment)
        print("\nUser: {}, \nCity: {}, \nDate: {}, \nRating: {}, \nComment:{}".format(self.user, self.location, self.datePosted, self.rating, self.comment))

def funct(url):
    bizObject = Business ()

    # initialize BS4
    print("begin requesting page...")
    baseUrl = url.split('?', 1)[0]
    url = baseUrl
    page_response = requests.get(url, timeout=10)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    print("Successful page response from: {}\n".format(url))
    # !ID!
    # generate ID
    id = random.randint(1, 10000) 

    # begin grabbing content, 1st page
    title = page_content.find('h1', attrs={"class": businessName}).text

    # !Address! 
    addressblock = page_content.find('div', attrs={"class": addressBlockClass})
    addresses = addressblock.find_all('span', attrs={"class": addressClass})
    address = ""
    for i in addresses:
        address = address + i.text + "$ "
    
    numberOfReviews = page_content.find('p', attrs={"class": numOfRatings}).text
    numReviews = [int(i) for i in numberOfReviews.split() if i.isdigit()][0]

    # !Average Rating!
    # # TODO  clean this function
    # # find outter class, then REGEX/SOUP out the aria-labelb 
    # try: 
    #     avg = page_content.find('div', attrs={"class": avgRating1})["aria-label"]
    #     avgRate = [int(i) for i in avg.split() if i.isdigit()][0]
    #     print("Average Rating 1 found.")
    #     # logging.debug('AVG Rating Class 1 Found')
    # except Exception as ex:
    #     print('Error:',  ex)
    #     # logging.error('Error:', ex)
    # try:
    #     avgRate = page_content.find('div', attrs={"class": avgRating2})["aria-label"]
    #     # logging.debug('AVG Rating Class 2 Found')
    #     print("Average Rating 2 found.")
    # except Exception as ex:
    #     print('Error:',  ex)
    #     # logging.error('Error:', ex)
    # try:
    #     avg = page_content.find('div', attrs={"class": avgRating3})["aria-label"]
    #     avgRate = [int(i) for i in avg.split() if i.isdigit()][0]
    #     # logging.debug('AVG Rating Class 1 Found')
    #     print("Average Rating 3 found.")
    #     # logging.debug('AVG Rating Class 2 Found')
    # except Exception as ex:
    #     print('Error:',  ex)
    # try:
    #     avg = page_content.find('div', attrs={"class": avgRating4})["aria-label"]
    #     avgRate = [int(i) for i in avg.split() if i.isdigit()][0]
    #     # logging.debug('AVG Rating Class 1 Found')
    #     if avg:
    #         print("Average Rating 4 found.")
    # except Exception as ex:
    #     print('Error:',  ex)
    # try:
    #     avg = page_content.find('div', attrs={"class": avgRating5})["aria-label"]
    #     avgRate = [int(i) for i in avg.split() if i.isdigit()][0]
    #     # logging.debug('AVG Rating Class 1 Found')
    #     if avg:
    #         print("Average Rating 4 found.")
    # except Exception as ex:
    avgRate = None
    #     # logging.error('Error:', ex)

    # !Phone! 
    webPhoneDirBlock= page_content.find('div', attrs={"class": webPhoneDirBlockClass})
    phoneWWW = webPhoneDirBlock.find_all('p', attrs={"class": phoneNum0}) 
    phone = re.search(phoneRegex, str(phoneWWW)).group(0)
    try:
        www = webPhoneDirBlock.find('a', attrs={"role": "link"}).text
    except Exception as asdf:
        print('www Error:', asdf)
        www = None

    # !Amenities!
    amenitiesBlock = page_content.find('div', attrs={"class": amenitiesBlockClass})
    amenitiesDictionary = amenitiesBlock.find_all('div', attrs={"class": amenitiesDictionaryClass})
    amenities = {}
    for i in amenitiesDictionary:
        temp = i.findAll('span')
        amenities.update( {temp[0].text:temp[1].text.replace(u'\xa0', u' ')}) 
    
    # !Categories!
    categories = {}
    categoryBlock = page_content.find('div', attrs={"class": categoriesBlockClass})

    
    # !Comments!
    mainBlocks = page_content.findAll('div', attrs={"class": mainBlockClass}) # find all review blocks
    for i in mainBlocks:
        review = Review()
        try:
            userName = i.find('span', attrs={"class": userClass}).text # user name 
            review.user = userName
        except Exception as ex:
            pass
            # print("userClass 1 not found.")
        try:
            userName = i.find('a', attrs={"class": userClass1}).text # user name 
            review.user = userName
        except Exception as ex:
            pass
            # print("UserClass 2 not found")

        review.comment = i.find('p', attrs={"class": commentClass}).text # comment
        review.location = i.find('span', attrs={"class": userCityClass}).text #user city

        ratingDateBlock = i.find('div', attrs={"class": ratingDateClass})
        for j in ratingDateBlock:
            try:
                review.datePosted = j.find('span', attrs={"class": ratingDateClass0}).text
            except:
                pass
            try:
                rating = j.find('div', attrs={"role": "img"})["aria-label"]
                review.rating = [int(i) for i in rating.split() if i.isdigit()][0]
            except:
                pass
        bizObject.reviews.append(review)

    bizObject.id = id
    bizObject.url = baseUrl 
    bizObject.name = title
    bizObject.address = address
    bizObject.numReviews = numReviews
    bizObject.avgRating = avgRate
    bizObject.phone = phone
    bizObject.website = www
    bizObject.amenities = amenities
    # TODO: add amenities to object
    print("#"*30)
    print("Begin pagination")

    p = 20
    while True:
        pageCount = p/20 + 1
        newUrl = (url + "?start={}".format(p))
        print("!~!~"*20)
        print("\n\n\n\nTry Scraping:\n{}".format(newUrl))
        print(pageCount)
        
        try:
            page_response = requests.get(newUrl, timeout=5)
            page_content = BeautifulSoup(page_response.content, "html.parser")
            print("\nSuccessful page_response")

            mainBlocks = page_content.findAll('div', attrs={"class": mainBlockClass})
            print(type(mainBlocks))
            print("!~!~"*20)
            p += 20
            if mainBlocks:
                for i in mainBlocks:
                    review = Review()
                    try:
                        userName = i.find('span', attrs={"class": userClass}).text # user name 
                        review.user = userName
                    except Exception as ex:
                        # print("userClass 1 not found.")
                        pass
                    try:
                        userName = i.find('a', attrs={"class": userClass1}).text # user name 
                        review.user = userName
                    except Exception as ex:
                        # print("UserClass 2 not found")
                        pass

                    review.comment = i.find('p', attrs={"class": commentClass}).text # comment
                    review.location = i.find('span', attrs={"class": userCityClass}).text #user city

                    ratingDateBlock = i.find('div', attrs={"class": ratingDateClass})
                    for j in ratingDateBlock:
                        try:
                            review.datePosted = j.find('span', attrs={"class": ratingDateClass0}).text
                        except:
                            pass
                        try:
                            rating = j.find('div', attrs={"role": "img"})["aria-label"]
                            review.rating = [int(i) for i in rating.split() if i.isdigit()][0]
                        except:
                            pass
                    bizObject.reviews.append(review)
            else:
                break
        except: 
            print("!"*30)

    bizObject.reviewCount = len(bizObject.reviews)
    print("-"*20)

    for x in bizObject.reviews:
        print(x)
    print(bizObject)
    print("-"*20)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('url', help='yelp bussiness url')
    args = argparser.parse_args()
    url = args.url
    funct(url)