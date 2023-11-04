from constants import *

def listMEPs():
    return MEPLIST["person_name"]

def listPoliticalGroups():
    o = pd.unique(ENTIRE_DATASET['EPGroup'])
    return o

def listCountries():
    o = pd.unique(ENTIRE_DATASET['MemberState'])
    return o

def listOrgs():
    o = pd.unique(ORG_MEMBERSHIP["organization_name"])
    return o

def orgMemberCount(org):
    l = pd.unique(ORG_MEMBERSHIP.loc[ORG_MEMBERSHIP["organization_name"] == org]["person_name"])
    return len(l)

def getBiggestOrgs(howmany=5):
    x = []
    for i in listOrgs():
        x.append([i, orgMemberCount(i)])
    df_orgmembercount = pd.DataFrame(x, columns=["OrgName", "MemberCount"])
    asd = df_orgmembercount.sort_values(by="MemberCount", ascending=False)[0:howmany]
    return asd["OrgName"]

## DATA PER COMMITTEE

def getCommitteeSplitData():
    imp_comm_datasets = {}
    for comm in IMPORTANT_COMMITTEES:
        imp_comm_datasets[comm] = ENTIRE_DATASET.loc[ENTIRE_DATASET["Committee"] == comm]
    return imp_comm_datasets

def getCommitteeData(comm):
    # get the data for the specific committee
    return getCommitteeSplitData()[comm]

## DATA FOR EACH DOSSIER PER COMMITTEE

def getDossierSplitData():
    dossiers = {}
    for comm, data in getCommitteeSplitData().items():
        dossiers[comm] = pd.unique(data["Dossier"])
    return dossiers

def getDossierData(comm):
    return getDossierSplitData()[comm]

### acquiring the split data from the csv files in ./db/split

def acquireSplitData():
    o = []
    for i in range(39):
    # the number is manual, TODO: make it automatic from the number of files in the folder:
    # https://stackoverflow.com/questions/2632205/how-to-count-the-number-of-files-in-a-directory-using-python
        o.append(pd.read_csv(f"./db/split/{i}.csv"))
    return o

def isOrgMember(mepName, org, date=None):
    ## if `date` is not set, then we return True if the person
    ## was in the Org at any point
    if date==None:
        df = ORG_MEMBERSHIP.loc[ORG_MEMBERSHIP["organization_name"] == org]["person_name"]
        return mepName in df.values
    else:
        raise NotImplementedError("sorry, can't check for the date yet :(")
