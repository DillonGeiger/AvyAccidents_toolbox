import arcpy
in_data = "Avalanche_Accidents"
activity = "Climber"

out_fc = "{}_AvyAccidents".format(activity)
print(out_fc)

wc = """PrimaryActivity = '{}'""".format(activity)

activity_sel = arcpy.analysis.Select(in_data, out_fc, wc)
