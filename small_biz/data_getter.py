# -*- coding: utf-8 -*-
'''
Created on Monday, 30th March 2020 7:36:30 pm
===============================================================================
@filename:  data_getter.py
@author:    Manuel Martinez (manmart@nber.org)
@project:   covid 19 - small business survey
@purpose:   general purpose code for getting data from qualtrics api
===============================================================================
'''
import io
import os

import pandas as pd
import requests


def get_surv_data(surv_name: str) -> pd.DataFrame:
    '''
    export current data for a specific survey id into a pandas dataframe

    Args:
        surv_id (str): survey id

    Returns:
        pd.DataFrame: survey responses
    '''
    surv_ids = {'latam': 'SV_d6ZulWfxVdP6brf',
                'us': 'SV_5pOfQn2X4uYUZpz',
                'us-invite': 'SV_6lYENZ8l1DQTu4d'}

    if surv_name not in surv_ids:
        raise KeyError(f'surv_name must be in {set(surv_ids.keys())}')

    # set up values
    api_key = os.environ['QUAL_APIKEY']
    prog_check = 0.0
    prog_status = 'inProgress'
    url = ('https://princetonsurvey.az1.qualtrics.com/API/v3/surveys/{}/'
           'export-responses/'.format(surv_ids[surv_name]))
    headers = {'content-type': 'application/json',
               'x-api-token': api_key}
    data_kwds = {'format': 'csv',
                 'useLabels': True}
    ready = None

    # start up download from server
    dl_req = requests.post(url=url,
                           headers=headers,
                           json=data_kwds)

    prog_id = dl_req.json()['result']['progressId']
    prog_status = dl_req.json()['result']['status']

    # check on progress
    while prog_status != 'complete' and \
            prog_status != 'failed' and \
            ready is None:
        req_check_url = url + prog_id
        req_check_resp = requests.get(url=req_check_url,
                                      headers=headers)
        req_check_prog = req_check_resp.json()['result']['percentComplete']

        if ready is None:
            print(f'Progress = {req_check_prog:.2f}')

        try:
            ready = req_check_resp.json()['result']['fileId']
        except KeyError:
            pass

        prog_status = req_check_resp.json()['result']['status']
        if prog_status == 'complete':
            print(f'Progress = {req_check_prog:.2f}')

    # check for errors
    if prog_status == 'failed':
        raise Exception('export failed')

    file_id = req_check_resp.json()['result']['fileId']

    # download file
    req_dl_url = url + file_id + '/file'
    req_dl = requests.get(url=req_dl_url,
                          headers=headers,
                          stream=True)

    # extract from zip into pandas dataframe
    df = pd.read_csv(io.BytesIO(req_dl.content), compression='zip')

    # drop qualtric headers
    df = df.iloc[2:, :].copy()
    df.reset_index(inplace=True, drop=True)

    # lowercase cols
    df.columns = df.columns.str.lower()

    return df


if __name__ == '__main__':
    df = get_surv_data(surv_name='us')
