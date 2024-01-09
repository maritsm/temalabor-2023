from constants import *

from cohesiveness import *

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

def getImportantCommitteeMembers(comm=None):
    #TODO: also correct for different membership at different times
    IMPORTANT_COMMITTEE_MEMBERS = {}
    for committee in IMPORTANT_COMMITTEES:
        IMPORTANT_COMMITTEE_MEMBERS[committee] = []
        for mep in MEPLIST.values:
            name = mep[1]
            if isOrgMember(name, "Committee on the Environment, Public Health and Food Safety"): #### ????????
                IMPORTANT_COMMITTEE_MEMBERS[committee].append(name)
    if comm == None:
        return IMPORTANT_COMMITTEE_MEMBERS
    else:
        return IMPORTANT_COMMITTEE_MEMBERS[comm]
    
def getCosponsorshipDataset():
    return nx.from_pandas_edgelist(COSPONSORSHIP_EDGELIST, source ="amendment_id", target = "person_full_name")

def getBigBoyDataFrame():
    pa = PROCEDURE_POLICYAREA
    cosp = COSPONSORSHIP_EDGELIST
    docorg = DOCUMENT_ORGANIZATION
    smallboy = pd.merge(cosp, pa, on="procedure_interinst_id")
    return pd.merge(smallboy, DOCUMENT_ORGANIZATION, on = "document_eu_id")

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

###########
    
def getProcedureDates():
    return pd.read_csv("db/procdate.csv", header = 0, keep_default_na = False)

def getProcedureDateDict():
    cosp = COSPONSORSHIP_EDGELIST
    proc = cosp.groupby("procedure_interinst_id")
    procedure_dates = {}
    for i, x in proc:
        procedure_dates[i] = min(x["date"].unique())
    return procedure_dates

def getCohDf():
    ## copypastelgetés a `splitbigboy.ipynb`-ból
    my_committees = ["ITRE", "ENVI", "AFET"]
    bigboy = getBigBoyDataFrame()
    data_to_plot = {}
    for cmtee in my_committees:
        cmteeonly = bigboy.loc[bigboy["organization_abbr"] == cmtee]
        cmtee_members = getImportantCommitteeMembers(comm=cmtee)
        #TODO: EP Groupra is filterelni
        pedno = cmteeonly.groupby(cmteeonly.procedure_interinst_id)

        coh_overtime = {}
        ## TODO: itt vetítés
        for i, x in pedno:
            pdedgelist = nx.from_pandas_edgelist(x, source='amendment_id', target = 'person_full_name')
            coh_overtime[i] = cohesiveness(pdedgelist, pdedgelist)
        data_to_plot[cmtee] = coh_overtime
    coh_df = pd.DataFrame(data_to_plot)
    procdate =  getProcedureDateDict()
    coh_df.index = coh_df.index.map(lambda x : procdate[x])
    coh_df.sort_index(inplace=True)

    return coh_df