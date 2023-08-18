#make new fc with results of fatality stats
#Define data
## Make state analysis selection
in_data = "Avalanche_Accidents1"
state_data = "US_states"
state = 'CA'
out_fc = "{}_FatalityStats".format(state)
wc = """STUSPS = '{}'""".format(state)
state_sel = arcpy.analysis.Select(state_data, out_fc, wc)

## Add new fields and populate with stats calculations

## Total deaths
total_fatal = arcpy.management.AddField(state_sel, 'total_fatal', 'FLOAT')

state_list = []
fields = ['State', 'Killed']
totalcursor = arcpy.da.SearchCursor(in_data, fields)
for row in totalcursor: 
    if row[0] == state:
        state_list.append(row[1])

## Percentage of total national deaths
perc_fatal = arcpy.management.AddField(state_sel, 'perc_fatal', 'DOUBLE')

US_list = []
perccursor = arcpy.da.SearchCursor(in_data, fields)
for row in perccursor:
    US_list.append(row[1])
    
## populate state_sel with results of search cursor
UP_fields = ['total_fatal', 'perc_fatal']
updatecursor = arcpy.da.UpdateCursor(state_sel, UP_fields)
for row in updatecursor:
    row[0] = sum(state_list)
    row[1] = sum(state_list)/sum(US_list)
    updatecursor.updateRow(row)
