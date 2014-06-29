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

    To Do
    --- Pass the number of orgs to the chart.
    --- Add the org home page URI as a parameter.  Make sure every org has a
        value -- D3 doesn't like missing values
    --- make the tooltip persistent so that you can click on the URIs.
    --- Make the link in the notes clickable
    --- Try the hierarchcal display and doing a transform between radial and
        hierarchical

    Future enhancements
    --- How to handle orgs that report to more than one org.  In this version,
        the child is replicated as a child of each of its parents.
"""

__author__      = "Michael Conlon"
__copyright__   = "Copyright 2013, University of Florida"
__license__     = "BSD 3-Clause license"
__version__     = "0.2"

import vivotools as vt
import json
import string
import tempita

def get_org_parms(uri,orgs):
    """
    Given an org uri, find the parms for the org in the orgs json, and identify
    the uri of the children of the org
    """
    org_parms = {}
    for entry in orgs:
        if entry["uri"]["value"] == uri:
            for key in entry.keys():
                if key == "childuri":
                    if "childuri" in org_parms:
                        org_parms["childuri"].append(entry[key]["value"])
                    else:
                        org_parms["childuri"] = [entry[key]["value"]]
                elif key == "type":
                    type = entry["type"]["value"]
                    if type.find("Administrative") > 0:
                        type = "AdministrativeUnit"
                    elif type.find("NonGovernmentalOrganization") > 0:
                        type = "NonGovernmentalOrganization"
                    else:
                        type = type.split("#")[1]
                    org_parms["type"] = type
                else:
                    org_parms[key] = entry[key]["value"]
    return org_parms

def tree_build(uri,orgs):
    """
    Given uri, the uri of an org in VIVO, and orgs, the JSON list from VIVO,
    take the next step in the recursion to add the org at the uri, and process
    each childuri, if any
    """
    org_parms = get_org_parms(uri,orgs)
    if "childuri" in org_parms:
        # process children
        org_parms["children"] = []
        for curi in org_parms["childuri"]:
            if curi != uri:
                org_parms["children"].append(tree_build(curi,orgs))
    return org_parms

query = tempita.Template("""
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
            vivo:StudentOrganization, vivo:Team, vivo:Consortium,
            vivo:Museum, vivo:AcademicDepartment)) .
        FILTER (!bound(?successor)) .
        }
        GROUP BY ?uri ?childuri
        ORDER BY ?uri ?childuri""")
query = query.substitute()

# Data from file
# orgs = json.loads(open('orgs-vivo-in.json').read())["results"]["bindings"]

# Data from VIVO SPARQL query

orgs = vt.vivo_sparql_query(query)["results"]["bindings"]

org_dict = {}
for org in orgs:
    uri = org["uri"]["value"]
    org_dict[uri] = org_dict.get(uri,0)+1
print len(org_dict),"orgs"

result = {}
uri = "http://vivo.ufl.edu/individual/n1278130" # UF
#uri = "http://vivo.ufl.edu/individual/n8763427" # CTSI
#uri = "http://vivo.ufl.edu/individual/n142500" # CTSI Biobehavioral core
result = tree_build(uri,orgs)
orgs_file = open("orgs.json","w")
print >>orgs_file,json.dumps(result,indent=4)
orgs_file.close()
 
