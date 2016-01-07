import CMOR3Table
import json

AllVars = CMOR3Table.CMOR3Table()

MIPs = AllVars.getMIPs();
cmor3Table={}
cmor3Table['MIPs'] = {}
for MIP in MIPs:
    cmor3Table['MIPs'][MIP[0]] = {}
    cmor3Table['MIPs'][MIP[0]]['experimentGroups'] = {}
    exptGroups = AllVars.getExperimentGroups(MIP[0])
    for exptGroup in exptGroups:
	exptGroupLabel =  AllVars.getExperimentGroupLabel(exptGroup[0])
	cmor3Table['MIPs'][MIP[0]]['experimentGroups'][exptGroupLabel] = {}
	cmor3Table['MIPs'][MIP[0]]['experimentGroups'][exptGroupLabel]['experiments'] = {}
	experimentsDict = cmor3Table['MIPs'][MIP[0]]['experimentGroups'][exptGroupLabel]['experiments'] 
	experiments =  AllVars.getExperimentsbyExptGroupID(exptGroup[0],MIP[0])
	for experiment in experiments:
	    experimentLabel =  AllVars.getExperimentLabel(experiment[0])
	    experimentsDict[experimentLabel]= {}
	    experimentsDict[experimentLabel]['variables'] = {}
	    variablesDict=experimentsDict[experimentLabel]['variables'] 
	    variables=AllVars.getVariables(MIP[0],exptGroupLabel,experimentLabel)
	    for variable in variables:
		grid = AllVars.getGrid(variable[0])
		spatialShape = AllVars.getSpatialShape(grid[0])
		temporalShape = AllVars.getTemporalShape(grid[1])
		varDict = AllVars.convertVarStructureToDictionary(variable)
		# Print Report
		# ----------------------
		variablesDict[varDict['label']] = {}
		currentVarDict=variablesDict[varDict['label']]
		currentVarDict['frequency']         = varDict['frequency']
		currentVarDict['mipTable']          = varDict['mipTable']
		currentVarDict['modeling_realm']    = varDict['modeling_realm']
		currentVarDict['ok_max_mean_abs']   = varDict['ok_max_mean_abs']
		currentVarDict['ok_min_mean_abs']   = varDict['ok_min_mean_abs']
		currentVarDict['positive']          = varDict['positive']
		currentVarDict['valid_max']         = varDict['valid_max']
		currentVarDict['valid_min']         = varDict['valid_min']
		currentVarDict['cell_measures']     = grid[2]
		currentVarDict['cell_methods']      = grid[3]
		currentVarDict['dimensions']        = spatialShape[0]
		currentVarDict['levelFlag']         = spatialShape[1]
		currentVarDict['levels']            = spatialShape[2]
		currentVarDict['timeDimension']     = temporalShape[0]
		currentVarDict['timeLabel']         = temporalShape[1]
AllVars.close()
print json.dumps(cmor3Table, indent=4)

