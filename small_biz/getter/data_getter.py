# -*- coding: utf-8 -*-
"""
Created on Monday, 30th March 2020 7:36:30 pm
===============================================================================
@filename:  data_getter.py
@author:    Manuel Martinez (manmart@nber.org)
@project:   covid 19 - small business survey
@purpose:   general purpose code for getting data from qualtrics api
===============================================================================
"""
import os

import requests


class DataGetter:
    def __init__(self):
        self.api_key = os.environ['QUAL_APIKEY']
        self.prog_check = 0.0
        self.prog_status = 'in progress'
        self.url = \
            ('https://princetonsurvey.az1.qualtrics.com/API/v3/surveys/{}/'
             'export-responses/')
        self.headers = {'content-type': 'application/json',
                        'x-api-token': self.api_key}


if __name__ == "__main__":
    dg = DataGetter()
