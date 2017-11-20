# VIVO Org Chart

We use [D3](http://d3js.org) to create an interactive org chart which displays organizational structure,
serves as a data visualization for the organizations, and provides a navigation mechanism.

## Data

Where's what you'll need in your VIVO:

1. One or more orgs that have sub-structure.  At the University of Florida, the org structure of the university flows
from the University entity in VIVO.  It has subOrganization assertions and they have subOrganization assertions and
so on.  Use successorOrg to exclude organizations that are no longer active.
1. Connections between people, papers, courses, and grants to the organizations.  A person has a position in a department,
which in turn is a subOrganization of some other and so on.  That's enough to count the people in the organization.  
People author papers, and so papers can be attributed to the organization containing the person.  Grants, grant dollars,
and courses can be attributed in a similar manner.

A python program queries VIVO and makes the data structure required by D3.

## To Do

1. Update for current VIVO ontology.
1. Remove dependency on vivo tools library.
1. Update D3 to version 4.
1. Add a web site where the org chart is displayed.
1. Add interactive controls (see below)

## Future interactive controls

1. Color by org metrics

	1. Heat map on people
	1. Heat map on grants
	1. Heat paper on papers
	1. Heat map on courses
	1. Heat map on grant dollars
	1. Org type

1. Size by any org metric

1. Scale slider

1. Mouse over -- each org should show its data (whatever is selected above) when mouse over.

1. Click -- when single clicked, each org should show a data box with its metrics (see above)  It's photo. A link into VIVO.  A link to its home page. Link to Google Map (would be cool, but our orgs do not have geo properties and do not have geo data).  The data box should have a Dismiss button. The data box should stay up until dismissed.  Any number of data boxes can be open at the same time.

1. Double Click -- when double clicked, the graph should redraw with the selected org as the center of the org chart.  Might be surprising adn where is the return path?

1. Print/Export -- need to be able to export to SVG and PDF for printing.
