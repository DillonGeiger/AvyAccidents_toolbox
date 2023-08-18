in_data = "Avalanche_Accidents"
year = 2020

out_fc = "AvyAccidents_{}".format(year)
print(out_fc)

wc = """AvyYear = {}""".format(year)

year_sel = arcpy.analysis.Select(in_data, out_fc, wc)
