import pandas as pd
import logging
import numpy as np
from data_imports import *


def compare_kanton(df_wikidata, df_api):
    """
    This functions checks all entries from ZH Kanton Data and compares it with the wikidata
    :param df_wikidata:
    :param df_statdata:
    :return: list of index in df_statdata not in df_wikidata --> need to be uploaded to wikidata
    """
    logging.info('Compare: {0} stat_entries with {1} wikidate_entries'.format(df_api['date'].count,
                                                                              df_wikidata['date'].count))

    # add column 'check'
    df_api['check'] = df_api['date'].astype(str) + '---' + df_api['BFS_NR'].astype(str)
    df_wikidata['check'] = df_wikidata['date'].astype(str) + '---' + df_wikidata['bfs_id'].astype(str)
    
    print("NOT IN THE DATASET")
    print(df_api[(df_api['check'].isin(df_wikidata['check']) == False)]['date'].astype(str).str[:4].unique())
    #return df_api[(df_api['check'].isin(df_wikidata['check']) == False)].index.tolist()


def compare_stadt(df_wikidata, df_api):
    """
    This functions checks all entries from ZH Kanton Data and compares it with the wikidata
    :param df_wikidata:
    :param df_statdata:
    :return: list of index in df_statdata not in df_wikidata --> need to be uploaded to wikidata
    """
    logging.info('Compare: {0} stat_entries with {1} wikidate_entries'.format(df_api['date'].count,
                                                                              df_wikidata['date'].count))

    # add column 'check'
    df_api['check'] = df_api['date'].astype(str) + '---' + df_api['wikidata_id'].astype(str)
    df_wikidata['check'] = df_wikidata['date'].astype(str) + '---' + df_wikidata['wikidata_id'].astype(str)
    
    print("NOT IN THE DATASET")
    print(df_api[(df_api['check'].isin(df_wikidata['check']) == False)]['date'].astype(str).str[:4].unique())
    #return df_api[(df_api['check'].isin(df_wikidata['check']) == False)].index.tolist()

def main():
    
    kantonZH_api = import_kantonZH_api()
    stadtZH_api = import_stadtZH_api()
    
    swisstopowikidata = import_swisstopowikidata_kantonZH()
    wikidata_kantonZH = import_wikidata_kantonZH()
    wikidata_stadtZH = import_wikidata_stadtZH()
    
    kantonZHapiANDswisstopowikidata = pd.merge(kantonZH_api, swisstopowikidata, how='left', left_on=['BFS_NR'], right_on=['bfs']).dropna()
    
    print("kantonZHapiANDswisstopowikidata.head(")
    print(kantonZHapiANDswisstopowikidata.head())
    
    print("compare_kanton(wikidata_kantonZH, kantonZHapiANDswisstopowikidata)")
    print(compare_kanton(wikidata_kantonZH, kantonZHapiANDswisstopowikidata))

    print("compare_stadt(wikidata_stadtZH, stadtZH_api)")
    print(compare_stadt(wikidata_stadtZH, stadtZH_api))

if __name__ == "__main__":
    main()
