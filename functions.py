import pandas as pd
import networkx as nx

from constants import *

def getPopulationData(countryname):
    return COUNTRY_POPULATION[countryname]
def getNumberOfMEPs(countryname, pre_brexit = True):
    if pre_brexit:
        return NO_EP_SEATS_PRE_BREXIT[countryname]
    else:
        return NO_EP_SEATS_POST_BREXIT[countryname]
def getNumberOfMEPs_by_epgroup(epgroupname, pre_brexit = True):
    if pre_brexit:
        return EP_GROUP_NO_SEATS_PRE_BREXIT[epgroupname]
    else:
        return EP_GROUP_NO_SEATS_POST_BREXIT[epgroupname]
    
def createNxGraph():
    # we use MEPName instead of OfficialMEPID
    G = nx.from_pandas_edgelist(ENTIRE_DATASET, source='AmendmentID', target='MEPName')
    return G

def listMEPs():
    return MEPLIST["person_name"]

def listPoliticalGroups():
    o = pd.unique(ENTIRE_DATASET['EPGroup'])
    return o


# TODO: extend function to use the "start_date" and "end_date" that's now available for the MEP polgroup membership in `epgroup_memberships_9th_term.csv`
def listMEPs_by_polgroup(polgroup):
    o = pd.unique(ENTIRE_DATASET.loc[ENTIRE_DATASET['EPGroup'] == polgroup]['MEPName'])
    return o

def listMEPs_by_country(country):
    o = MEPLIST.loc[MEPLIST['country'] == country]['person_name']
    return o

def graphInfo(G):
    print(f"Some information about this graph:\n"
        f"Number of nodes: {nx.number_of_nodes(G)}\n"
        f"Number of edges: {nx.number_of_edges(G)}\n")
    print(f"The nodes in this graph include: {list(G.nodes)[:100]}")


def getMEPDataFromID(identifier):
    x = ENTIRE_DATASET.loc[ENTIRE_DATASET['OfficialMEPID'] == identifier]
    x = x.iloc[0]
    x = x.drop(['AmendmentID',
                          'Committee',
                          'Dossier',
                          'PENumber',
                          'DocumentType',
                          'Date'])
    return dict(x)

def getMEPData(column, value):
    x = ENTIRE_DATASET.loc[ENTIRE_DATASET[column] == value]
    x = x.iloc[0]
    x = x.drop(['AmendmentID',
                          'Committee',
                          'Dossier',
                          'PENumber',
                          'DocumentType',
                          'Date'])
    return dict(x)


## TODO:  some code that will automate the process of making LaTeX tables from pandas data

def pprintPandas(df):
    for i in df:
        print(i[0], getMEPData("MEPName", i[0])["MemberState"], getMEPData("MEPName", i[0])["EPGroup"], i[1])

def pandasToLatex(df): #TODO: ezen még van mit upgradelni
    o = ""
    for i in df:

        o += f'{i[0]} & {getMEPData("MEPName", i[0])["MemberState"]} & {getMEPData("MEPName", i[0])["EPGroup"]} & {i[1]} \\\\ \n'
    #COUNTRY_ABBREV
    return o


### acquiring the split data from the csv files in ./db/split

def acquireSplitData():
    o = []
    for i in range(39):
    # the number is manual, TODO: make it automatic from the number of files in the folder:
    # https://stackoverflow.com/questions/2632205/how-to-count-the-number-of-files-in-a-directory-using-python
        o.append(pd.read_csv(f"./db/split/{i}.csv"))
    return o
