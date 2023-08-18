avalanche_fl = "Avalanche_Accidents"
state = "CO"
year = 2020
activty = "Climber"
state_data = "US_states"

#state selection
out_fc = "{}_{}_{}_AvyAccidents".format(state, year, activity)
print(out_fc)

wc = """STUSPS = '{}'""".format(state)
state_sel = arcpy.analysis.Select(state_data, out_fc, wc)
#year selection
#new field
AvyYear = arcpy.management.AddField(state_sel, 'AvyYear', 'LONG')

#activty selection
#new field
Activity = arcpy.management.AddField(state_sel, 'Activity', 'TEXT')

#fatalities
#new field
Killed = arcpy.management.AddField(state_sel, 'Killed', 'TEXT')
fatal_list = []
fields = ['State', 'AvyYear', 'Killed']
cursor = arcpy.da.SearchCursor(avalanche_fl, fields)
for row in cursor: 
    if row[0] == state and row[1] == year:
        fatal_list.append(row[2])
        print(fatal_list)

UP_fields = ['AvyYear', 'Activity', 'killed']
updatecursor = arcpy.da.UpdateCursor(state_sel, UP_fields)
for row in updatecursor:
    row[0] = year
    row[1] = activity
    row[2] = sum(fatal_list)
    updatecursor.updateRow(row)
