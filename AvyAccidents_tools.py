import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [CSVtoShapefile, FatalityStats, AvyYearSelection, ActivitySelection,StateYearActivity_FC]
####1
class CSVtoShapefile(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "CSVtoShapefile"
        self.description = "converts avalanche .csv to .shp"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        avalanche_data = arcpy.Parameter(name="avalanche_data", displayName="avalanche csv", direction="input")
        outputDir = arcpy.Parameter(name="outputDir", displayName="Output path", direction="input")
        fcName = arcpy.Parameter(name="fcName", displayName="new fc name", direction="output")
       
        params = [avalanche_data, outputDir, fcName]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        ## convert CSV to esri shapefile
        avalanche_data = parameters[0].ValueAsText
        outputDir = parameters[1].ValueAsText
        fcName = parameters[2].ValueAsText
        
        xylayer = arcpy.management.MakeXYEventLayer(avalanche_data, 'lon', 'lat', 'xylayer')
        newfc = arcpy.FeatureClassToFeatureClass_conversion('xylayer', outputDir, fcName)

        arcpy.management.Delete('xylayer')
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
####2 
class FatalityStats(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "FatalityStats"
        self.description = "runs the fatality stats of chosen state."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        avalanche_fl = arcpy.Parameter(name="avalanche_fl", displayName="avalanche feature layer",datatype="GPLayer", direction="input")
        
        stateField = arcpy.Parameter(name="stateField", displayName="Field with State Names", datatype="Field", direction="Input")
        stateField.parameterDependencies = [avalanche_fl.name]
        
        state = arcpy.Parameter(name="state", displayName="select a state", direction= "input")
        state.filter.type = "ValueList"
        state.filter.list = []

        state_data = arcpy.Parameter(name="state_data", displayName="state input data", datatype="GPLayer", direction="input")
        params = [avalanche_fl, stateField, state, state_data]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if parameters[1].value:
            with arcpy.da.SearchCursor(parameters[0].valueAsText, parameters[1].valueAsText) as rows:
                parameters[2].filter.list = sorted(list(set([row[0] for row in rows])))
        else:
            parameters[2].filter.list = []
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        ## convert CSV to esri shapefile
        #make new fc with results of fatality stats
        #Define data
        ## Make state analysis selection
        
        avalanche_fl = parameters[0].ValueAsText
        state_data = parameters[3].ValueAsText
        state = parameters[2].ValueAsText
        
        out_fc = "{}_FatalityStats".format(state)
        wc = """STUSPS = '{}'""".format(state)
        state_sel = arcpy.analysis.Select(state_data, out_fc, wc)

        ## Add new fields and populate with stats calculations

        ## Total deaths
        total_fatal = arcpy.management.AddField(state_sel, 'total_fatal', 'FLOAT')

        state_list = []
        fields = ['State', 'Killed']
        totalcursor = arcpy.da.SearchCursor(avalanche_fl, fields)
        for row in totalcursor: 
            if row[0] == state:
                state_list.append(row[1])

        ## Percentage of total national deaths
        perc_fatal = arcpy.management.AddField(state_sel, 'perc_fatal', 'DOUBLE')

        US_list = []
        perccursor = arcpy.da.SearchCursor(avalanche_fl, fields)
        for row in perccursor:
            US_list.append(row[1])

        ## populate state_sel with results of search cursor
        UP_fields = ['total_fatal', 'perc_fatal']
        updatecursor = arcpy.da.UpdateCursor(state_sel, UP_fields)
        for row in updatecursor:
            row[0] = sum(state_list)
            row[1] = sum(state_list)/sum(US_list)
            updatecursor.updateRow(row)

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
####3
class AvyYearSelection(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "AvyYearSelect"
        self.description = "makes an analysis selection of the chosen Avy Year"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        avalanche_fl = arcpy.Parameter(name="avalanche_fl", displayName="avalanche feature layer",datatype="GPLayer", direction="input")
        AvyYear_Field = arcpy.Parameter(name="AvyYear_Field", displayName="Field with Avalanche Year", datatype="Field", direction="Input")
        AvyYear_Field.parameterDependencies = [avalanche_fl.name]
        
        year = arcpy.Parameter(name="year", displayName="Avalanche Year", direction="input")
        year.filter.type = "ValueList"
        year.filter.list = []
    
        params = [avalanche_fl, AvyYear_Field, year]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if parameters[1].value:
            with arcpy.da.SearchCursor(parameters[0].valueAsText, parameters[1].valueAsText) as rows:
                parameters[2].filter.list = sorted(list(set([row[0] for row in rows])))
        else:
            parameters[2].filter.list = []
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        in_data = parameters[0].ValueAsText
        year = parameters[2].ValueAsText
        
        out_fc = "AvyAccidents_{}".format(year)
        wc = """AvyYear = {}""".format(year)

        year_sel = arcpy.analysis.Select(in_data, out_fc, wc)

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
####
class ActivitySelection(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "ActivitySelection"
        self.description = "makes an analysis selection of the chosen Activty"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        avalanche_fl = arcpy.Parameter(name="avalanche_fl", displayName="avalanche feature layer",datatype="GPLayer", direction="input")
        PrimaryActivity_Field = arcpy.Parameter(name="PrimaryActivity_field", displayName="Field with activity data", datatype="Field", direction="Input")
        PrimaryActivity_Field.parameterDependencies = [avalanche_fl.name]
        
        activity = arcpy.Parameter(name="activity", displayName="activity", direction="input")
        activity.filter.type = "ValueList"
        activity.filter.list = []

        
        activity_fc = arcpy.Parameter(name="activity_fc", displayName="Activity name for fc name (no spaces)", direction="output")

        params = [avalanche_fl, PrimaryActivity_Field, activity, activity_fc]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if parameters[1].value:
            with arcpy.da.SearchCursor(parameters[0].valueAsText, parameters[1].valueAsText) as rows:
                parameters[2].filter.list = sorted(list(set([row[0] for row in rows])))
        else:
            parameters[2].filter.list = []
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        in_data = parameters[0].ValueAsText
        activity = parameters[2].ValueAsText
        activity_fc = parameters[3].ValueAsText

        out_fc = "{}_AvyAccidents".format(activity_fc)
        wc = """PrimaryActivity = '{}'""".format(activity)

        activity_sel = arcpy.analysis.Select(in_data, out_fc, wc)
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return

####5
class StateYearActivity_FC(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "StateYearActivity_FC"
        self.description = "makes an analysis selection of the given state, year, and activty. Populates new feilds with fatality values."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        avalanche_fl = arcpy.Parameter(name="avalanche_fl", displayName="avalanche feature layer",datatype="GPLayer", direction="input")
        
        state_Field = arcpy.Parameter(name="state_Field", displayName="Field with state data", datatype="Field", direction="Input")
        state_Field.parameterDependencies = [avalanche_fl.name]
        
        state = arcpy.Parameter(name="state", displayName="choose a state", direction="input")
        state.filter.type = "ValueList"
        state.filter.list = []
        
        year_Field = arcpy.Parameter(name="year_Field", displayName="Field with Avy Year data", datatype="Field", direction="Input")
        year_Field.parameterDependencies = [avalanche_fl.name]
        
        year = arcpy.Parameter(name="year", displayName="choose a year", direction="input")
        year.filter.type = "ValueList"
        year.filter.list = []
        
        activity_Field = arcpy.Parameter(name="activity_Field", displayName="Field with activity data", datatype="Field", direction="Input")
        activity_Field.parameterDependencies = [avalanche_fl.name]
        
        activity = arcpy.Parameter(name="activity", displayName="choose an activity", direction="input")
        activity.filter.type = "ValueList"
        activity.filter.list = []
        
        state_data = arcpy.Parameter(name="state_data", displayName="state feature layer",datatype="GPLayer", direction="input")
        activity_name = arcpy.Parameter(name="activity_name", displayName="Activity name for fc name(no spaces)", direction="output")
        params = [avalanche_fl, state_Field, state, year_Field, year, activity_Field, activity, state_data, activity_name]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if parameters[1].value:
            with arcpy.da.SearchCursor(parameters[0].valueAsText, parameters[1].valueAsText) as rows:
                parameters[2].filter.list = sorted(list(set([row[0] for row in rows])))
        else:
            parameters[2].filter.list = []
            
        if parameters[3].value:
            with arcpy.da.SearchCursor(parameters[0].valueAsText, parameters[3].valueAsText) as rows:
                parameters[4].filter.list = sorted(list(set([row[0] for row in rows])))
        else:
            parameters[4].filter.list = []
        
        if parameters[5].value:
            with arcpy.da.SearchCursor(parameters[0].valueAsText, parameters[5].valueAsText) as rows:
                parameters[6].filter.list = sorted(list(set([row[0] for row in rows])))
        else:
            parameters[6].filter.list = []
        
        return

    
    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        avalanche_fl = parameters[0].ValueAsText
        state = parameters[2].ValueAsText
        year = parameters[4].ValueAsText 
        activity = parameters[6].ValueAsText
        state_data = parameters[7].ValueAsText
        activity_name = parameters[8].ValueAsText
        
        #state selection
        out_fc = "{}_{}_{}_AvyAccidents".format(state, year, activity_name)
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

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
