import pandas as pd
import networkx as nx

DATA_LOCATION = "db/ep_cosponsorship_dataset.csv"
# we put `keep_default_na` here so that nan-s get parsed in the way we want
ENTIRE_DATASET = pd.read_csv(DATA_LOCATION, header = 0, keep_default_na = False)

MEPLIST = pd.read_csv("db/meplist_9th_term.csv", header = 0, keep_default_na = False)

EPGROUP_MEMBERSHIP = pd.read_csv("db/epgroup_memberships_9th_term.csv", header = 0, keep_default_na = False)

ORG_MEMBERSHIP = pd.read_csv("db/organization_membership_9th_term.csv", header = 0, keep_default_na = False)

COSPONSORSHIP_EDGELIST = pd.read_csv("db/cosponsorship_edgelist_9th_term.csv", header = 0, keep_default_na = False)

DOCUMENT_ORGANIZATION = pd.read_csv("db/document_organization_9th_term.csv", header = 0, keep_default_na = False)

PROCEDURE_POLICYAREA = pd.read_csv("db/procedure_policyarea_9th_term.csv", header = 0, keep_default_na = False)

# the committees we will analyze
IMPORTANT_COMMITTEES = ["ENVI", "AFET", "ITRE"]

### from down here it's obsolete data

COUNTRY_POPULATION = {
    "Austria" : 9106126,
    "Belgium" : 11584008,
    "Bulgaria" : 6519789,
    "Croatia" : 3871833,
    "Cyprus" : 918100,
    "Czechia" : 10524167,
    "Denmark" : 5932654,
    "Estonia" : 1331824,
    "Finland" : 5563970,
    "France" : 65269154,
    "Germany" : 83237124,
    "United Kingdom" : 66980000,
    "Greece" : 10432481,
    "Hungary" : 9772756,
    "Ireland" : 5149139,
    "Italy" : 58850717,
    "Latvia" : 1893223,
    "Lithuania" : 2810761,
    "Luxembourg" : 645397,
    "Malta" : 519562,
    "Netherlands" : 17590672,
    "Poland" : 38036118,
    "Portugal" : 10343066,
    "Romania" : 19053815,
    "Slovakia" : 5428792,
    "Slovenia" : 2107180,
    "Spain" : 47400798,
    "Sweden" : 10521556
}

NO_EP_SEATS_POST_BREXIT =  {
    "Austria" : 19,
    "Belgium" : 21,
    "Bulgaria" : 17,
    "Croatia" : 12,
    "Cyprus" : 6,
    "Czechia" : 21,
    "Denmark" : 14,
    "Estonia" : 7,
    "Finland" : 14,
    "France" : 79,
    "Germany" : 96,
    "United Kingdom" : 0,
    "Greece" : 21,
    "Hungary" : 21,
    "Ireland" : 13,
    "Italy" : 76,
    "Latvia" : 8,
    "Lithuania" : 11,
    "Luxembourg" : 6,
    "Malta" : 6,
    "Netherlands" : 29,
    "Poland" : 52,
    "Portugal" : 21,
    "Romania" : 33,
    "Slovakia" : 14,
    "Slovenia" : 8,
    "Spain" : 59,
    "Sweden" : 21
}

NO_EP_SEATS_PRE_BREXIT =  {
    "Austria" : 18,
    "Belgium" : 21,
    "Bulgaria" : 17,
    "Croatia" : 11,
    "Cyprus" : 6,
    "Czechia" : 21,
    "Denmark" : 13,
    "Estonia" : 6,
    "Finland" : 13,
    "France" : 74,
    "Germany" : 96,
    "United Kingdom" : 27+46,
    "Greece" : 21,
    "Hungary" : 21,
    "Ireland" : 11,
    "Italy" : 73,
    "Latvia" : 8,
    "Lithuania" : 11,
    "Luxembourg" : 6,
    "Malta" : 6,
    "Netherlands" : 26,
    "Poland" : 51,
    "Portugal" : 21,
    "Romania" : 32,
    "Slovakia" : 13,
    "Slovenia" : 8,
    "Spain" : 58,
    "Sweden" : 20
}

#pre-brexit
EP_GROUP_NO_SEATS_PRE_BREXIT = {
    'EPP': 182,
    'ECR': 62,
    'ID': 73,
    'Greens/EFA': 74,
    'RE': 108,
    'S&D': 154,
    'NI': 54,
    'GUE/NGL': 41,
}

#post-brexit
EP_GROUP_NO_SEATS_POST_BREXIT = {
    'EPP': 187,
    'ECR': 61,
    'ID': 76,
    'Greens/EFA': 67,
    'RE': 98,
    'S&D': 147,
    'NI': 29,
    'GUE/NGL': 39,
}

COUNTRY_ABBREV = {
    "Austria" : "AT",
    "Belgium" : "BE",
    "Bulgaria" : "BG",
    "Croatia" : "HR",
    "Cyprus" : "CY",
    "Czechia" : "CZ",
    "Denmark" : "DK",
    "Estonia" : "EE",
    "Finland" : "FI",
    "France" : "FR",
    "Germany" : "DE",
    "United Kingdom" : "GB",
    "Greece" : "GR",
    "Hungary" : "HU",
    "Ireland" : "IE",
    "Italy" : "IT",
    "Latvia" : "LV",
    "Lithuania" : "LT",
    "Luxembourg" : "LU",
    "Malta" : "MT",
    "Netherlands" : "NL",
    "Poland" : "PL",
    "Portugal" : "PT",
    "Romania" : "RO",
    "Slovakia" : "SK",
    "Slovenia" : "SI",
    "Spain" : "ES",
    "Sweden" : "SE"
}
