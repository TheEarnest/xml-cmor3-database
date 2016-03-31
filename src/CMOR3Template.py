# ==================
# JSON Template
# ==================
HeaderJSON = """
{
    "Header":{
                    "data_spec_version": "<data_spec_version>",
                    "table_id":         "Table <table>",
                    "realm":            "<modeling_realm>",
                    "frequency":        "<frequency>",
                    "cmor_version":     "<cmorVersion>",
                    "cf_version":       "<cfVersion>",
                    "activity_id":      "<activityID>-XXXX",
                    "table_date":       "<tableDate>",
                    "missing_value":    "<missingValue>",
                    "product":          "output",
                    "approx_interval":  "<approxInterval>",
                    <DUMMYENTRY>
                    "generic_levels":   "<generic_levels>",
                    "Conventions":      "CF-1.8 CMIP-6.0"
              },
"""

axisTemplateJSON = """
"<axis_entry>": {
                    "standard_name":    "<standard_name>",
                    "units":            "<units>",
                    "axis":             "<axis>",
                    "long_name":        "<long_name>",
                    "climatology":      "<climatology>",
                    "formula":          "<formula>",
                    "must_have_bounds": "<must_have_bounds>",
                    "out_name":         "<out_name>",
                    "positive":         "<positive>",
                    "requested":        <requested>,
                    "requested_bounds": <requested_bounds>,
                    "stored_direction":  "<stored_direction>",
                    "tolerance":        "<tolerance>",
                    "type":             "<type>",
                    "valid_max":        "<valid_max>",
                    "valid_min":        "<valid_min>",
                    "value":             "<value>",
                    "z_bounds_factors": "<z_bounds_factors>",
                    "z_factors":        "<z_factors>"
                },
"""
FormulaVarTemplateJSON = """
"<variable_entry>": {
                        "long_name":   "<long_name>",
                        "units":       "<units>",
                        "dimensions":  "<dimensions>",
                        "type":        "<type>"
                    },
"""

VarTemplateJSON = """
"<variable_entry>": {
                        "modeling_realm":    "<modeling_realm>",
                        "standard_name":     "<standard_name>",
                        "units":             "<units>",
                        "cell_methods":      "<cell_methods>",
                        "cell_measures":     "<cell_measure>",
                        "long_name":         "<long_name>",
                        "comment":           "<comment>",
                        "dimensions":        "<dimensions>",
                        "out_name":          "<outname>",
                        "type":              "<type>",
                        "positive":          "<positive>",
                        "valid_min":         "<valid_min>",
                        "valid_max":         "<valid_max>",
                        "ok_min_mean_abs":   "<ok_min_mean_abs>",
                        "ok_max_mean_abs":   "<ok_max_mean_abs>"
},
"""


GridHeaderJSON = """
{
    "Header":{
                "table_id": "Table grids",
                "cmor_version":  "<cmorVersion>",
                "cf_version":    "<cfVersion>",
                "activity_id":    "<activityID>",
                "table_date":    "<tableDate>",
                "missing_value": "<missingValue>",
                "baseURL": "http://cmip-pcmdi.llnl.gov/CMIP6/dataLocation",
                "product": "output"
             },

    "mapping_entry": {
                "sample_user_mapping": {
                            "parameter1": "false_easting",
                            "parameter2": "false_northing",
                            "coordinates": "rlon rlat"
                                       }
             },
"""

GridVarTemplateJSON = """
"<grid_variable_entry>": {
                        "standard_name":     "<standard_name>",
                        "units":             "<units>",
                        "long_name":         "<long_name>",
                        "dimensions":        "<dimensions>",
                        "out_name":          "<out_name>",
                        "valid_min":         "<valid_min>",
                        "valid_max":         "<valid_max>"
                         },
"""
GridAxisTemplateJSON = """
"<grid_axis_entry>": {
                    "standard_name":    "<standard_name>",
                    "units":            "<units>",
                    "axis":             "<axis>",
                    "long_name":        "<long_name>",
                    "out_name":         "<out_name>",
                    "type":             "<type>"
                },
"""


FooterTemplateJSON="""
}
"""
# ==================
#  Header information
# ==================
tableDict = { "Amon": { "approxInterval" : "30.00000", 
                        "genericLevels"  : "alevel alevhalf",
                        "frequency"      : "mon"
                      },
              "Lmon": { "approxInterval" : "30.00000",
                        "genericLevels"  : "",
                        "frequency"      : "mon"
                      },
              "LImon": { "approxInterval" : "30.00000",
                        "genericLevels"  : "",
                        "frequency"      : "mon"
                      },
              "cfMon": { "approxInterval" : "30.00000",
                        "genericLevels"  : "olevel",
                        "frequency"      : "mon"
                      },
              "Omon": { "approxInterval" : "30.00000",
                        "genericLevels"  : "olevel",
                        "frequency"      : "mon"
                      },
              "SImon": { "approxInterval" : "30.00000",
                        "genericLevels"  : "",
                        "frequency"      : "mon"
                      },
              "aero": { "approxInterval" : "30.00000",
                        "genericLevels"  : "alevel alev1",
                        "frequency"      : "mon"
                      },
              "Oclim": { "approxInterval" : "30.00000",
                        "genericLevels"  : "olevel",
                        "frequency"      : "monClim"
                      },
              "Oyr": { "approxInterval" : "365.00000",
                        "genericLevels"  : "olevel",
                        "frequency"      : "yr"
                      },
              "SIday":  { "approxInterval" : "1.00000",
                        "genericLevels"  : "",
                        "frequency"      : "day"
                      },
              "Oday":  { "approxInterval" : "1.00000",
                        "genericLevels"  : "",
                        "frequency"      : "day"
                      },
              "cfDay":  { "approxInterval" : "1.00000",
                        "genericLevels"  : "alevel alevhalf",
                        "frequency"      : "day"
                      },
              "day":  { "approxInterval" : "1.00000",
                        "genericLevels"  : "",
                        "frequency"      : "day"
                      },
              "cf3hr":  { "approxInterval" : "0.125000",
                        "genericLevels"  : "",
                        "frequency"      : "3hr"
                      },
              "3hr":  { "approxInterval" : "0.125000",
                        "genericLevels"  : "",
                        "frequency"      : "3hr"
                      },
              "6hrLev":  { "approxInterval" : "0.250000",
                        "genericLevels"  : "alevel",
                        "frequency"      : "3hr"
                      },
              "6hrPlev":  { "approxInterval" : "0.250000",
                        "genericLevels"  : "",
                        "frequency"      : "3hr"
                      },
              "subhr": { "approxInterval" : "0.017361",
                        "genericLevels"  : "alevel alevhalf",
                        "frequency"      : "subhr"
                      },
              "cfsites": { "approxInterval" : "0.017361",
                           "genericLevels"  : "alevel alevhalf",
                           "approxIntervalWarning":  "0.25",
                           "approxIntervalError":  "0.75",
                           "frequency"      : "subhr"
                      },
              "fx": { "approxInterval" : "0.00000",
                        "genericLevels"  : "olevel",
                        "frequency"      : "fx"
                      }

             }

# ==================
#  Old CMOR2 format
# ==================
Header = """
table_id: "Table <table>"
modeling_realm: "<modeling_realm>"

frequency:  "<frequency>"

cmor_version: <cmorVersion>  # minimum version of CMOR that can read this table
cf_version:   <cfVersion>    # version of CF that output conforms to
activity_id:   "<activityID>"    # project id
table_date:   "<tableDate>"   # date this table was constructed

missing_value: <missingValue>    # value used to indicate a missing value
                                 #   in arrays output by netCDF as 32-bit IEEE
                                 #   floating-point numbers (float or real)

baseURL: "http://cmip-pcmdi.llnl.gov/CMIP6/dataLocation"
product: "output"

# space separated required global attribute

required_global_attributes: [ "creation_date","tracking_id","forcing","model_id","parent_experiment_id","parent_experiment_rip","branch_time","contact","institute_id" ]    

forcings:   "N/A Nat Ant GHG SD SI SA TO SO Oz LU Sl Vl SS Ds BC MD OC AA"

approx_interval:  <approxInterval> # approximate spacing between successive time
                          #   samples (in units of the output time
                          #   coordinate.select distinct mip,label,description from experiment order by mip;

generic_levels:   "<generic_levels>";
"""
# ==================
axisTemplate = """
!===============
axis_entry: <axis_entry>
!===============

!----------------------------------
! Axis attributes:
!----------------------------------
standard_name:    <standard_name>
units:            <units>
axis:             <axis>
long_name:        <long_name>
!----------------------------------
! Additional axis information:
!----------------------------------
climatology:      <climatology>
formula:          <formula>
must_have_bounds: <must_have_bounds>
out_name:         <out_name>
positive:         <positive>
requested:        <requested>
requested_bounds: <requested_bounds>
stored_direction: <stored_direction>
tolerance:        <tolerance>
type:             <type>
valid_max:        <valid_max>
valid_min:        <valid_min>
value:            <value>
z_bounds_factors: <z_bounds_factors>
z_factors:        <z_factors>
"""


FormulaVarTemplate = """
!===============
variable_entry: <variable_entry>
!===============

!----------------------------------
! Variable attributes:
!----------------------------------
long_name:   <long_name>
units:       <units>
!----------------------------------
! Additional variable information:
!----------------------------------
dimensions:  <dimensions>
type:        <type>
!----------------------------------
"""

VarTemplate = """
!===============
variable_entry:  <variable_entry>
!===============

modeling_realm:    <modeling_realm>
!----------------------------------
! Variable attributes:
!----------------------------------
standard_name:     <standard_name>
units:             <units>
cell_methods:      <cell_methods>
cell_measures:     <cell_measure>
long_name:         <long_name>
comment:           <comment>
!----------------------------------
! Additional variable information:
!----------------------------------
dimensions:        <dimensions>
out_name:          <outname>
type:              <type>
positive:          <positive>
valid_min:         <valid_min>
valid_max:         <valid_max>
ok_min_mean_abs:   <ok_min_mean_abs>
ok_max_mean_abs:   <ok_max_mean_abs>
"""


