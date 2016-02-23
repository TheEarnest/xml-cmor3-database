import json
import CMOR3Table
import re
import datetime
import CMOR3Template
import sys
import getopt
# import pdb

cmorVersion = "3.0"
cfVersion = "1.6"
projectID = "CMIP6"
tableDate = datetime.date.today().strftime("%d %B %Y")
missingValue = "1e20"
approxInterval = "30.000000"
tableDict = CMOR3Template.tableDict
cursor = CMOR3Table.CMOR3Table()
MIPS = cursor.getMIPs()
JSON = ""


# ==============================================================
#                     replaceString()
# ==============================================================
def replaceString(var_entry, var, field):
    """
       Replace a <field> with a string (deleting "<" and ">")
    """
    if(var == ''):
        var_entry = re.sub(r"" + field + ":.*\n", "", var_entry)
    var_entry = var_entry.replace("<" + field + ">", var)
    return var_entry


# ==============================================================
#                     createHeader()
# ==============================================================
def createHeader(realm="Amon", bJSON=True):
    """
    Create CMIP6 Header table
    """
    try:
        approxInterval = tableDict[realm]["approxInterval"]
        genericLevels = tableDict[realm]["genericLevels"]
    except:
        approxInterval = ""
        genericLevels = ""
    Header = CMOR3Template.Header
    if(bJSON):
        Header = CMOR3Template.HeaderJSON
    Header = replaceString(Header, cmorVersion,    "cmorVersion")
    Header = replaceString(Header, cfVersion,      "cfVersion")
    Header = replaceString(Header, projectID,      "projectID")
    Header = replaceString(Header, tableDate,      "tableDate")
    Header = replaceString(Header, missingValue,   "missingValue")
    Header = replaceString(Header, approxInterval, "approxInterval")
    Header = replaceString(Header, realm,          "table")
    Header = replaceString(Header, genericLevels, "generic_levels")
    Header = Header.replace("<modeling_realm>", varSQL[0][3])
    Header = Header.replace("<frequency>", varSQL[0][1])
    return Header


# ==============================================================
#                     createHeader()
# ==============================================================
def createFooter(bJSON=True):
    """
    Close main bJSON object is needed
    """
    if(bJSON):
        return "}\n"
    return ""


# ==============================================================
#                     createAxes()
# ==============================================================
def createAxes(bJSON=True):
    """
    Define all axis entries in table
    """
    Allaxes = cursor.getAxes()
    if(bJSON):
        axis_entry = "\"axis_entry\": {"
    else:
        axis_entry = ""

    for entry in Allaxes:
        axis = list(entry)
        if(bJSON):
            axis_entry = axis_entry + CMOR3Template.axisTemplateJSON
        else:
            axis_entry = axis_entry + CMOR3Template.axisTemplate

        if(axis[8] == ""):
            axis[8] = "\"\""
        axis_entry = replaceString(axis_entry, axis[0], "axis_entry")
        axis_entry = replaceString(axis_entry, axis[1], "axis")
        axis_entry = replaceString(axis_entry, axis[2], "climatology")
        axis_entry = replaceString(axis_entry, axis[3], "formula")
        axis_entry = replaceString(axis_entry, axis[4], "long_name")
        axis_entry = replaceString(axis_entry, axis[5], "must_have_bounds")
        axis_entry = replaceString(axis_entry, axis[6], "out_name")
        axis_entry = replaceString(axis_entry, axis[7], "positive")
        axis_entry = replaceString(axis_entry, axis[8], "requested")
        axis_entry = replaceString(axis_entry, axis[9], "standard_name")
        axis_entry = replaceString(axis_entry, axis[10], "stored_direction")
        axis_entry = replaceString(axis_entry, axis[11], "tolerance")
        axis_entry = replaceString(axis_entry, axis[12], "type")
        axis_entry = replaceString(axis_entry, axis[13], "units")
        axis_entry = replaceString(axis_entry, axis[14], "valid_min")
        axis_entry = replaceString(axis_entry, axis[15], "valid_max")
        axis_entry = replaceString(axis_entry, axis[16], "value")
        axis_entry = replaceString(axis_entry, axis[17], "z_bounds_factors")
        axis_entry = replaceString(axis_entry, axis[18], "z_factors")
    if(bJSON):
        axis_entry = axis_entry + "\"Dummy\": \"\"\n},"
    return axis_entry


# ==============================================================
#                     createFormulaVar()
# ==============================================================
def createFormulaVar(bJSON=True):
    """
    Define all variables needed by formula.
    """
    formulaVars = cursor.getFormulaVars()

    if(bJSON):
        var_entry = "\"variable_entry\": {"
    else:
        var_entry = ""

    for entry in formulaVars:
        fvar = list(entry)
        # -----------------------------------------------
        # Add double quote for JSON if dimension is empty
        # -----------------------------------------------
        if(bJSON):
            var_entry = var_entry + CMOR3Template.FormulaVarTemplateJSON
        else:
            var_entry = var_entry + CMOR3Template.FormulaVarTemplate

        var_entry = replaceString(var_entry, fvar[0], "variable_entry")
        var_entry = replaceString(var_entry, fvar[1], "long_name")
        var_entry = replaceString(var_entry, fvar[2], "type")
        var_entry = replaceString(var_entry, fvar[3].strip(), "dimensions")
        var_entry = replaceString(var_entry, fvar[4], "units")

    return var_entry


# ==============================================================
#                     createVariables()
# ==============================================================
def createGrids(bJSON=True):
    """
    Create grib tables
    """

    Header = CMOR3Template.GridHeaderJSON
    Header = replaceString(Header, cmorVersion,    "cmorVersion")
    Header = replaceString(Header, cfVersion,      "cfVersion")
    Header = replaceString(Header, projectID,      "projectID")
    Header = replaceString(Header, tableDate,      "tableDate")
    Header = replaceString(Header, missingValue,   "missingValue")
    Footer = "}\n"

    GridAxes = cursor.getAxesGrids()

    vars = cursor.getVarGrids()
    varSQL = [vars[i] for i in range(len(vars))]

    axis_entry = "\"axis_entry\": {"
    for entry in GridAxes:
        axis = list(entry)
        axis_entry += CMOR3Template.GridAxisTemplateJSON

        axis_entry = replaceString(axis_entry, axis[0], "grid_axis_entry")
        axis_entry = replaceString(axis_entry, axis[1], "axis")
        axis_entry = replaceString(axis_entry, axis[2], "long_name")
        axis_entry = replaceString(axis_entry, axis[3], "out_name")
        axis_entry = replaceString(axis_entry, axis[4], "standard_name")
        axis_entry = replaceString(axis_entry, axis[5], "type")
        axis_entry = replaceString(axis_entry, axis[6], "units")

    axis_entry += "\"Dummy\": \"\"\n},"

    variable_entry = "\"variable_entry\": {"
    for varGrid in varSQL:
        variable_entry += CMOR3Template.GridVarTemplateJSON
        variable_entry = replaceString(variable_entry, varGrid[0], "grid_variable_entry")
        variable_entry = replaceString(variable_entry, varGrid[1], "standard_name")
        variable_entry = replaceString(variable_entry, varGrid[2], "units")
        variable_entry = replaceString(variable_entry, varGrid[3], "long_name")
        variable_entry = replaceString(variable_entry, varGrid[5], "out_name")
        variable_entry = replaceString(variable_entry, varGrid[6], "valid_min")
        variable_entry = replaceString(variable_entry, varGrid[7], "valid_max")
        variable_entry = variable_entry.replace("<dimensions>",
                                                (varGrid[4].replace("|", " ")).strip(" "))

    variable_entry = variable_entry + "\"Dummy\":   \"\"\n }"

    CMIP6Table = (json.loads("".join(Header + axis_entry + variable_entry + Footer)))

    if("Dummy" in CMIP6Table['axis_entry']):
        del CMIP6Table['axis_entry']['Dummy']
    if("Dummy" in CMIP6Table['variable_entry']):
        del CMIP6Table['variable_entry']['Dummy']

    print(json.dumps(CMIP6Table, indent=4))


# ==============================================================
#                     createVariables()
# ==============================================================
def createVariables(bJSON=True):
    """
    Define All Variables
    """

    var_entry = createFormulaVar(bJSON)

    for entry in varSQL:
        var = list(entry)

        if(bJSON):
            var_entry = var_entry + CMOR3Template.VarTemplateJSON
        else:
            var_entry = var_entry + CMOR3Template.VarTemplate
        # -------------------------------------------------------------
        #  Delete "unset" comment
        # -------------------------------------------------------------
        if(var[16] == 'unset'):
            var[16] = ''
        var_entry = replaceString(var_entry, var[0],  "variable_entry")
        var_entry = replaceString(var_entry, var[3],  "modeling_realm")
        var_entry = replaceString(var_entry, var[14], "standard_name")
        var_entry = replaceString(var_entry, var[13], "units")
        var_entry = replaceString(var_entry, var[11], "cell_methods")
        var_entry = replaceString(var_entry, var[12], "cell_measure")
        var_entry = replaceString(var_entry, var[17], "long_name")
        var_entry = replaceString(var_entry, var[16].replace('"', '\''), "comment")
        var_entry = replaceString(var_entry, var[6],  "positive")
        var_entry = replaceString(var_entry, var[8],  "valid_min")
        var_entry = replaceString(var_entry, var[7],  "valid_max")
        var_entry = replaceString(var_entry, var[5],  "ok_min_mean_abs")
        var_entry = replaceString(var_entry, var[4],  "ok_max_mean_abs")

        var_entry = var_entry.replace("<dimensions>",
                                      (var[9].replace("|", " ") + " " +
                                          var[10].replace("|", " ")).strip(" "))
        var_entry = var_entry.replace("<outname>", var[0])
        var_entry = var_entry.replace("<type>", var[15])
    if(bJSON):
        var_entry = var_entry + "\"Dummy\":   \"\"\n }"
    return var_entry


# ==============================================================
#              createExptIDs()
# ==============================================================
def createExptIDs(bJSON=True):
    """
    return a string containing all experiments
    """
    experiments = cursor.getAllExperiment()
    if(bJSON):
        expt_ids = """\"experiments\": {\n"""
        for expt in experiments:
            expt_ids = expt_ids + "\"" + expt[1] + "\":" + "  \"" + expt[2].replace('"', '\'') + "\",\n"
            expt_ids = expt_ids + "\"Dummy\":" + "\"\"\n"
        expt_ids = expt_ids + """}"""
    else:
        expt_ids = ""
        for expt in experiments:
            expt_ids = expt_ids + """expt_id_ok: '""" + expt[2] + """' '""" + expt[1] + """'\n"""
    return expt_ids


# ==============================================================
#                     main()
# ==============================================================
def main(argv):
    """
    """
    global vars, varSQL
    realm = "Amon"
    bJSON = False
    expt = False
    try:
        opts, args = getopt.getopt(argv, "hr:je", ["realm=", "JSON", "expt"])
        if(not opts):
            print 'CMORCreateTable.py [-r <realm> | -e ] -j'
            sys.exit(2)
    except getopt.GetoptError:
        print 'CMORCreateTable.py [-r <realm> | -e ] -j'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'CMORCreateTable.py [-r <realm> | -e ] -j'
            sys.exit()
        elif opt in ("-r", "--realm"):
            realm = arg
        elif opt in ("-j", "--JSON"):
            bJSON = True
        elif opt in ("-e", "--expt"):
            expt = True

    # -------------------------------------------------------------
    #  Create grids and exit
    # -------------------------------------------------------------
    if realm == "grids":
        createGrids()
        return 0

    # -------------------------------------------------------------
    #  Create all other tables
    # -------------------------------------------------------------
    vars = cursor.getVarFromMipTable(realm, 'MIP')
    varSQL = [vars[i] for i in range(len(vars))]

    if(not varSQL):
        print "no Variable found for " + realm
        return -1

    Header            = createHeader(realm, bJSON=bJSON)
    experiments       = createExptIDs(bJSON=bJSON)
    axis_entry        = createAxes(bJSON=bJSON)
    formula_var_entry = createFormulaVar(bJSON=bJSON)
    variable_entry    = createVariables(bJSON=bJSON)
    Footer            = createFooter(bJSON=bJSON)

    if(bJSON):
        if(expt):
            CMIP6Table = (json.loads("{" + "".join(experiments) + "}"))
            if("Dummy" in CMIP6Table['experiments']):
                del CMIP6Table['experiments']['Dummy']
            print(json.dumps(CMIP6Table, indent=4))
        else:
            CMIP6Table = (json.loads("".join(Header + axis_entry + formula_var_entry +
                                                variable_entry + Footer)))
            if("Dummy" in CMIP6Table['axis_entry']):
                del CMIP6Table['axis_entry']['Dummy']
            if("Dummy" in CMIP6Table['variable_entry']):
                del CMIP6Table['variable_entry']['Dummy']
            print(json.dumps(CMIP6Table, indent=4))
    else:
        print Header
        print experiments
        print axis_entry
        print variable_entry
        print Footer

if __name__ == "__main__":
    main(sys.argv[1:])
