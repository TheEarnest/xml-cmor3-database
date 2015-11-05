#!/bin/env python

#sqlite> select DISTINCT vg.label from requestVar vg, requestVarGroup rvg, requestItem ri, requestlink rl where  ri.mip="GeoMIP" and ri.rlid==rl.uid and rl.refid=rvg.uid and vg.vid=rvg.uid;
import sqlite3
#import dreq
#import collections, string
#import scope
import pdb
import xml.etree.ElementTree as ET






conn = sqlite3.connect('/tmp/CMIP6')
c = conn.cursor()
c.execute("""drop table if exists var""")
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

conn.commit()
print "Create Tables"
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

#c.execute(""" create table denis (label text, mip text, priority text, table text, title text, uid text, vgid text, vid text)""")

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

# -----------------------------------
# Read in database and set namespace
# -----------------------------------
contentDoc = ET.parse( "../docs/dreq.xml" )
root=contentDoc.getroot()
namespace = '{urn:w3id.org:cmip6.dreq.dreq:a}'

var=root.findall('./{0}main/{0}var'.format(namespace))[0]
print "Create var"
for child in var.getchildren():
    description = child.get('description').replace("'","\"")  or ""
    id          = child.get('id')           or ""
    label       = child.get('label')        or ""
    proComment  = child.get('proComment')   or ""
    proNote     = child.get('pronote')      or ""
    prov        = child.get('prov')         or ""
    sn          = child.get('sn')           or ""
    title       = child.get('title').replace("'","\"")        or ""
    uid         = child.get('uid')          or "" 
    units       = child.get('units')        or ""
  
    cmd = """insert into var values ("""+ \
		 "'" + description + "'" + """, """ + \
		 "'" + id          + "'" + """, """ + \
		 "'" + label       + "'" + """, """ + \
		 "'" + proComment  + "'" + """, """ + \
		 "'" + proNote     + "'" + """, """ + \
		 "'" + prov        + "'" + """, """ + \
		 "'" + sn          + "'" + """, """ + \
		 "'" + title       + "'" + """, """ + \
		 "'" + uid         + "'" + """, """ + \
		 "'" + units       + "'" + """) """ 

    c.execute(cmd)
    conn.commit()
var=""

# ----------------------------------
#  Insert CMORvar in the database
# ----------------------------------
CMORvar=root.findall('./{0}main/{0}CMORvar'.format(namespace))[0]

print "Create CMORvar"
for child in CMORvar.getchildren():
    deflate         = child.get('deflate').replace('None','')         or ""
    deflate_level   = child.get('deflate_level').replace('None','')   or ""
    description     = child.get('description').replace('None','')     or "" 
    frequency       = child.get('frequency').replace('None','')       or ""
    label           = child.get('label').replace('None','')           or ""
    mipTable        = child.get('mipTable').replace('None','')        or ""
    modeling_realm  = child.get('modeling_realm').replace('None','')  or ""
    ok_max_mean_abs = child.get('ok_max_mean_abs').replace('None','') or ""
    ok_min_mean_abs = child.get('ok_min_mean_abs').replace('None','') or ""
    positive        = child.get('positive').replace('None','')        or ""
    prov            = child.get('prov').replace('None','')            or ""
    provNote        = child.get('provNote').replace('None','')        or ""
    rowIndex        = child.get('rowIndex').replace('None','')        or ""
    shuffle         = child.get('shuffle').replace('None','')         or ""
    stid            = child.get('stid').replace('None','')            or ""
    title           = child.get('title').replace('None','')           or ""
    type            = child.get('type').replace('None','')            or ""
    uid             = child.get('uid').replace('None','')             or "" 
    valid_max       = child.get('valid_max').replace('None','')       or ""
    valid_min       = child.get('valid_min').replace('None','')       or ""
    vid             = child.get('vid').replace('None','')             or ""

    cmd = """insert into CMORvar values ("""+ \
		 "'" + deflate         + "'" + """, """ + \
		 "'" + deflate_level   + "'" + """, """ + \
		 "'" + description.replace("'","\"")     + "'" + """, """ + \
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
		 "'" + type            + "'" + """, """ + \
		 "'" + uid             + "'" + """, """ + \
		 "'" + valid_max       + "'" + """, """ + \
		 "'" + valid_min       + "'" + """, """ + \
		 "'" + vid             + "'" + """) """ 

    c.execute(cmd)
    conn.commit()
CMORvar=""

# ----------------------------------
#  Insert structure in the database
# ----------------------------------
structure=root.findall('./{0}main/{0}structure'.format(namespace))[0]
print "Create structure"
for child in structure.getchildren():
    cell_measures   = child.get('cell_measures').replace('None','')   or "" 
    cell_methods    = child.get('cell_methods').replace('None','')    or ""
    coords          = child.get('coords').replace('None','')          or ""
    description     = child.get('description').replace('None','')     or ""
    flag_meanings   = child.get('flag_meanings').replace('None','')   or ""
    flag_values     = child.get('flag_values').replace('None','')     or ""
    label           = child.get('label').replace('None','')           or ""
    odims           = child.get('odims').replace('None','')           or ""
    procNote        = child.get('procNote').replace('None','')        or ""
    prov            = child.get('prov').replace('None','')            or ""
    spid            = child.get('spid').replace('None','')            or ""
    tmid            = child.get('tmid').replace('None','')            or ""
    uid             = child.get('uid').replace('None','')             or ""

    cmd = """insert into structure values ("""+ \
	     "'" + cell_measures   + "'" + """, """ + \
	     "'" + cell_methods    + "'" + """, """ + \
	     "'" + coords          + "'" + """, """ + \
	     "'" + description.replace("'","\"") + "'" + """, """ + \
	     "'" + flag_meanings   + "'" + """, """ + \
	     "'" + flag_values     + "'" + """, """ + \
	     "'" + label           + "'" + """, """ + \
	     "'" + odims           + "'" + """, """ + \
	     "'" + procNote        + "'" + """, """ + \
	     "'" + prov            + "'" + """, """ + \
	     "'" + spid            + "'" + """, """ + \
	     "'" + tmid            + "'" + """, """ + \
	     "'" + uid             + "'" + """) """ 
    c.execute(cmd)
    conn.commit()
structure=""

# ----------------------------------
#  Insert spatialShape in the database
# ----------------------------------
spatialShape=root.findall('./{0}main/{0}spatialShape'.format(namespace))[0]
print "Create spatialShape"
for child in spatialShape.getchildren():
    dimensions       = child.get('dimensions').replace('None','')      or ""
    label            = child.get('label').replace('None','')           or ""
    levelFlag        = child.get('levelFlag').replace('None','')       or ""
    levels           = child.get('levels').replace('None','')          or ""
    title            = child.get('title').replace('None','')           or ""
    uid              = child.get('uid'.replace('None',''))             or ""

    cmd = """insert into spatialShape values ("""+ \
                 "'" + dimensions + "'" + """, """ + \
                 "'" + label      + "'" + """, """ + \
                 "'" + levelFlag  + "'" + """, """ + \
                 "'" + levels     + "'" + """, """ + \
                 "'" + title      + "'" + """, """ + \
                 "'" + uid        + "'" + """) """ 
    c.execute(cmd)
    conn.commit()
spatialShape=""

# ----------------------------------
#  Insert temporalShape in the database
# ----------------------------------
temporalShape=root.findall('./{0}main/{0}temporalShape'.format(namespace))[0]
print "Create temporalShape"
for child in temporalShape.getchildren():
    dimensions            = child.get('dimensions').replace('None','')  or ""
    label                 = child.get('label').replace('None','') or ""
    title                 = child.get('title').replace('None','') or ""
    uid                   = child.get('uid').replace('None','') or ""
    cmd = """insert into temporalShape values ("""+ \
                 "'" + dimensions + "'" + """, """ + \
                 "'" + label      + "'" + """, """ + \
                 "'" + title      + "'" + """, """ + \
                 "'" + uid        + "'" + """) """ 
    c.execute(cmd)
    conn.commit()
temporalShape=""

# ----------------------------------
#  Insert requestVar in the database
# ----------------------------------
requestVar=root.findall('./{0}main/{0}requestVar'.format(namespace))[0]
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


    cmd = """insert into requestVar values ("""+ \
                 "'" + label    + "'" + """, """ + \
                 "'" + mip      + "'" + """, """ + \
                 "'" + priority + "'" + """, """ + \
                 "'" + tables   + "'" + """, """ + \
                 "'" + title    + "'" + """, """ + \
                 "'" + uid      + "'" + """, """ + \
                 "'" + vgid     + "'" + """, """ + \
                 "'" + vid      + "'" + """) """ 
    c.execute(cmd)
    conn.commit()
requestVar=""

requestVarGroup=root.findall('./{0}main/{0}requestVarGroup'.format(namespace))[0]
print "Create requestVarGrouop"
for child in requestVarGroup.getchildren():
    label                 = child.get('label') or ""
    mip                   = child.get('mip') or ""
    ref                   = child.get('ref') or ""
    refNote               = child.get('refNote') or ""
    title                 = child.get('title') or ""
    uid                   = child.get('uid') or ""

    cmd = """insert into requestVarGroup values ("""+ \
                 "'" + label   + "'" + """, """ + \
                 "'" + mip     + "'" + """, """ + \
                 "'" + ref     + "'" + """, """ + \
                 "'" + refNote + "'" + """, """ + \
                 "'" + title   + "'" + """, """ + \
                 "'" + uid     + "'" + """) """ 
    c.execute(cmd)
    conn.commit()
requestVarGroup=""

requestLink=root.findall('./{0}main/{0}requestLink'.format(namespace))[0]
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

    cmd = """insert into requestLink values ("""+ \
                 "'" + comment  + "'" + """, """ + \
                 "'" + grid     + "'" + """, """ + \
                 "'" + gridreq  + "'" + """, """ + \
                 "'" + mip      + "'" + """, """ + \
                 "'" + objective+ "'" + """, """ + \
                 "'" + opar     + "'" + """, """ + \
                 "'" + opt      + "'" + """, """ + \
                 "'" + preset   + "'" + """, """ + \
                 "'" + ref      + "'" + """, """ + \
                 "'" + refNote  + "'" + """, """ + \
                 "'" + refid    + "'" + """, """ + \
                 "'" + tab      + "'" + """, """ + \
                 "'" + title    + "'" + """, """ + \
                 "'" + uid      + "'" + """) """ 
    c.execute(cmd)
    conn.commit()
requestLink=""

requestItem=root.findall('./{0}main/{0}requestItem'.format(namespace))[0]
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

    cmd = """insert into requestItem values ("""+ \
                 "'" + comment.replace("'","\"")    + "'" + """, """ + \
                 "'" + esid       + "'" + """, """ + \
                 "'" + esidComment.replace("'","\"")+ "'" + """, """ + \
                 "'" + expt       + "'" + """, """ + \
                 "'" + label      + "'" + """, """ + \
                 "'" + mip        + "'" + """, """ + \
                 "'" + nenmax     + "'" + """, """ + \
                 "'" + nexmax     + "'" + """, """ + \
                 "'" + ny         + "'" + """, """ + \
                 "'" + nymax      + "'" + """, """ + \
                 "'" + rlid       + "'" + """, """ + \
                 "'" + tab        + "'" + """, """ + \
                 "'" + title.replace("'","\"")      + "'" + """, """ + \
                 "'" + uid        + "'" + """) """ 
    c.execute(cmd)
    conn.commit()
requestItem=""

experiment=root.findall('./{0}main/{0}experiment'.format(namespace))[0]
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

	cmd = """insert into experiment values ("""+ \
		     "'" + comment.replace("'", "\"")    + "'" + """, """ + \
		     "'" + description.replace("'", "\"")+ "'" + """, """ + \
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
		     "'" + uid        + "'" + """, """ + \
		     "'" + yps        + "'" + """) """ 

	c.execute(cmd)
	conn.commit()
experiment=""

exptgroup=root.findall('./{0}main/{0}exptgroup'.format(namespace))[0]
print "Create exptgroup"
for child in exptgroup.getchildren():
	label        = child.get('label') or ""
	ntot         = child.get('ntot') or ""
	tierMin      = child.get('tierMin') or ""
	uid          = child.get('uid') or ""
	cmd = """insert into exptgroup values ("""+ \
		     "'" + label    + "'" + """, """ + \
		     "'" + ntot     + "'" + """, """ + \
		     "'" + tierMin  + "'" + """, """ + \
		     "'" + uid      + "'" + """) """
	c.execute(cmd)
	conn.commit()
exptgroup=""
MIP=root.findall('./{0}main/{0}mip'.format(namespace))[0]
print "Create MIP"
for child in MIP.getchildren():
	label        = child.get('label') or ""
	status       = child.get('status') or ""
	title        = child.get('title') or ""
	uid          = child.get('uid') or ""
	url          = child.get('url') or ""
	cmd = """insert into MIP values ("""+ \
		     "'" + label  + "'" + """, """ + \
		     "'" + status + "'" + """, """ + \
		     "'" + title  + "'" + """, """ + \
		     "'" + uid    + "'" + """, """ + \
		     "'" + url    + "'" + """) """
	c.execute(cmd)
	conn.commit()

c.close()

