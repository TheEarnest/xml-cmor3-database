# ==================
# JSON Template
# ==================
HeaderJSON = """
{
    "Header":{
                    "table_id": "Table <table>",
                    "modeling_realm": "<modeling_realm>",
                    "frequency":    "<frequency>",
                    "cmor_version": "<cmorVersion>",
                    "cf_version":   "<cfVersion>",
                    "project_id":   "<projectID>",
                    "table_date":   "<tableDate>",
                    "missing_value": "<missingValue>",
                    "baseURL": "http://cmip-pcmdi.llnl.gov/CMIP6/dataLocation",
                    "product": "output",
                    "required_global_attributes": [ "creation_date",
                                                    "tracking_id",
                                                    "forcing",
                                                    "model_id",
                                                    "parent_experiment_id",
                                                    "parent_experiment_rip",
                                                    "branch_time",
                                                    "contact",
                                                    "institute_id" 
                                                  ],
                    "forcings":   "N/A Nat Ant GHG SD SI SA TO SO Oz LU Sl Vl SS Ds BC MD OC AA",
                    "approx_interval":  "<approxInterval>",
                    "generic_levels":   "<generic_levels>"
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
              "Omon": { "approxInterval" : "30.00000",
                        "genericLevels"  : "olevel",
                        "frequency"      : "mon"
                      },
              "OImon": { "approxInterval" : "30.00000",
                        "genericLevels"  : "olevel",
                        "frequency"      : "monClim"
                      },
              "OImon": { "approxInterval" : "30.00000",
                        "genericLevels"  : "",
                        "frequency"      : "mon"
                      },
              "Oyr": { "approxInterval" : "365.00000",
                        "genericLevels"  : "olevel",
                        "frequency"      : "yr"
                      },
              "day":  { "approxInterval" : "1.00000",
                        "genericLevels"  : "",
                        "frequency"      : "day"
                      },
              "3hr":  { "approxInterval" : "0.125000",
                        "genericLevels"  : "",
                        "frequency"      : "3hr"
                      },
              "6hr":  { "approxInterval" : "0.250000",
                        "genericLevels"  : "alevel",
                        "frequency"      : "3hr"
                      },
             "subhr": { "approxInterval" : "0.017361",
                        "genericLevels"  : "alevel alevhalf",
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
project_id:   "<projectID>"    # project id
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


