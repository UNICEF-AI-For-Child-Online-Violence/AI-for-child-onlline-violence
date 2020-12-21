import pandas as pd
import browserhistory as bh  # Used to extract Browsing History
# Uses Google's safe browsing API to test if websites are safe
from pysafebrowsing import SafeBrowsing
import csv
import libs.Constants
import libs.mongodb

API_KEY = libs.Constants.GC_API_KEY


def get_history():
    '''
    Gets all Browsing History from a Local Computer and inputs
    into a pandas array for analysis.

    :param sites: Accepts a list of sites from a pandas array
    :return: A pandas array of sites from Browsing History   
    '''
    dict_obj = bh.get_browserhistory()['chrome']
    # So for now, we would only need the first in the array
    # bh.write_browserhistory_csv()  # Writes history to a csv

    urls = list(zip(*dict_obj))[0]  # Zipping tuples then unpacking for urls
    # Quick User Identifier
    user = bh.get_username()
    return urls, user


def check_site(sites):  # input websites
    '''
    Uses Google's Safe Browsing API to test if sites are safe
    A flag is raised if a site is malicious or inaproppriate for children

    :param sites: Accepts a list of sites from a pandas array
    :return: A flag is raised if a site is malicious and added to the pandas array       
    '''
    s = SafeBrowsing(API_KEY)
    r = s.lookup_urls(sites)

    return r


def get_browser_results():
    urls, user = get_history()

    for url in urls:
        if url[0] != 'h':
            continue
        dict = {
            "user": user,
            "url": url,
            "malware_result": check_site([url])
        }
        # @TODO: If !is_inserted no db connection, must exit
        # print(r["Inserted"])
        r = libs.mongodb.browser_responses.insert(dict, check_keys=False)

    return urls


get_browser_results()
