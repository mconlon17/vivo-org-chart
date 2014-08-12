#!/usr/bin/env/python

"""
    orgs-json.py: Given JSON file from VIVO listing orgs and their sub orgs,
    build a heirarchical JSON file in which elements are children of other
    elements

    Version 0.1 MC 2013-10-04
    --- Read VIVO JSON, write heirarchical JSON using recursive function
        tree_build
    Version 0.2 MC 2013-12-08
    --  Query VIVO and write file orgs.json.  Add Number of employees count
        to each org.
    --  Title is now in upper left -- better for on screen viewing.  Name of
        org is now displayed from name of root node rather than hard coded.
    Version 0.3 MC 2014-08-11
    --  Remove the tempita dependency
    --  pylint standard coding
    --  pass the org_count to D3 for display

    To Do
    --- Add the org home page URI as a parameter.  Make sure every org has a
        value -- D3 doesn't like missing values
    --- Try the hierarchical display and doing a transform between radial and
        hierarchical
    --  Start from any org, not just UF (unions to depth)

    Future enhancements
    --- How to handle orgs that report to more than one org.  In this version,
        the child is replicated as a child of each of its parents.
"""

__author__ = "Michael Conlon"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause license"
__version__ = "0.3"

from vivotools import vivo_sparql_query
import json

def get_org_parms(org_uri, orgs):
    """
    Given an org_uri, find the parms for the org in the orgs json, and
    identify the org_uri of the children of the org
    """
    org_parms = {}
    for entry in orgs:
        if entry["uri"]["value"] == org_uri:
            for key in entry.keys():
                if key == "childuri":
                    if "childuri" in org_parms:
                        org_parms["childuri"].append(entry[key]["value"])
                    else:
                        org_parms["childuri"] = [entry[key]["value"]]
                elif key == "type":
                    org_type = entry["type"]["value"]
                    if org_type.find("Administrative") > 0:
                        org_type = "AdministrativeUnit"
                    elif org_type.find("NonGovernmentalOrganization") > 0:
                        org_type = "NonGovernmentalOrganization"
                    else:
                        org_type = org_type.split("#")[1]
                    org_parms["type"] = org_type
                else:
                    org_parms[key] = entry[key]["value"]
    return org_parms

def tree_build(org_uri, orgs):
    """
    Given the uri of an org in VIVO, and orgs, the JSON list from VIVO,
    take the next step in the recursion to add the org at the uri, and process
    each childuri, if any
    """
    org_parms = get_org_parms(org_uri, orgs)
    if "childuri" in org_parms:
        # process children
        org_parms["children"] = []
        for curi in org_parms["childuri"]:
            if curi != org_uri:
                org_parms["children"].append(tree_build(curi, orgs))
    return org_parms

query = """
    SELECT ?uri (MIN (DISTINCT ?uritype) AS ?type)
        (SAMPLE(DISTINCT ?urilabel) AS ?name) ?childuri
        (COUNT(DISTINCT ?person) AS ?nemployees)
    WHERE {
        {?uri a foaf:Organization .} UNION {?uri a foaf:Group .}
        ?uri a ufVivo:UFEntity .
        ?uri rdfs:label ?urilabel .
        ?uri a ?uritype .
        OPTIONAL {?uri vivo:hasSubOrganization ?childuri .}
        OPTIONAL {?uri vivo:hasSuccessorOrganization ?successor .}
        OPTIONAL {?uri ufVivo:homeDeptFor ?person . }
        FILTER (?uritype IN (vivo:College, vivo:University, vivo:Department,
            ufVivo:AdministrativeUnit,vivo:Center, vivo:Institute, vivo:School, vivo:ExtensionUnit, vivo:Library, vivo:Program, vivo:Committee,
            vivo:Foundation, vivo:Laboratory, vivo:Division, vivo:Company,
            vivo:Association, vivo:ClinicalOrganization, vivo:Hospital,
            vivo:Publisher, ufVivo:NonGovernmentalOrganization,
            vivo:ResearchOrganization,
            vivo:StudentOrganization, vivo:Team, vivo:Consortium,
            vivo:Museum, vivo:AcademicDepartment)) .
        FILTER (!bound(?successor)) .
        }
        GROUP BY ?uri ?childuri
        ORDER BY ?uri ?childuri"""

# Data from VIVO SPARQL query

org_result = vivo_sparql_query(query)["results"]["bindings"]

org_dict = {}
for org in org_result:
    uri = org["uri"]["value"]
    org_dict[uri] = org_dict.get(uri, 0)+1
print len(org_dict), "orgs"

result = {}
uri = "http://vivo.ufl.edu/individual/n1278130" # UF
#uri = "http://vivo.ufl.edu/individual/n8763427" # CTSI
#uri = "http://vivo.ufl.edu/individual/n142500" # CTSI Biobehavioral core
result = tree_build(uri, org_result)
result["org_count"] = len(org_dict)
orgs_file = open("orgs.json", "w")
print >>orgs_file, json.dumps(result, indent=4)
orgs_file.close()
