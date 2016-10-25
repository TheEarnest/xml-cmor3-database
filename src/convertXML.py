#!/bin/env python

# sqlite> select DISTINCT vg.label from requestVar vg, requestVarGroup rvg, requestItem ri, requestLink rl where  ri.mip="GeoMIP" and ri.rlid==rl.uid and rl.refid=rvg.uid and vg.vid=rvg.uid;
import sqlite3
import xml.etree.ElementTree as ET
import pylibconfig2 as cfg
import uuid
import sys
import pdb
# https://github.com/heinzK1X/pylibconfig2


conn = sqlite3.connect('./CMIP6.sql3')
conn.isolation_level = None
c = conn.cursor()
c.execute("""drop table if exists var;""")
c.execute("""drop table if exists CMORvar""")
c.execute("""drop table if exists structure""")
c.execute("""drop table if exists spatialShape""")
c.execute("""drop table if exists temporalShape""")
c.execute("""drop table if exists requestVar""")
c.execute("""drop table if exists requestVarGroup""")
c.execute("""drop table if exists requestLink""")
c.execute("""drop table if exists requestItem""")
c.execute("""drop table if exists experiment""")
c.execute("""drop table if exists exptgroup""")
c.execute("""drop table if exists MIP""")
c.execute("""drop table if exists axisEntry""")
c.execute("""drop table if exists expIDs""")
c.execute("""drop table if exists formulaVar""")
c.execute("""drop table if exists vocab_institute""")
c.execute("""drop table if exists vocab_model""")
c.execute("""drop table if exists vocab_activity""")
c.execute("""drop table if exists vocab_frequency""")
c.execute("""drop table if exists vocab_realm""")
c.execute("""drop table if exists vocab_grid""")
c.execute("""drop table if exists grid""")

print "Create Tables"

c.execute("""create table formulaVar (
        name      text,
        long_name text,
        type      text,
        dimension text,
        units      text)""")

c.execute("""create table var (
        description text,
        id text,
        label text,
        procComment text,
        procNote text,
        prov text,
        sn text,
        title text,
        uid text primary key not NULL ,
        units text)""")

c.execute(""" create table CMORvar (
        deflate text,
        deflate_level text,
        description text,
        frequency text,
        label text,
        mipTable text,
        modeling_realm text,
        ok_max_mean_abs text,
        ok_min_mean_abs text,
        positive text,
        prov text,
        provNote text,
        rowIndex text,
        shuffle text,
        stid text,
        title text,
        type text,
        uid text,
        valid_max text,
        valid_min text,
        vid text)""")

c.execute(""" create table structure (
    cell_measures text,
    cell_methods text,
    coords text,
    description text,
    flag_meanings text,
    flag_values text,
    label text,
    odims text,
    procNote text,
    prov text,
    spid text,
    tmid text,
    uid text)""")

c.execute(""" create table spatialShape (
    dimensions text,
    label text,
    levelFlag text,
    levels text,
    title text,
    uid text)""")

c.execute(""" create table temporalShape (
    dimensions text,
    label text,
    title text,
    uid text)""")

# c.execute(""" create table denis (label text, mip text, priority text, table text,
# title text, uid text, vgid text, vid text)""")

c.execute(""" create table requestVarGroup (
    label text,
    mip text,
    ref text,
    refNote text,
    title text,
    uid text)""")


c.execute(""" create table requestVar (
        label text,
        mip text,
        priority text,
        tables text,
        title text,
        uid text,
        vgid text,
        vid text )""")

c.execute(""" create table requestLink (
    comment text,
    grid text,
    gridreq text,
    mip text,
    objective text,
    opar text,
    opt text,
    preset text,
    ref text,
    refNote text,
    refid text,
    tab text,
    title text,
    uid text)""")

c.execute(""" create table requestItem (
        comment text,
    esid text,
    esidComment text,
    expt text,
    label text,
    mip text,
    nenmax text,
    nexmax text,
    ny text,
    nymax text,
    rlid text,
    tab text,
    title text,
    uid text)""")

c.execute(""" create table experiment (
    comment text,
    description text,
    egid text,
    endy text,
    ensz text,
    label text,
    mcfg text,
    mip text,
    nstart text,
    ntot text,
    starty text,
    tier text,
    uid text,
    yps text)""")

c.execute(""" create table exptgroup (
    label text,
    ntot text,
    tierMin text,
    uid text)""")

c.execute(""" create table MIP (
        label text,
        status text,
        title text,
        uid text,
        url text)""")


c.execute(""" create table axisEntry (
    name text,
    axis text,
    climatology text,
    formula text,
    long_name text,
    must_have_bounds text,
    out_name text,
    positive text,
    requested text,
    requested_bounds text,
    standard_name text,
    stored_direction text,
    tolerance text,
    type text,
    units text,
    valid_max text,
    valid_min text,
    value text,
    z_bounds_factors text,
    z_factors text,
    bounds_values text,
    origin text)""")

c.execute(""" create table expIDs (
    id text,
        title text)""")

c.execute(""" create table vocab_institute (
    description text,
    id text,
    isni text,
    label text,
    title text,
    url text,
    uuid text)""")

c.execute(""" create table vocab_model (
    description text,
    id text,
    label text,
    title text,
    uuid text)""")

c.execute(""" create table vocab_activity (
    id text,
    label text,
    status text,
    title text,
    url text,
    uuid text)""")

c.execute(""" create table vocab_frequency (
    id text,
    iso text,
    label text,
    title text,
    uuid text)""")

c.execute(""" create table vocab_realm (
    id text,
    label text,
    title text,
    uuid text)""")

c.execute(""" create table vocab_grid (
    id text,
    label text,
    title text,
    uuid text)""")

c.execute(""" create table grid (
    altLabel text,
    axis text,
    bounds text,
    boundsRequested text,
    boundsValues text,
    coords text,
    description text,
    direction text,
    isGrid text,
    isIndex text,
    label text,
    positive text,
    requested text,
    standardName text,
    tables text,
    title text,
    tolRequested text,
    type text,
    uid text,
    units text,
    value text
)""")


print "----------------------"
print "reading file vocab.xml"
print "----------------------"
# -----------------------------------
# Read in dreq.xml and set namespace
# -----------------------------------
contentDoc = ET.parse("../docs/vocab.xml")
root = contentDoc.getroot()
print "Create institute"
institute = root.findall('./institute')[0]
c.execute("begin")
for child in institute.getchildren():
        description = child.get('description').replace("'", "\"") or ""
        iid = child.get('id') or ""
        isni = child.get('isni') or ""
        label = child.get('label') or ""
        title = child.get('title') or ""
        url = child.get('url') or ""
        uid = child.get('uuid') or ""
        cmd = """ insert into vocab_institute values (""" + \
             "'" + description + "'" + """, """ + \
             "'" + iid         + "'" + """, """ + \
             "'" + isni        + "'" + """, """ + \
             "'" + label       + "'" + """, """ + \
             "'" + title       + "'" + """, """ + \
             "'" + url         + "'" + """, """ + \
             "'" + uid.replace('\'','')        + "'" + """) """
        c.execute(cmd)
institute = ""
conn.execute("commit")

print "Create model"

model = root.findall('./model')[0]
c.execute("begin")
for child in model.getchildren():
        description = child.get('description').replace("'", "\"") or ""
        mid         = child.get('id') or ""
        label       = child.get('label') or ""
        title       = child.get('title') or ""
        uid         = child.get('uuid') or ""
        cmd = """ insert into vocab_model values (""" + \
             "'" + description + "'" + """, """ + \
             "'" + mid         + "'" + """, """ + \
             "'" + label       + "'" + """, """ + \
             "'" + title       + "'" + """, """ + \
             "'" + uid.replace('\'','')         + "'" + """) """
        c.execute(cmd)
model = ""

print "Create activity"
activity = root.findall('./activity')[0]
for child in activity.getchildren():
        aid         = child.get('id') or ""
        label       = child.get('label') or ""
        status      = child.get('status') or ""
        title       = child.get('title') or ""
        url         = child.get('url') or ""
        uid         = child.get('uuid') or ""
        cmd = """ insert into vocab_activity values (""" + \
             "'" + aid       + "'" + """, """ + \
             "'" + label     + "'" + """, """ + \
             "'" + status    + "'" + """, """ + \
             "'" + title     + "'" + """, """ + \
             "'" + url       + "'" + """, """ + \
             "'" + uid.replace('\'','')       + "'" + """) """
        c.execute(cmd)
activity = ""

print "Create frequency"
frequency = root.findall('./frequency')[0]
for child in frequency.getchildren():
        fid         = child.get('id') or ""
        iso       = child.get('iso') or ""
        label      = child.get('label') or ""
        title      = child.get('title') or ""
        uid         = child.get('uuid') or ""
        cmd = """ insert into vocab_frequency values (""" + \
             "'" + fid       + "'" + """, """ + \
             "'" + iso       + "'" + """, """ + \
             "'" + label     + "'" + """, """ + \
             "'" + title     + "'" + """, """ + \
             "'" + uid.replace('\'','')       + "'" + """) """
        c.execute(cmd)
frequency = ""

print "Create realm"
realm = root.findall('./realm')[0]
for child in realm.getchildren():
        rid         = child.get('id') or ""
        label       = child.get('label') or ""
        title       = child.get('title') or ""
        uid         = child.get('uuid') or ""
        cmd = """ insert into vocab_realm values (""" + \
             "'" + rid       + "'" + """, """ + \
             "'" + label     + "'" + """, """ + \
             "'" + title     + "'" + """, """ + \
             "'" + uid.replace('\'','')       + "'" + """) """
        c.execute(cmd)
realm = ""


print "Create grid"
grid = root.findall('./grid')[0]
for child in grid.getchildren():
        gid         = child.get('id') or ""
        label      = child.get('label') or ""
        title      = child.get('title') or ""
        uid         = child.get('uuid') or ""
        cmd = """ insert into vocab_grid values (""" + \
             "'" + gid       + "'" + """, """ + \
             "'" + label     + "'" + """, """ + \
             "'" + title     + "'" + """, """ + \
             "'" + uid.replace('\'','')       + "'" + """) """
        c.execute(cmd)
grid = ""
conn.execute("commit")
# -----------------------------------
# Read in dreq.xml and set namespace
# -----------------------------------
print "----------------------"
print "reading file dreq.xml"
print "----------------------"

contentDoc = ET.parse("../docs/dreq.xml")
root = contentDoc.getroot()
namespace = '{urn:w3id.org:cmip6.dreq.dreq:a}'

# *********************************************************************
# Create first shot of axes from Martin's table.  If axes are missing,
# they will be created by reading CMIP5 tables
# *********************************************************************
axes = root.findall('./{0}main/{0}grids'.format(namespace))[0]
print "Create Martin's dreq.xml axes"
c.execute("begin")
for child in axes.getchildren():
    name               = child.get('label') or ""
    if name in ['alevel', 'olevel', 'alevhalf' ]:
        continue
    if name == 'sdepth1':
        pdb.set_trace()
    caxis              = child.get('axis') or ""
    long_name          = child.get('title') or ""
    must_have_bounds   = child.get('bounds') or ""
    out_name           = child.get('altLabel') or ""
    positive           = child.get('positive') or ""

    if child.get('boundsRequested'):
        requested_bounds = str([str(x) for x in child.get('boundsRequested').split()] )
    else:
        requested_bounds = ""

    if child.get('requested'):
        try:
            requested  = str([str(x) for x in child.get('requested').split()])
        except:
            try:
                requested  = str([str(x) for x in child.get('requested').split()])
            except:
                sys.exit(1)
    else:
        requested  = ""

    if child.get('boundsValues'):
        bounds_values = str([float(x) for x in child.get('boundsValues').split()] )
        # convert list into string of values
        # -----------------------------------
        bounds_values = " ".join(str(value) for value in eval(bounds_values))
    else:
        bounds_values = ""

    standard_name      = child.get('standardName') or ""
    stored_direction   = child.get('direction') or ""
    ctype              = child.get('type') or ""
    units              = child.get('units') or ""
    valid_max          = child.get('valid_max') or ""
    valid_min          = child.get('valid_min') or ""
    value              = child.get('value') or ""
    tolerance          = ""
    z_bounds_factors   = ""
    z_factors          = ""
    climatology        = ""
    formula            = ""
                        
    cmd = """select name from axisEntry where name = '""" + str(name).strip() + "';"
    c.execute(cmd)
    results = c.fetchall()
    if not results:
        cmd = """insert into axisEntry values (""" + \
              "'" + str(name)              + "'" + """, """ \
              "'" + str(caxis)             + "'" + """, """ \
              "'" + str(climatology)       + "'" + """, """ \
              "'" + str(formula)           + "'" + """, """ \
              "'" + str(long_name)         + "'" + """, """ \
              "'" + str(must_have_bounds)  + "'" + """, """ \
              "'" + str(out_name)          + "'" + """, """ \
              "'" + str(positive)          + "'" + """, """ \
              "'" + str(requested).replace("'","\"")        + "'" + """, """ \
              "'" + str(requested_bounds).replace("'", "\"")  + "'" + """, """ \
              "'" + str(standard_name)     + "'" + """, """ \
              "'" + str(stored_direction)  + "'" + """, """ \
              "'" + str(tolerance)         + "'" + """, """ \
              "'" + str(ctype)             + "'" + """, """ \
              "'" + str(units)             + "'" + """, """ \
              "'" + str(valid_max)         + "'" + """, """ \
              "'" + str(valid_min)         + "'" + """, """ \
              "'" + str(value)             + "'" + """, """ \
              "'" + str(z_bounds_factors)  + "'" + """, """ \
              "'" + str(z_factors)         + "'" + """, """ \
              "'" + str(bounds_values)     + "'" + """, """ \
              "'" + "XML"                  + "'" + """) """
        c.execute(cmd)
axes=""
c.execute("commit")

print "Create grid"

grid = root.findall('./{0}main/{0}grids'.format(namespace))[0]
c.execute("begin")
for child in grid.getchildren():
        altLabel              = child.get('altLabel') or ""
        axis                  = child.get('axis') or ""             
        bounds                = child.get('bounds') or ""

        if child.get('boundsRequested'):
            boundsRequested   = str([float(x) for x in child.get('boundsRequested').split()] )
        else:
            boundsRequested   = ""

        if child.get('boundsValues'):
            boundsValues  = str([float(x) for x in child.get('boundsValues').split()] )
        else:
            boundsValues  = ""
        coords                = child.get('coords') or ""
        description           = child.get('description').replace("'","\"") or ""
        direction             = child.get('direction') or ""
        isGrid                = child.get('isGrid') or ""
        isIndex               = child.get('isIndex') or ""
        label                 = child.get('label') or ""
        positive              = child.get('positive') or ""
        requested  = ""
        if child.get('requested'):
            try:
                requested  = str([float(x) for x in child.get('requested').split()])
            except:
                try:
                    requested  = str([float(x) for x in child.get('requested').split()])
                except:
                    requested  = ""
        standardName          = child.get('standardName') or ""
        tables                = child.get('tables') or ""
        title                 = child.get('title') or ""
        tolRequested          = child.get('tolRequested') or ""
        itype                 = child.get('type') or ""
        uid                   = child.get('uid') or ""
        units                 = child.get('units') or ""
        value                 = child.get('value') or ""

        cmd = """ insert into grid values (""" + \
             "'" + altLabel        + "'" + """, """ + \
             "'" + axis            + "'" + """, """ + \
             "'" + bounds          + "'" + """, """ + \
             "'" + boundsRequested + "'" + """, """ + \
             "'" + boundsValues    + "'" + """, """ + \
             "'" + coords          + "'" + """, """ + \
             "'" + description     + "'" + """, """ + \
             "'" + direction       + "'" + """, """ + \
             "'" + isGrid          + "'" + """, """ + \
             "'" + isIndex         + "'" + """, """ + \
             "'" + label           + "'" + """, """ + \
             "'" + positive        + "'" + """, """ + \
             "'" + requested       + "'" + """, """ + \
             "'" + standardName    + "'" + """, """ + \
             "'" + tables          + "'" + """, """ + \
             "'" + title           + "'" + """, """ + \
             "'" + tolRequested    + "'" + """, """ + \
             "'" + itype           + "'" + """, """ + \
             "'" + uid.replace('\'','')             + "'" + """, """ + \
             "'" + units           + "'" + """, """ + \
             "'" + value + "'" + """) """
        c.execute(cmd)
grid = ""


var = root.findall('./{0}main/{0}var'.format(namespace))[0]
print "Create var"
for child in var.getchildren():
    description = child.get('description').replace("'", "\"")  or ""
    vid         = child.get('id').replace('\'','')           or ""
    label       = child.get('label')        or ""
    proComment  = child.get('proComment')   or ""
    proNote     = child.get('pronote')      or ""
    prov        = child.get('prov')         or ""
    sn          = child.get('sn')           or ""
    title       = child.get('title').replace("'", "\"")        or ""
    uid         = child.get('uid').replace('\'','')          or ""
    units       = child.get('units')        or ""

    cmd = """insert into var values (""" + \
         "'" + description + "'" + """, """ + \
         "'" + vid         + "'" + """, """ + \
         "'" + label       + "'" + """, """ + \
         "'" + proComment  + "'" + """, """ + \
         "'" + proNote     + "'" + """, """ + \
         "'" + prov        + "'" + """, """ + \
         "'" + sn          + "'" + """, """ + \
         "'" + title       + "'" + """, """ + \
         "'" + uid.replace('\'','')         + "'" + """, """ + \
         "'" + units       + "'" + """) """

    c.execute(cmd)
var = ""

# ----------------------------------
#  Insert CMORvar in the database
# ----------------------------------
CMORvar = root.findall('./{0}main/{0}CMORvar'.format(namespace))[0]

print "Create CMORvar"

for child in CMORvar.getchildren():
    defaultPriority = child.get('defaultPriority') or ""
    deflate         = child.get('deflate')         or ""
    deflate_level   = child.get('deflate_level')   or ""
    description     = child.get('description')     or ""
    frequency       = child.get('frequency')       or ""
    label           = child.get('label')           or ""
    mipTable        = child.get('mipTable')        or ""
    modeling_realm  = child.get('modeling_realm')  or ""
    ok_max_mean_abs = child.get('ok_max_mean_abs') or ""
    ok_min_mean_abs = child.get('ok_min_mean_abs') or ""
    positive        = child.get('positive')        or ""
    prov            = child.get('prov')            or ""
    provNote        = child.get('provNote')        or ""
    rowIndex        = child.get('rowIndex')        or ""
    shuffle         = child.get('shuffle')         or ""
    stid            = child.get('stid')            or ""
    title           = child.get('title')           or ""
    vtype           = child.get('type')            or ""
    uid             = child.get('uid').replace('\'','')             or ""
    valid_max       = child.get('valid_max')       or ""
    valid_min       = child.get('valid_min')       or ""
    vid             = child.get('vid').replace('\'','')             or ""

    defaultPriority = defaultPriority.replace('None', '')
    deflate         = deflate.replace('None', '')
    deflate_level   = deflate_level.replace('None', '')
    description     = description.replace('None', '')
    frequency       = frequency.replace('None', '')
    label           = label.replace('None', '')
    mipTable        = mipTable.replace('None', '')
    modeling_realm  = modeling_realm.replace('None', '')
    ok_max_mean_abs = ok_max_mean_abs.replace('None', '')
    ok_min_mean_abs = ok_min_mean_abs.replace('None', '')
    positive        = positive.replace('None', '')
    prov            = prov.replace('None', '')
    provNote        = provNote.replace('None', '')
    rowIndex        = rowIndex.replace('None', '')
    shuffle         = shuffle.replace('None', '')
    stid            = stid.replace('None', '')
    title           = title.replace('None', '')
    title           = title.replace('\'', '')
    vtype           = vtype.replace('None', '')
    uid             = uid.replace('None', '')
    valid_max       = valid_max.replace('None', '')
    valid_min       = valid_min.replace('None', '')
    vid             = vid.replace('None', '')

    cmd = """insert into CMORvar values (""" + \
         "'" + deflate         + "'" + """, """ + \
         "'" + deflate_level   + "'" + """, """ + \
         "'" + description.replace("'", "\"")     + "'" + """, """ + \
         "'" + frequency       + "'" + """, """ + \
         "'" + label           + "'" + """, """ + \
         "'" + mipTable        + "'" + """, """ + \
         "'" + modeling_realm  + "'" + """, """ + \
         "'" + ok_max_mean_abs + "'" + """, """ + \
         "'" + ok_min_mean_abs + "'" + """, """ + \
         "'" + positive        + "'" + """, """ + \
         "'" + prov            + "'" + """, """ + \
         "'" + provNote        + "'" + """, """ + \
         "'" + rowIndex        + "'" + """, """ + \
         "'" + shuffle         + "'" + """, """ + \
         "'" + stid            + "'" + """, """ + \
         "'" + title           + "'" + """, """ + \
         "'" + vtype           + "'" + """, """ + \
         "'" + uid.replace('\'','')             + "'" + """, """ + \
         "'" + valid_max       + "'" + """, """ + \
         "'" + valid_min       + "'" + """, """ + \
         "'" + vid.replace('\'','')            + "'" + """) """

    c.execute(cmd)
CMORvar = ""

# ----------------------------------
#  Insert structure in the database
# ----------------------------------
structure = root.findall('./{0}main/{0}structure'.format(namespace))[0]
print "Create structure"
for child in structure.getchildren():
    cell_measures   = child.get('cell_measures').replace('None', '')   or ""
    cell_methods    = child.get('cell_methods').replace('None', '')    or ""
    coords          = child.get('coords').replace('None', '')          or ""
    description     = child.get('description').replace('None', '')     or ""
    flag_meanings   = child.get('flag_meanings').replace('None', '')   or ""
    flag_values     = child.get('flag_values').replace('None', '')     or ""
    label           = child.get('label').replace('None', '')           or ""
    odims           = child.get('odims').replace('None', '')           or ""
    procNote        = child.get('procNote').replace('None', '')        or ""
    prov            = child.get('prov').replace('None', '')            or ""
    spid            = child.get('spid').replace('None', '')            or ""
    tmid            = child.get('tmid').replace('None', '')            or ""
    uid             = child.get('uid').replace('None', '')             or ""

    cmd = """insert into structure values (""" + \
         "'" + cell_measures   + "'" + """, """ + \
         "'" + cell_methods    + "'" + """, """ + \
         "'" + coords          + "'" + """, """ + \
         "'" + description.replace("'", "\"") + "'" + """, """ + \
         "'" + flag_meanings   + "'" + """, """ + \
         "'" + flag_values     + "'" + """, """ + \
         "'" + label           + "'" + """, """ + \
         "'" + odims           + "'" + """, """ + \
         "'" + procNote        + "'" + """, """ + \
         "'" + prov            + "'" + """, """ + \
         "'" + spid            + "'" + """, """ + \
         "'" + tmid            + "'" + """, """ + \
         "'" + uid.replace('\'','')             + "'" + """) """
    c.execute(cmd)
structure = ""

# ----------------------------------
#  Insert spatialShape in the database
# ----------------------------------
spatialShape = root.findall('./{0}main/{0}spatialShape'.format(namespace))[0]
print "Create spatialShape"
for child in spatialShape.getchildren():
    dimensions       = child.get('dimensions').replace('None', '')      or ""
    label            = child.get('label').replace('None', '')           or ""
    levelFlag        = child.get('levelFlag').replace('None', '')       or ""
    levels           = child.get('levels').replace('None', '')          or ""
    title            = child.get('title').replace('None', '')           or ""
    uid              = child.get('uid'.replace('None', ''))             or ""

    cmd = """insert into spatialShape values (""" + \
                 "'" + dimensions + "'" + """, """ + \
                 "'" + label      + "'" + """, """ + \
                 "'" + levelFlag  + "'" + """, """ + \
                 "'" + levels     + "'" + """, """ + \
                 "'" + title      + "'" + """, """ + \
                 "'" + uid.replace('\'','')        + "'" + """) """
    c.execute(cmd)

spatialShape = ""
# ----------------------------------
#  Insert temporalShape in the database
# ----------------------------------
temporalShape = root.findall('./{0}main/{0}temporalShape'.format(namespace))[0]
print "Create temporalShape"
for child in temporalShape.getchildren():
    dimensions            = child.get('dimensions').replace('None', '')  or ""
    label                 = child.get('label').replace('None', '') or ""
    title                 = child.get('title').replace('None', '') or ""
    uid                   = child.get('uid').replace('None', '') or ""
    cmd = """insert into temporalShape values (""" + \
                 "'" + dimensions + "'" + """, """ + \
                 "'" + label      + "'" + """, """ + \
                 "'" + title      + "'" + """, """ + \
                 "'" + uid.replace('\'','')        + "'" + """) """
    c.execute(cmd)
temporalShape = ""

# ----------------------------------
#  Insert requestVar in the database
# ----------------------------------
requestVar = root.findall('./{0}main/{0}requestVar'.format(namespace))[0]
print "Create requestVar"
for child in requestVar.getchildren():
    label                 = child.get('label') or ""
    mip                   = child.get('mip') or ""
    priority              = child.get('priority') or ""
    tables                = child.get('tables') or ""
    title                 = child.get('title') or ""
    uid                   = child.get('uid') or ""
    vgid                  = child.get('vgid') or ""
    vid                   = child.get('vid') or ""

    cmd = """insert into requestVar values (""" + \
                 "'" + label    + "'" + """, """ + \
                 "'" + mip      + "'" + """, """ + \
                 "'" + priority + "'" + """, """ + \
                 "'" + tables   + "'" + """, """ + \
                 "'" + title    + "'" + """, """ + \
                 "'" + uid.replace('\'','')      + "'" + """, """ + \
                 "'" + vgid     + "'" + """, """ + \
                 "'" + vid.replace('\'','')      + "'" + """) """
    c.execute(cmd)
requestVar = ""

requestVarGroup = root.findall('./{0}main/{0}requestVarGroup'.format(namespace))[0]
print "Create requestVarGrouop"
for child in requestVarGroup.getchildren():
    label                 = child.get('label') or ""
    mip                   = child.get('mip') or ""
    ref                   = child.get('ref') or ""
    refNote               = child.get('refNote') or ""
    title                 = child.get('title') or ""
    uid                   = child.get('uid') or ""

    cmd = """insert into requestVarGroup values (""" + \
                 "'" + label   + "'" + """, """ + \
                 "'" + mip     + "'" + """, """ + \
                 "'" + ref     + "'" + """, """ + \
                 "'" + refNote + "'" + """, """ + \
                 "'" + title   + "'" + """, """ + \
                 "'" + uid.replace('\'','')     + "'" + """) """
    c.execute(cmd)
requestVarGroup = ""

requestLink = root.findall('./{0}main/{0}requestLink'.format(namespace))[0]
print "Create requestLink"
for child in requestLink.getchildren():
    comment            = child.get('comment') or ""
    grid               = child.get('grid') or ""
    gridreq            = child.get('gridreq') or ""
    mip                = child.get('mip') or ""
    objective          = child.get('objective') or ""
    opar               = child.get('opar') or ""
    opt                = child.get('opt') or ""
    preset             = child.get('preset') or ""
    ref                = child.get('ref') or ""
    refNote            = child.get('refNote') or ""
    refid              = child.get('refid') or ""
    tab                = child.get('tab') or ""
    title              = child.get('title') or ""
    uid                = child.get('uid') or ""

    cmd = """insert into requestLink values (""" + \
                 "'" + comment  + "'" + """, """ + \
                 "'" + grid     + "'" + """, """ + \
                 "'" + gridreq  + "'" + """, """ + \
                 "'" + mip      + "'" + """, """ + \
                 "'" + objective + "'" + """, """ + \
                 "'" + opar     + "'" + """, """ + \
                 "'" + opt      + "'" + """, """ + \
                 "'" + preset   + "'" + """, """ + \
                 "'" + ref      + "'" + """, """ + \
                 "'" + refNote  + "'" + """, """ + \
                 "'" + refid    + "'" + """, """ + \
                 "'" + tab      + "'" + """, """ + \
                 "'" + title    + "'" + """, """ + \
                 "'" + uid.replace('\'','')      + "'" + """) """
    c.execute(cmd)
requestLink = ""

requestItem = root.findall('./{0}main/{0}requestItem'.format(namespace))[0]
print "Create requestItem"
for child in requestItem.getchildren():
    comment            = child.get('comment') or ""
    esid               = child.get('esid') or ""
    esidComment        = child.get('esidComment') or ""
    expt               = child.get('expt') or ""
    label              = child.get('label') or ""
    mip                = child.get('mip') or ""
    nenmax             = child.get('nenmax') or ""
    nexmax             = child.get('nexmax') or ""
    ny                 = child.get('ny') or ""
    nymax              = child.get('nymax') or ""
    rlid               = child.get('rlid') or ""
    tab                = child.get('tab') or ""
    title              = child.get('title') or ""
    uid                = child.get('uid') or ""

    cmd = """insert into requestItem values (""" + \
                 "'" + comment.replace("'", "\"")    + "'" + """, """ + \
                 "'" + esid       + "'" + """, """ + \
                 "'" + esidComment.replace("'", "\"") + "'" + """, """ + \
                 "'" + expt       + "'" + """, """ + \
                 "'" + label      + "'" + """, """ + \
                 "'" + mip        + "'" + """, """ + \
                 "'" + nenmax     + "'" + """, """ + \
                 "'" + nexmax     + "'" + """, """ + \
                 "'" + ny         + "'" + """, """ + \
                 "'" + nymax      + "'" + """, """ + \
                 "'" + rlid       + "'" + """, """ + \
                 "'" + tab        + "'" + """, """ + \
                 "'" + title.replace("'", "\"")      + "'" + """, """ + \
                 "'" + uid.replace('\'','')        + "'" + """) """
    c.execute(cmd)
requestItem = ""

experiment = root.findall('./{0}main/{0}experiment'.format(namespace))[0]
print "Create experiment"
for child in experiment.getchildren():
    comment      = child.get('comment') or ""
    description  = child.get('description') or ""
    egid         = child.get('egid') or ""
    endy         = child.get('endy') or ""
    ensz         = child.get('ensz') or ""
    label        = child.get('label') or ""
    mcfg         = child.get('mcfg') or ""
    mip          = child.get('mip') or ""
    nstart       = child.get('nstart') or ""
    ntot         = child.get('ntot') or ""
    starty       = child.get('starty') or ""
    tier         = child.get('tier') or ""
    uid          = child.get('uid') or ""
    yps          = child.get('yps') or ""

    cmd = """insert into experiment values (""" + \
             "'" + comment.replace("'", "\"")    + "'" + """, """ + \
             "'" + description.replace("'", "\"") + "'" + """, """ + \
             "'" + egid       + "'" + """, """ + \
             "'" + endy       + "'" + """, """ + \
             "'" + ensz       + "'" + """, """ + \
             "'" + label      + "'" + """, """ + \
             "'" + mcfg       + "'" + """, """ + \
             "'" + mip        + "'" + """, """ + \
             "'" + nstart     + "'" + """, """ + \
             "'" + ntot       + "'" + """, """ + \
             "'" + starty     + "'" + """, """ + \
             "'" + tier       + "'" + """, """ + \
             "'" + uid.replace('\'','')        + "'" + """, """ + \
             "'" + yps        + "'" + """) """

    c.execute(cmd)
experiment = ""

exptgroup = root.findall('./{0}main/{0}exptgroup'.format(namespace))[0]
print "Create exptgroup"
for child in exptgroup.getchildren():
    label        = child.get('label') or ""
    ntot         = child.get('ntot') or ""
    tierMin      = child.get('tierMin') or ""
    uid          = child.get('uid') or ""
    cmd = """insert into exptgroup values (""" + \
             "'" + label    + "'" + """, """ + \
             "'" + ntot     + "'" + """, """ + \
             "'" + tierMin  + "'" + """, """ + \
             "'" + uid.replace('\'','')      + "'" + """) """
    c.execute(cmd)
exptgroup = ""
MIP = root.findall('./{0}main/{0}mip'.format(namespace))[0]
print "Create MIP"
for child in MIP.getchildren():
    label        = child.get('label') or ""
    status       = child.get('status') or ""
    title        = child.get('title') or ""
    uid          = child.get('uid') or ""
    url          = child.get('url') or ""
    cmd = """insert into MIP values (""" + \
             "'" + label  + "'" + """, """ + \
             "'" + status + "'" + """, """ + \
             "'" + title  + "'" + """, """ + \
             "'" + uid.replace('\'','')    + "'" + """, """ + \
             "'" + url    + "'" + """) """
    c.execute(cmd)

for file in ["../tables/Amon_libconfig", "CMIP5_Omon_CMOR3" ]:
    cmor2 = cfg.Config()
    cmor2.read_file(file)
    # Add formula variables
    #
    formulaVar = [key for key in cmor2.variable_entry.keys()
                   if cmor2.variable_entry.__dict__[key].long_name.find("formula") != -1]
    variables = [key for key in cmor2.axis_entries.keys() if hasattr(cmor2.axis_entries.__dict__[key], 'z_factors')]

    z_bnds     = {key for var in variables for key in
                  cmor2.axis_entries.__dict__[var].z_bounds_factors.split(" ")
                  if key.find(':') == -1
                  if key in cmor2.variable_entry.__dict__.keys()}
    z_factors  = {key for var in variables for key in
                  cmor2.axis_entries.__dict__[var].z_factors.split(" ")
                  if key.find(':') == -1
                  if key in cmor2.variable_entry.__dict__.keys()}

    z_factors.update(z_bnds)

    formulaVar = list(z_factors)
    print "Create formula variables"
    for var in formulaVar:
        name = var
        long_name = cmor2.variable_entry.__dict__[var].long_name           \
                        if ('long_name' in
                            cmor2.variable_entry.__dict__[var].keys()) else ""
        ctype     = cmor2.variable_entry.__dict__[var].type                 \
                        if ('type' in
                            cmor2.variable_entry.__dict__[var].keys()) else ""
        dimension = " ".join(cmor2.variable_entry.__dict__[var].dimensions[:])\
                        if ('dimensions' in
                            cmor2.variable_entry.__dict__[var].keys()) else ""
        units     = cmor2.variable_entry.__dict__[var].units                \
                        if ('units' in
                            cmor2.variable_entry.__dict__[var].keys()) else ""

        cmd = """select name from formulaVar where name = '""" + str(name).strip() + "';"
        c.execute(cmd)
        results = c.fetchall()
        if not results:
            cmd = """insert into formulaVar values (""" + \
                  "'" + str(name)              + "'" + """, """ \
                  "'" + str(long_name)         + "'" + """, """ \
                  "'" + str(ctype)             + "'" + """, """ \
                  "'" + str(dimension)         + "'" + """, """ \
                  "'" + str(units)             + "'" + """) """

        c.execute(cmd)

    print "Create axes"
    for axis in cmor2.axis_entries.keys():
        #    for item in cmor2.axis_entries.__getattribute__(axis).keys():
        #        print item
        name               = axis
        caxis              = cmor2.axis_entries.__getattribute__(axis).__getattribute__('axis')             \
                               if ('axis'             in cmor2.axis_entries.__getattribute__(axis).keys())     else ""
        climatology        = cmor2.axis_entries.__getattribute__(axis).__getattribute__('climatology')      \
                               if ('climatology'      in cmor2.axis_entries.__getattribute__(axis).keys())     else ""
        formula            = cmor2.axis_entries.__getattribute__(axis).__getattribute__('formula')          \
                               if ('formula'          in cmor2.axis_entries.__getattribute__(axis).keys())     else ""
        long_name          = cmor2.axis_entries.__getattribute__(axis).__getattribute__('long_name')        \
                               if ('long_name'        in cmor2.axis_entries.__getattribute__(axis).keys())     else ""
        must_have_bounds   = cmor2.axis_entries.__getattribute__(axis).__getattribute__('must_have_bounds') \
                               if ('must_have_bounds' in cmor2.axis_entries.__getattribute__(axis).keys())     else ""
        out_name           = cmor2.axis_entries.__getattribute__(axis).__getattribute__('out_name')         \
                               if ('out_name'       in cmor2.axis_entries.__getattribute__(axis).keys())       else ""
        positive           = cmor2.axis_entries.__getattribute__(axis).__getattribute__('positive').strip()         \
                               if ('positive'       in cmor2.axis_entries.__getattribute__(axis).keys())       else ""
        requested          = cmor2.axis_entries.__getattribute__(axis).__getattribute__('requested')        \
                               if ('requested'      in cmor2.axis_entries.__getattribute__(axis).keys())       else ""
        requested_bounds   = cmor2.axis_entries.__getattribute__(axis).__getattribute__('requested_bounds')        \
                               if ('requested_bounds'  in cmor2.axis_entries.__getattribute__(axis).keys())    else ""
        standard_name      = cmor2.axis_entries.__getattribute__(axis).__getattribute__('standard_name')    \
                               if ('standard_name'  in cmor2.axis_entries.__getattribute__(axis).keys())       else ""
        stored_direction   = cmor2.axis_entries.__getattribute__(axis).__getattribute__('stored_direction') \
                               if ('stored_direction' in cmor2.axis_entries.__getattribute__(axis).keys())     else ""
        tolerance          = cmor2.axis_entries.__getattribute__(axis).__getattribute__('tolerance')        \
                               if ('tolerance' in cmor2.axis_entries.__getattribute__(axis).keys())            else ""
        ctype              = cmor2.axis_entries.__getattribute__(axis).__getattribute__('type')             \
                               if ('type'      in cmor2.axis_entries.__getattribute__(axis).keys())            else ""
        units              = cmor2.axis_entries.__getattribute__(axis).__getattribute__('units')            \
                               if ('units'     in cmor2.axis_entries.__getattribute__(axis).keys())            else ""
        valid_max          = cmor2.axis_entries.__getattribute__(axis).__getattribute__('valid_max')        \
                               if ('valid_max' in cmor2.axis_entries.__getattribute__(axis).keys())            else ""
        valid_min          = cmor2.axis_entries.__getattribute__(axis).__getattribute__('valid_min')        \
                               if ('valid_min' in cmor2.axis_entries.__getattribute__(axis).keys())            else ""
        value              = cmor2.axis_entries.__getattribute__(axis).__getattribute__('value')            \
                               if ('value'     in cmor2.axis_entries.__getattribute__(axis).keys())            else ""
        z_bounds_factors   = cmor2.axis_entries.__getattribute__(axis).__getattribute__('z_bounds_factors') \
                               if ('z_bounds_factors'    in cmor2.axis_entries.__getattribute__(axis).keys())  else ""
        z_factors          = cmor2.axis_entries.__getattribute__(axis).__getattribute__('z_factors')        \
                               if ('z_factors' in cmor2.axis_entries.__getattribute__(axis).keys())            else ""
        bounds_values      = cmor2.axis_entries.__getattribute__(axis).__getattribute__('bounds_values')    \
                               if ('bounds_values'  in cmor2.axis_entries.__getattribute__(axis).keys())       else ""

#        cmd = """select name from axisEntry where name = '""" + str(name).strip() + "';"
#        c.execute(cmd)
#        results = c.fetchall()
#        if not results:
#            cmd = """insert into axisEntry values (""" + \
#                  "'" + str(name)              + "'" + """, """ \
#                  "'" + str(caxis)             + "'" + """, """ \
#                  "'" + str(climatology)       + "'" + """, """ \
#                  "'" + str(formula)           + "'" + """, """ \
#                  "'" + str(long_name)         + "'" + """, """ \
#                  "'" + str(must_have_bounds)  + "'" + """, """ \
#                  "'" + str(out_name)          + "'" + """, """ \
#                  "'" + str(positive)          + "'" + """, """ \
#                  "'" + str(requested)         + "'" + """, """ \
#                  "'" + str(requested_bounds)  + "'" + """, """ \
#                  "'" + str(standard_name)     + "'" + """, """ \
#                  "'" + str(stored_direction)  + "'" + """, """ \
#                  "'" + str(tolerance)    + "'" + """, """ \
#                  "'" + str(ctype)             + "'" + """, """ \
#                  "'" + str(units)             + "'" + """, """ \
#                  "'" + str(valid_max)    + "'" + """, """ \
#                  "'" + str(valid_min)    + "'" + """, """ \
#                  "'" + str(value)        + "'" + """, """ \
#                  "'" + str(z_bounds_factors)  + "'" + """, """ \
#                  "'" + str(z_factors)         + "'" + """, """ \
#                  "'" + str(bounds_values)     + "'" + """, """ \
#                  "'" + "Amon"                 + "'" + """) """
#            c.execute(cmd)
#            conn.commit()


cmor2 = cfg.Config()
cmor2.read_file("../tables/Amon_libconfig")
for expt in cmor2.expt_ids:
    eid                = expt.id or ""
    title              = expt.title or ""
    cmd = """insert into expIDs values (""" + \
          "'" + str(eid)              + "'" + """, """ \
          "'" + str(title)             + "'" + """) """
    c.execute(cmd)
# *********************************************************
# CMOR 3 files are libconfig2 format from old CMOR2 tables
# *********************************************************
files = ["./CMIP5_Omon_CMOR3", "./CMIP6_OImon_CMOR3", "./CMIP6_LImon_CMOR3",
         "./CMIP6_Lmon_CMOR3", "./CMIP5_3hr_CMOR3",
         "./CMIP5_cfSites_CMOR3", "./CMIP5_cf3hr_CMOR3", "./CMIP5_cfMon_CMOR3"]
#, "./CMIP6_new_axis_CMOR3" ]
for file in files:
    print "reading file" + file
    cmor2 = cfg.Config()
    cmor2.read_file(file)
    # Add formula variables
    #

    variables = [key for key in cmor2.axis_entries.keys()
                 if hasattr(cmor2.axis_entries.__dict__[key], 'z_factors')]

    z_bnds     = {key for var in variables for key in cmor2.axis_entries.__dict__[var].z_bounds_factors.split(" ")
                  if key.find(':') == -1  if key in cmor2.variable_entry.__dict__.keys()}
    z_factors  = {key for var in variables for key in cmor2.axis_entries.__dict__[var].z_factors.split(" ") if key.find(':') == -1
                  if key in cmor2.variable_entry.__dict__.keys()}

    z_factors.update(z_bnds)

    formulaVar = list(z_factors)
    print "Create formula variables"
    for var in formulaVar:
        name = var
        long_name = cmor2.variable_entry.__dict__[var].long_name                     \
                        if ('long_name' in cmor2.variable_entry.__dict__[var].keys()) else ""
        ctype     = cmor2.variable_entry.__dict__[var].type                          \
                        if ('type' in cmor2.variable_entry.__dict__[var].keys())      else ""
        dimension = " ".join(cmor2.variable_entry.__dict__[var].dimensions[:])       \
                        if ('dimensions' in cmor2.variable_entry.__dict__[var].keys()) else ""
        units     = cmor2.variable_entry.__dict__[var].units                         \
                        if ('units' in cmor2.variable_entry.__dict__[var].keys())     else ""

        cmd = """select name from formulaVar where name = '""" + str(name).strip() + "';"
        c.execute(cmd)
        results = c.fetchall()
        if not results:
            cmd = """insert into formulaVar values (""" + \
                  "'" + str(name)              + "'" + """, """ \
                  "'" + str(long_name)         + "'" + """, """ \
                  "'" + str(ctype)             + "'" + """, """ \
                  "'" + str(dimension)         + "'" + """, """ \
                  "'" + str(units)             + "'" + """) """

            c.execute(cmd)

    print "Create axes"
    for axis in cmor2.axis_entries.keys():
        #
        #    for item in cmor2.axis_entries.__getattribute__(axis).keys():
        #        print item
        #
        name               = axis
        caxis              = cmor2.axis_entries.__getattribute__(axis).__getattribute__('axis')             \
                               if ('axis'             in cmor2.axis_entries.__getattribute__(axis).keys())     else ""
        climatology        = cmor2.axis_entries.__getattribute__(axis).__getattribute__('climatology')      \
                               if ('climatology'      in cmor2.axis_entries.__getattribute__(axis).keys())     else ""
        formula            = cmor2.axis_entries.__getattribute__(axis).__getattribute__('formula')          \
                               if ('formula'          in cmor2.axis_entries.__getattribute__(axis).keys())     else ""
        long_name          = cmor2.axis_entries.__getattribute__(axis).__getattribute__('long_name')        \
                               if ('long_name'        in cmor2.axis_entries.__getattribute__(axis).keys())     else ""
        must_have_bounds   = cmor2.axis_entries.__getattribute__(axis).__getattribute__('must_have_bounds') \
                               if ('must_have_bounds' in cmor2.axis_entries.__getattribute__(axis).keys())     else ""
        out_name           = cmor2.axis_entries.__getattribute__(axis).__getattribute__('out_name')         \
                               if ('out_name'       in cmor2.axis_entries.__getattribute__(axis).keys())       else ""
        positive           = cmor2.axis_entries.__getattribute__(axis).__getattribute__('positive').strip()         \
                               if ('positive'       in cmor2.axis_entries.__getattribute__(axis).keys())       else ""
        requested          = cmor2.axis_entries.__getattribute__(axis).__getattribute__('requested')        \
                               if ('requested'      in cmor2.axis_entries.__getattribute__(axis).keys())       else ""
        requested_bounds   = cmor2.axis_entries.__getattribute__(axis).__getattribute__('requested_bounds')        \
                               if ('requested_bounds'  in cmor2.axis_entries.__getattribute__(axis).keys())    else ""
        standard_name      = cmor2.axis_entries.__getattribute__(axis).__getattribute__('standard_name')    \
                               if ('standard_name'  in cmor2.axis_entries.__getattribute__(axis).keys())       else ""
        stored_direction   = cmor2.axis_entries.__getattribute__(axis).__getattribute__('stored_direction') \
                               if ('stored_direction' in cmor2.axis_entries.__getattribute__(axis).keys())     else ""
        tolerance          = cmor2.axis_entries.__getattribute__(axis).__getattribute__('tolerance')        \
                               if ('tolerance' in cmor2.axis_entries.__getattribute__(axis).keys())            else ""
        ctype              = cmor2.axis_entries.__getattribute__(axis).__getattribute__('type')             \
                               if ('type'      in cmor2.axis_entries.__getattribute__(axis).keys())            else ""
        units              = cmor2.axis_entries.__getattribute__(axis).__getattribute__('units')            \
                               if ('units'     in cmor2.axis_entries.__getattribute__(axis).keys())            else ""
        valid_max          = cmor2.axis_entries.__getattribute__(axis).__getattribute__('valid_max')        \
                               if ('valid_max' in cmor2.axis_entries.__getattribute__(axis).keys())            else ""
        valid_min          = cmor2.axis_entries.__getattribute__(axis).__getattribute__('valid_min')        \
                               if ('valid_min' in cmor2.axis_entries.__getattribute__(axis).keys())            else ""
        value              = cmor2.axis_entries.__getattribute__(axis).__getattribute__('value')            \
                               if ('value'     in cmor2.axis_entries.__getattribute__(axis).keys())            else ""
        z_bounds_factors   = cmor2.axis_entries.__getattribute__(axis).__getattribute__('z_bounds_factors') \
                               if ('z_bounds_factors'    in cmor2.axis_entries.__getattribute__(axis).keys())  else ""
        z_factors          = cmor2.axis_entries.__getattribute__(axis).__getattribute__('z_factors')        \
                               if ('z_factors' in cmor2.axis_entries.__getattribute__(axis).keys())            else ""
        bounds_values      = cmor2.axis_entries.__getattribute__(axis).__getattribute__('bounds_values')    \
                               if ('bounds_values' in cmor2.axis_entries.__getattribute__(axis).keys())        else ""

        cmd = """select name from axisEntry where name = '""" + str(name).strip() + "';"
        c.execute(cmd)
        results = c.fetchall()
        if not results:
            tkFile = file.split("_")[1]
            cmd = """insert into axisEntry values (""" + \
                  "'" + str(name)              + "'" + """, """ \
                  "'" + str(caxis)             + "'" + """, """ \
                  "'" + str(climatology)       + "'" + """, """ \
                  "'" + str(formula).replace("\n","\\n")           + "'" + """, """ \
                  "'" + str(long_name)         + "'" + """, """ \
                  "'" + str(must_have_bounds)  + "'" + """, """ \
                  "'" + str(out_name)          + "'" + """, """ \
                  "'" + str(positive)          + "'" + """, """ \
                  "'" + str(requested)         + "'" + """, """ \
                  "'" + str(requested_bounds)  + "'" + """, """ \
                  "'" + str(standard_name)     + "'" + """, """ \
                  "'" + str(stored_direction)  + "'" + """, """ \
                  "'" + str(tolerance)    + "'" + """, """ \
                  "'" + str(ctype)             + "'" + """, """ \
                  "'" + str(units)             + "'" + """, """ \
                  "'" + str(valid_max)    + "'" + """, """ \
                  "'" + str(valid_min)    + "'" + """, """ \
                  "'" + str(value)        + "'" + """, """ \
                  "'" + str(z_bounds_factors)  + "'" + """, """ \
                  "'" + str(z_factors)         + "'" + """, """ \
                  "'" + str(bounds_values)         + "'" + """, """ \
                  "'" + str(tkFile)            + "'" + """) """
            c.execute(cmd)

cmor2 = cfg.Config()
cmor2.read_file("./CMIP5_grids_CMOR3")
print "Create axes for grids"
for axis in cmor2.axis_entry.keys():
    name               = axis
    caxis              = cmor2.axis_entry.__getattribute__(axis).__getattribute__('axis')             \
                           if ('axis'             in cmor2.axis_entry.__getattribute__(axis).keys())     else ""
    climatology        = cmor2.axis_entry.__getattribute__(axis).__getattribute__('climatology')      \
                           if ('climatology'      in cmor2.axis_entry.__getattribute__(axis).keys())     else ""
    formula            = cmor2.axis_entry.__getattribute__(axis).__getattribute__('formula')          \
                           if ('formula'          in cmor2.axis_entry.__getattribute__(axis).keys())     else ""
    long_name          = cmor2.axis_entry.__getattribute__(axis).__getattribute__('long_name')        \
                           if ('long_name'        in cmor2.axis_entry.__getattribute__(axis).keys())     else ""
    must_have_bounds   = cmor2.axis_entry.__getattribute__(axis).__getattribute__('must_have_bounds') \
                           if ('must_have_bounds' in cmor2.axis_entry.__getattribute__(axis).keys())     else ""
    out_name           = cmor2.axis_entry.__getattribute__(axis).__getattribute__('out_name')         \
                           if ('out_name'       in cmor2.axis_entry.__getattribute__(axis).keys())       else ""
    positive           = cmor2.axis_entry.__getattribute__(axis).__getattribute__('positive').strip()         \
                           if ('positive'       in cmor2.axis_entry.__getattribute__(axis).keys())       else ""
    requested          = cmor2.axis_entry.__getattribute__(axis).__getattribute__('requested')        \
                           if ('requested'      in cmor2.axis_entry.__getattribute__(axis).keys())       else ""
    requested_bounds   = cmor2.axis_entry.__getattribute__(axis).__getattribute__('requested_bounds')        \
                           if ('requested_bounds'  in cmor2.axis_entry.__getattribute__(axis).keys())  else ""
    standard_name      = cmor2.axis_entry.__getattribute__(axis).__getattribute__('standard_name')    \
                           if ('standard_name'  in cmor2.axis_entry.__getattribute__(axis).keys())       else ""
    stored_direction   = cmor2.axis_entry.__getattribute__(axis).__getattribute__('stored_direction') \
                           if ('stored_direction' in cmor2.axis_entry.__getattribute__(axis).keys())     else ""
    tolerance          = cmor2.axis_entry.__getattribute__(axis).__getattribute__('tolerance')        \
                           if ('tolerance' in cmor2.axis_entry.__getattribute__(axis).keys())            else ""
    ctype              = cmor2.axis_entry.__getattribute__(axis).__getattribute__('type')             \
                           if ('type'      in cmor2.axis_entry.__getattribute__(axis).keys())            else ""
    units              = cmor2.axis_entry.__getattribute__(axis).__getattribute__('units')            \
                           if ('units'     in cmor2.axis_entry.__getattribute__(axis).keys())            else ""
    valid_max          = cmor2.axis_entry.__getattribute__(axis).__getattribute__('valid_max')        \
                           if ('valid_max' in cmor2.axis_entry.__getattribute__(axis).keys())            else ""
    valid_min          = cmor2.axis_entry.__getattribute__(axis).__getattribute__('valid_min')        \
                           if ('valid_min' in cmor2.axis_entry.__getattribute__(axis).keys())            else ""
    value              = cmor2.axis_entry.__getattribute__(axis).__getattribute__('value')            \
                           if ('value'     in cmor2.axis_entry.__getattribute__(axis).keys())            else ""
    z_bounds_factors   = cmor2.axis_entry.__getattribute__(axis).__getattribute__('z_bounds_factors') \
                           if ('z_bounds_factors'    in cmor2.axis_entry.__getattribute__(axis).keys())  else ""
    z_factors          = cmor2.axis_entry.__getattribute__(axis).__getattribute__('z_factors')        \
                           if ('z_factors' in cmor2.axis_entry.__getattribute__(axis).keys())            else ""
    bounds_values      = cmor2.axis_entry.__getattribute__(axis).__getattribute__('bounds_values')    \
                           if ('bounds_values' in cmor2.axis_entry.__getattribute__(axis).keys())        else ""

    cmd = """select name from axisEntry where name = '""" + str(name).strip() + "';"
    c.execute(cmd)
    results = c.fetchall()

    if not results:
        cmd = """insert into axisEntry values (""" + \
              "'" + str(name)              + "'" + """, """ \
              "'" + str(caxis)             + "'" + """, """ \
              "'" + str(climatology)       + "'" + """, """ \
              "'" + str(formula)           + "'" + """, """ \
              "'" + str(long_name)         + "'" + """, """ \
              "'" + str(must_have_bounds)  + "'" + """, """ \
              "'" + str(out_name)          + "'" + """, """ \
              "'" + str(positive)          + "'" + """, """ \
              "'" + str(requested)         + "'" + """, """ \
              "'" + str(requested_bounds)  + "'" + """, """ \
              "'" + str(standard_name)     + "'" + """, """ \
              "'" + str(stored_direction)  + "'" + """, """ \
              "'" + str(tolerance)    + "'" + """, """ \
              "'" + str(ctype)             + "'" + """, """ \
              "'" + str(units)             + "'" + """, """ \
              "'" + str(valid_max)    + "'" + """, """ \
              "'" + str(valid_min)    + "'" + """, """ \
              "'" + str(value)        + "'" + """, """ \
              "'" + str(z_bounds_factors)  + "'" + """, """ \
              "'" + str(z_factors)         + "'" + """, """ \
              "'" + str(bounds_values)         + "'" + """, """ \
              "'grid') """
        c.execute(cmd)

gridVar = [key for key in cmor2.variable_entry.keys()]

print "Create grid variables"

ssLabelTmpl = "grid-"
for var in gridVar:
    count = 1
    ssLabel = ssLabelTmpl + str(count)

    name = var
    deflate         = ""
    deflate_level   = ""
    description     = ""
    frequency       = ""
    label           = ""
    mipTable        = ""
    modeling_realm  = ""
    ok_max_mean_abs = ""
    ok_min_mean_abs = ""
    positive        = ""
    prov            = ""
    provNote        = ""
    rowIndex        = ""
    shuffle         = ""
    stid            = ""
    title           = ""
    vtype           = ""
    uid             = ""
    valid_max       = ""
    valid_min       = ""
    vid             = ""

    dimensions  = "|".join(cmor2.variable_entry.__dict__[var].dimensions)
    print dimensions
    cmd = """select uid from spatialShape where dimensions = '""" + dimensions + "';"
    c.execute(cmd)
    results = c.fetchall()

    if not results:
        # -------------------------
        # Insert new struture ID
        # -------------------------
        spid = uuid.uuid4().urn.split(':')[2]
        cmd = """insert into spatialShape values (""" + \
                     "'" + dimensions + "'" + """, """ + \
                     "'ssd-" + name   + "'" + """, """ + \
                     "'false'"        + """, """ + \
                     "'0'"            + """, """ + \
                     "'ssd-" + name   + "'" + """, """ + \
                     "'" + spid        + "'" + """) """
        c.execute(cmd)
    else:
        spid=results[0][0]
    print spid
    stid = uuid.uuid4().urn.split(':')[2]
    cmd = """insert into structure values (""" + \
                 "'area:areacella'" + """, """ + \
                 "''" + """, """ + \
                 "''" + """, """ + \
                 "''" + """, """ + \
                 "''" + """, """ + \
                 "''" + """, """ + \
                 "'" + ssLabel  + "'" + """, """  \
                 "''" + """, """ + \
                 "''" + """, """ + \
                 "''" + """, """ + \
                 "'" + spid       + "'" + """, """  \
                 "'" + "0000-0000-0000"       + "'" + """, """ \
                 "'" + stid        + "'" + """) """
    c.execute(cmd)

    # -------------------------
    # select new uid for grid shape
    # -------------------------
    cmd = """select uid from var where label = '""" + name + "';"
    c.execute(cmd)
    results = c.fetchall()
    if not results:
        units     = cmor2.variable_entry.__dict__[var].units \
            if ('units' in cmor2.variable_entry.__dict__[var].keys()) else ""
        vid = uuid.uuid4().urn.split(':')[2]
        cmd = """insert into var values (""" + \
                 "'grid variable'" + """, """ + \
                 "'" + ssLabel       + "'" + """, """  \
                 "'" + name       + "'" + """, """  \
                 "''" + """, """ + \
                 "''" + """, """ + \
                 "''" + """, """ + \
                 "''" + """, """ + \
                 "''" + """, """ + \
                 "'" + vid.replace('\'','')       + "'" + """, """  \
                 "'" + units      + "'" + """) """
        c.execute(cmd)
        results = c.fetchall()
    else:
        vid = results[0][0]

    long_name = cmor2.variable_entry.__dict__[var].long_name                     \
                    if ('long_name' in cmor2.variable_entry.__dict__[var].keys()) else ""
    standard_name = cmor2.variable_entry.__dict__[var].standard_name                          \
                    if ('standard_name' in cmor2.variable_entry.__dict__[var].keys())      else ""
    units     = cmor2.variable_entry.__dict__[var].units                         \
                    if ('units' in cmor2.variable_entry.__dict__[var].keys())     else ""
    out_name  = cmor2.variable_entry.__dict__[var].out_name                          \
                    if ('out_name ' in cmor2.variable_entry.__dict__[var].keys())      else ""
    valid_min = cmor2.variable_entry.__dict__[var].valid_min                          \
                    if ('valid_min' in cmor2.variable_entry.__dict__[var].keys())      else ""
    valid_max = cmor2.variable_entry.__dict__[var].valid_max                          \
                    if ('valid_max' in cmor2.variable_entry.__dict__[var].keys())      else ""

    cmd = """select label from CMORvar where label = '""" + str(name).strip() + "' and mipTable='grids';"
    c.execute(cmd)
    results = c.fetchall()
    #
    # grid
    #
    if not results:
        mipTable = "grids"
        label = name
        cmd = """insert into CMORvar values (""" + \
             "'" + deflate         + "'" + """, """ + \
             "'" + deflate_level   + "'" + """, """ + \
             "'" + description.replace("'", "\"")     + "'" + """, """ + \
             "'" + frequency       + "'" + """, """ + \
             "'" + label           + "'" + """, """ + \
             "'" + mipTable        + "'" + """, """ + \
             "'" + modeling_realm  + "'" + """, """ + \
             "'" + ok_max_mean_abs + "'" + """, """ + \
             "'" + ok_min_mean_abs + "'" + """, """ + \
             "'" + positive        + "'" + """, """ + \
             "'" + prov            + "'" + """, """ + \
             "'" + provNote        + "'" + """, """ + \
             "'" + rowIndex        + "'" + """, """ + \
             "'" + shuffle         + "'" + """, """ + \
             "'" + stid            + "'" + """, """ + \
             "'" + title           + "'" + """, """ + \
             "'" + vtype           + "'" + """, """ + \
             "'" + uid.replace('\'','')             + "'" + """, """ + \
             "'" + str(valid_max)  + "'" + """, """ + \
             "'" + str(valid_min)  + "'" + """, """ + \
             "'" + vid.replace('\'','')             + "'" + """) """

        c.execute(cmd)

c.execute("commit")
###  Work on cfMon
#cmor2=cfg.Config()
#cmor2.read_file("./CMIP5_cfMon_CMOR3")
#print "Create axes for cfMon"
#for axis in cmor2.axis_entry.keys():
#   name               = axis
#   caxis              = cmor2.axis_entry.__getattribute__(axis).__getattribute__('axis')             \
#                          if ('axis'             in cmor2.axis_entry.__getattribute__(axis).keys())     else ""
#   climatology        = cmor2.axis_entry.__getattribute__(axis).__getattribute__('climatology')      \
#                          if ('climatology'      in cmor2.axis_entry.__getattribute__(axis).keys())     else ""
#   formula            = cmor2.axis_entry.__getattribute__(axis).__getattribute__('formula')          \
#                          if ('formula'          in cmor2.axis_entry.__getattribute__(axis).keys())     else ""
#   long_name          = cmor2.axis_entry.__getattribute__(axis).__getattribute__('long_name')        \
#                          if ('long_name'        in cmor2.axis_entry.__getattribute__(axis).keys())     else ""
#   must_have_bounds   = cmor2.axis_entry.__getattribute__(axis).__getattribute__('must_have_bounds') \
#                          if ('must_have_bounds' in cmor2.axis_entry.__getattribute__(axis).keys())     else ""
#   out_name           = cmor2.axis_entry.__getattribute__(axis).__getattribute__('out_name')         \
#                          if ('out_name'       in cmor2.axis_entry.__getattribute__(axis).keys())       else ""
#   positive           = cmor2.axis_entry.__getattribute__(axis).__getattribute__('positive').strip()         \
#                          if ('positive'       in cmor2.axis_entry.__getattribute__(axis).keys())       else ""
#   requested          = cmor2.axis_entry.__getattribute__(axis).__getattribute__('requested')        \
#                          if ('requested'      in cmor2.axis_entry.__getattribute__(axis).keys())       else ""
#   standard_name      = cmor2.axis_entry.__getattribute__(axis).__getattribute__('standard_name')    \
#                          if ('standard_name'  in cmor2.axis_entry.__getattribute__(axis).keys())       else ""
#   stored_direction   = cmor2.axis_entry.__getattribute__(axis).__getattribute__('stored_direction') \
#                          if ('stored_direction' in cmor2.axis_entry.__getattribute__(axis).keys())     else ""
#   tolerance          = cmor2.axis_entry.__getattribute__(axis).__getattribute__('tolerance')        \
#                          if ('tolerance' in cmor2.axis_entry.__getattribute__(axis).keys())            else ""
#   ctype              = cmor2.axis_entry.__getattribute__(axis).__getattribute__('type')             \
#                          if ('type'      in cmor2.axis_entry.__getattribute__(axis).keys())            else ""
#   units              = cmor2.axis_entry.__getattribute__(axis).__getattribute__('units')            \
#                          if ('units'     in cmor2.axis_entry.__getattribute__(axis).keys())            else ""
#   valid_max          = cmor2.axis_entry.__getattribute__(axis).__getattribute__('valid_max')        \
#                          if ('valid_max' in cmor2.axis_entry.__getattribute__(axis).keys())            else ""
#   valid_min          = cmor2.axis_entry.__getattribute__(axis).__getattribute__('valid_min')        \
#                          if ('valid_min' in cmor2.axis_entry.__getattribute__(axis).keys())            else ""
#   value              = cmor2.axis_entry.__getattribute__(axis).__getattribute__('value')            \
#                          if ('value'     in cmor2.axis_entry.__getattribute__(axis).keys())            else ""
#   z_bounds_factors   = cmor2.axis_entry.__getattribute__(axis).__getattribute__('z_bounds_factors') \
#                          if ('z_bounds_factors'    in cmor2.axis_entry.__getattribute__(axis).keys())  else ""
#   z_factors          = cmor2.axis_entry.__getattribute__(axis).__getattribute__('z_factors')        \
#                          if ('z_factors' in cmor2.axis_entry.__getattribute__(axis).keys())            else ""
#
#
#   cmd = """select name from axisEntry where name = '"""+str(name)+"';"
#   c.execute(cmd)
#   results = c.fetchall()
#
#   if not results:
#       cmd = """insert into axisEntry values ("""+ \
#             "'" + str(name)              + "'" + """, """ \
#             "'" + str(caxis)             + "'" + """, """ \
#             "'" + str(climatology)       + "'" + """, """ \
#             "'" + str(formula)           + "'" + """, """ \
#             "'" + str(long_name)         + "'" + """, """ \
#             "'" + str(must_have_bounds)  + "'" + """, """ \
#             "'" + str(out_name)          + "'" + """, """ \
#             "'" + str(positive)          + "'" + """, """ \
#             "'" + str(requested)         + "'" + """, """ \
#             "'" + str(standard_name)     + "'" + """, """ \
#             "'" + str(stored_direction)  + "'" + """, """ \
#             "'" + str(tolerance)    + "'" + """, """ \
#             "'" + str(ctype)             + "'" + """, """ \
#             "'" + str(units)             + "'" + """, """ \
#             "'" + str(valid_max)    + "'" + """, """ \
#             "'" + str(valid_min)    + "'" + """, """ \
#             "'" + str(value)        + "'" + """, """ \
#             "'" + str(z_bounds_factors)  + "'" + """, """ \
#             "'" + str(z_factors)         + "'" + """, """ \
#             "'cfMon') """
#       c.execute(cmd)
#       conn.commit()
#

c.close()
