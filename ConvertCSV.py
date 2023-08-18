## make imports and define workspace
## convert CSV to esri shapefile

import arcpy

avalanche_data = r'C:\Users\dillongeiger\Desktop\Final\Avalanche_data\Accidents_2022_PUBLIC - Data.csv'
fcName = 'Avalanche_Accidents'
outputDir = r'C:\Users\dillongeiger\Desktop\Final\Avalanche_Accidents\Avalanche_Accidents.gdb'

xylayer = arcpy.management.MakeXYEventLayer(avalanche_data, 'lon', 'lat', 'xylayer')
newfc = arcpy.FeatureClassToFeatureClass_conversion('xylayer', outputDir, fcName)
arcpy.management.Delete('xylayer')


