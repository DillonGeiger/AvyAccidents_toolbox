# AvyAccidents_toolbox
Avalanche Accidents Python Toolbox

This repository is for the "AvyAccidents_tools" Python toolbox. The python toolbox has five tools that conduct an analysis of the national avalanche accident data that is managed by the Colorado Avalanche Information Center.

Two sets of data are required to run the toolbox. 
The primary data source is a .CSV file Therefore the first tool that must be utilized is the "CSVtoShapefile" tool That converts the CSV file to a usable feature layer. The second data source is a .shp file of the US states.

After utilizing this tool first any of the other tools may be used.
"ActivitySelection", and "AvyYearSelection" Make simple selections of the input activity and input Avy Year.
"Fatality Stats" Makes an analysis selection of a state adds to new fields and populates the fields with the total deaths for the given state and the percentage of the total national fatalities.
"StateYearActivity_FC" makes an analysis selection of state, year, and activity. Next it adds 3 new fields populated with year, activity, and total fatalities for the given year and activity.

of the seven remaining files in the repository only two of them are of importance:
"AvalancheToolbox.ipynb" Is the complete and functioning Jupyter notebook for the toolbox.
"AvyAccidents_tools.py" is the complete and functioning python file that can be used for the toolbox.

The remaining files in the repository are script snippets of each tool and have since been edited to be adapted towards the python toolbox.
