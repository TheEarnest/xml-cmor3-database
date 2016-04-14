#!/bin/env python
import sqlite3


# ====================================================================
#      CMOR3Table
# ====================================================================
class CMOR3Table:
    '''
    API to read XML and Amon Table
    '''
    # --------------------------------------------------------------------
    #      __init__()
    # --------------------------------------------------------------------
    def __init__(self):
        '''
        '''
        conn = sqlite3.connect('./CMIP6.sql3')
        self.c = conn.cursor()

    # --------------------------------------------------------------------
    #      getMIPs()
    # --------------------------------------------------------------------
    def getMIPs(self):
        '''
        Extract all MIPs
        '''
        cmd = """select DISTINCT m.label from MIP m;"""
        self.c.execute(cmd)
        MIPS = self.c.fetchall()
        return MIPS

    # --------------------------------------------------------------------
    #      getActivity()
    # --------------------------------------------------------------------
    def getActivities(self):
        """
        Return a list of controled vocabulary for activity_id
        """
        cmd = """select distinct label,title
                from vocab_activity
                order by label;"""
        self.c.execute(cmd)
        activities = self.c.fetchall()
        return activities

    # --------------------------------------------------------------------
    #      getInstitutions()
    # --------------------------------------------------------------------
    def getInstitutions(self):
        """
        Return a list of controled vocabulary for CMIP6 Institutions
        """
        cmd = """select distinct label,title
                from vocab_institute
                order by label;"""
        self.c.execute(cmd)
        institutions = self.c.fetchall()
        return institutions

    # --------------------------------------------------------------------
    #      getModels()
    # --------------------------------------------------------------------
    def getModels(self):
        """
        Return a list of controled vocabulary for CMIP6 Models
        """
        cmd = """select distinct label
                from vocab_model
                order by label;"""
        self.c.execute(cmd)
        models = self.c.fetchall()
        return models

    # --------------------------------------------------------------------
    #      getAllExperiment()
    # --------------------------------------------------------------------
    def getAllExperiment(self):
        """
        Return a list of all experiment and description
        """
        cmd = """select distinct mip,label,description
                from experiment
                order by mip;"""
        self.c.execute(cmd)
        experiments = self.c.fetchall()
        return experiments

    # --------------------------------------------------------------------
    #      getExperimentGroups()
    # --------------------------------------------------------------------
    def getExperimentGroups(self, MIP):
        '''
        Retrieve Experiment Groups and Experiments requested by a MIP
        '''
        # sqlite> select DISTINCT eg.label,
        # eg.uid from exptGroup eg, requestItem ri
        # where ri.mip='CFMIP' and ri.esid = eg.uid order by eg.label;

        cmd = """select DISTINCT eg.uid
               from exptGroup eg,
                requestItem ri
               where  ri.mip='""" + MIP + """' and
                  eg.uid=ri.esid
           order by eg.label;"""
        self.c.execute(cmd)
        ExptGroups = self.c.fetchall()
        return ExptGroups

    # --------------------------------------------------------------------
    #      getExperimentGroupUID()
    # --------------------------------------------------------------------
    def getExperimentGroupUID(self, Label):
        '''
        Retrive Experiment Group UID from Label
        '''
        cmd = """select DISTINCT eg.uid
            from exptGroup eg
            where  eg.label='""" + Label + """';"""

        self.c.execute(cmd)
        ExptGroupUID = self.c.fetchall()
        return ExptGroupUID[0][0]

    # --------------------------------------------------------------------
    #     getExperimentGroupLabel()
    # --------------------------------------------------------------------
    def getExperimentGroupLabel(self, exptGroupUID):
        '''
        Retrieve Experiment Groups Label
        '''
        cmd = """select DISTINCT eg.label
            from exptGroup eg
            where  eg.uid='""" + exptGroupUID + """';"""

        self.c.execute(cmd)
        ExptGroupLabel = self.c.fetchall()
        return ExptGroupLabel[0][0]

    # --------------------------------------------------------------------
    #      getExperimentLabel()
    # --------------------------------------------------------------------
    def getExperimentLabel(self, experimentUID):
        '''
        Retrieve Experiment Label
        '''
        cmd = """select DISTINCT ex.label
            from experiment ex
            where  ex.uid='""" + experimentUID + """';"""

        self.c.execute(cmd)
        ExptGroupLabel = self.c.fetchall()
        return ExptGroupLabel[0][0]

    # --------------------------------------------------------------------
    #      getExperimentUID()
    # --------------------------------------------------------------------
    def getExperimentUID(self, experimentLabel):
        '''
        Retrieve Experiment Identifier
        '''
        cmd = """select DISTINCT ex.uid
            from experiment ex
            where  ex.label='""" + experimentLabel + """';"""

        self.c.execute(cmd)
        ExptGroupUID = self.c.fetchall()
        return ExptGroupUID[0][0]

    # --------------------------------------------------------------------
    #      getExperimentsbyExptGroupID()
    # --------------------------------------------------------------------
    def getExperimentsbyExptGroupID(self, exptGroupUID, MIP):
        '''
        Retrieve experiments from an experiment group ID.
        '''
        # sqlite> select DISTINCT ex.label from requestItem ri,
        # experiment ex, exptGroup eg where ex.mip='CFMIP' and
        # eg.uid=ex.egid and eg.uid=ri.esid and eg.label='Cfmip4' order by eg.label;

        exptGroupLabel = self.getExperimentGroupLabel(exptGroupUID)
        cmd = """select DISTINCT ex.uid
            from exptGroup eg,
                 experiment ex,
                 requestItem ri
            where ex.mip='""" + MIP + """' and
                  eg.uid = ex.egid and
                  eg.uid = ri.esid and
                  eg.label = '""" + exptGroupLabel + """'
            order by eg.label"""
        self.c.execute(cmd)
        Experiments = self.c.fetchall()
        return Experiments

    # --------------------------------------------------------------------
    #      getExperimentsbyExptGroupLabel()
    # --------------------------------------------------------------------
    def getExperimentsbyExptGroupLabel(self, exptGrpLabel, MIP):
        '''
        Retrieve experiments from an experiment group Label.
        '''
        #sqlite> select DISTINCT ex.label from requestItem ri, experiment ex, exptGroup eg where ex.mip='CFMIP' and eg.uid=ex.egid and eg.uid=ri.esid and eg.label='Cfmip4' order by eg.label;

        exptGroupUID = self.getExperimentGroupUID(exptGrpLabel)
        cmd = """select DISTINCT ex.label
            from exptGroup eg,
                 experiment ex,
                 requestItem ri
            where ex.mip='""" + MIP + """' and
                  eg.uid = """ + exptGroupUID + """ and
                  eg.uid = ri.esid and
                  eg.label = '""" + exptGrpLabel + """'
            order by eg.label"""
        self.c.execute(cmd)
        Experiments = self.c.fetchall()
        return Experiments

    # --------------------------------------------------------------------
    #      getGrid()
    # --------------------------------------------------------------------
    def getGrid(self, structureID):
        '''
        Retrieve structure grid from stid
        '''
        cmd = "select s.spid,s.tmid,s.cell_measures, s.cell_methods from structure s where s.uid == '" + structureID + "';"
        self.c.execute(cmd)
        data = self.c.fetchone()
        return data

    # --------------------------------------------------------------------
    #      getSpatialShape()
    # --------------------------------------------------------------------
    def getSpatialShape(self, spatialID):
        '''
        Retrieve XYZ grid from spatialShape table

        Return dimensions, levelFlag and levels
        '''
        # ----------------------
        # Extract Spatial dimension
        # ----------------------
        cmd = "select ss.dimensions, ss.levelFlag, ss.levels from spatialShape ss where ss.uid == '" + spatialID + "';"
        self.c.execute(cmd)
        spatial = self.c.fetchone()
        return spatial

    # --------------------------------------------------------------------
    #      getTemporalShape()
    # --------------------------------------------------------------------
    def getTemporalShape(self, spatialID):
        '''
        Retrieve time dimension from temporalShape table

        return dimension and label
        '''
        # ----------------------
        # Extract Time dimension
        # ----------------------
        cmd = "select ts.dimensions, ts.label from temporalShape ts where ts.uid == '" + spatialID + "';"
        self.c.execute(cmd)
        temporal = self.c.fetchone()
        return temporal

    # --------------------------------------------------------------------
    #      getVariables()
    # --------------------------------------------------------------------
    def getVariables(self, MIP, exptGroupLabel, experimentLabel):
        '''
        Get all variables requested by an experiment group

        return GridUID, label, frequency, mipTable, modeling_real,
               ok_max_mean_abs, ok_min_mean_abs, positive, valid_max,
               valid_min, group_label, experiment_label.
        '''
        exptGroupUID = self.getExperimentGroupUID(exptGroupLabel)
        exptUID      = self.getExperimentUID(experimentLabel)
        cmd = """select DISTINCT v.stid,
                       v.label,
                       v.frequency,
                       v.mipTable,
                       v.modeling_realm,
                       v.ok_max_mean_abs,
                       v.ok_min_mean_abs,
                       v.positive,
                       v.valid_max,
                       v.valid_min,
                       eg.label,
                       ex.label
                from experiment ex,
                     exptGroup eg,
                     requestVar rv,
                     requestVarGroup rvg,
                     requestItem ri,
                     requestlink rl,
                     CMORvar v
                where  rl.mip='""" + MIP + """'  and
                       eg.uid='""" + exptGroupUID + """' and
                       ex.uid='""" + exptUID + """' and
                       eg.uid=ri.esid and
                       ri.rlid=rl.uid   and
                       rl.refid=rvg.uid and
                       rvg.uid=rv.vgid  and
                       v.uid=rv.vid
                order by eg.label,ex.label;"""
        self.c.execute(cmd)
        variables = self.c.fetchall()
        return variables

    # --------------------------------------------------------------------
    #      getFormulaVars()
    # --------------------------------------------------------------------
    def getFormulaVars(self):
        '''
        Return all formula variables
        '''
        cmd = """select DISTINCT  fv.name,
                                  fv.long_name,
                                  fv.type,
                                  fv.dimension,
                                  fv.units
                 from formulaVar fv
            """
        self.c.execute(cmd)
        formulaVars = self.c.fetchall()

        return formulaVars

    # --------------------------------------------------------------------
    #      getVarFromMipTable()
    # --------------------------------------------------------------------
    def getVarFromMipTable(self, mipTable, MIP):
        '''
        Return all variables from a provenance (Amon,Omon,...) for a selecte MIP
        '''
        cmd = """select DISTINCT  v.label,
                                v.frequency,
                                v.mipTable,
                                v.modeling_realm,
                                v.ok_max_mean_abs,
                                v.ok_min_mean_abs,
                                v.positive,
                                v.valid_max,
                                v.valid_min,
                                ss.dimensions,
                                ts.dimensions,
                                st.cell_measures,
                                st.cell_methods,
                                vv.units,
                                vv.sn,
                                v.type,
                                vv.description,
                                v.title,
                                st.odims,
                                st.coords
                from exptGroup eg,
                    requestVar rv,
                    requestVarGroup rvg,
                    requestItem ri,
                    requestlink rl,
                    spatialShape ss,
                    temporalShape ts,
                    structure st,
                    CMORvar v,
                    var vv
                where rl.mip like '%""" + MIP + """%' and
                      eg.uid=ri.esid and
                      ri.rlid=rl.uid and
                      rl.refid=rvg.uid and
                      rvg.uid=rv.vgid  and
                      v.stid = st.uid and
                      st.spid = ss.uid and
                      st.tmid = ts.uid and
                      v.uid=rv.vid and
                      v.vid=vv.uid and
                      v.mipTable='""" + mipTable + """'
                order by eg.label;"""
        self.c.execute(cmd)
        variables = self.c.fetchall()

        return variables

    # --------------------------------------------------------------------
    #      getAxesGrids()
    # --------------------------------------------------------------------
    def getAxesGrids(self):
        '''
        Return all axes for CMIP grids table
        '''
        cmd = """ select ae.name,
                       ae.axis,
                       ae.long_name,
                       ae.out_name,
                       ae.standard_name,
                       ae.type,
                       ae.units,
                       ae.valid_min,
                       ae.valid_max
                from axisEntry ae
                where origin = 'grid';"""

        self.c.execute(cmd)
        axes = self.c.fetchall()

        return axes

    # --------------------------------------------------------------------
    #      getVarGrids()
    # --------------------------------------------------------------------
    def getVarGrids(self):
        '''
        Return all variables for CMIP grids table
        '''
        cmd = """select DISTINCT v.label,
                               var.sn,
                               var.units,
                               v.title,
                               ss.dimensions,
                               v.label,
                               v.valid_min,
                               v.valid_max
               from CMORvar v,
                    structure st,
                    spatialShape ss,
                    var
               where st.uid = v.stid
                     and ss.uid = st.spid
                     and v.vid=var.uid
                     and v.mipTable like '%grids%'"""
        self.c.execute(cmd)
        variables = self.c.fetchall()

        return variables

    # --------------------------------------------------------------------
    #      getVarProvenance()
    # --------------------------------------------------------------------
    def getVarProvenance(self, prov, MIP):
        '''
        Return all variables from a provenance (Amon,Omon,...) for a selecte MIP
        '''
        cmd = """select DISTINCT  v.label,
                                v.frequency,
                                v.mipTable,
                                v.modeling_realm,
                                v.ok_max_mean_abs,
                                v.ok_min_mean_abs,
                                v.positive,
                                v.valid_max,
                                v.valid_min,
                                ss.dimensions,
                                ts.dimensions,
                                st.cell_measures,
                                st.cell_methods,
                                vv.units,
                                vv.sn,
                                v.type,
                                vv.description,
                                v.title
                from experiment ex,
                    exptGroup eg,
                    requestVar rv,
                    requestVarGroup rvg,
                    requestItem ri,
                    requestlink rl,
                    spatialShape ss,
                    temporalShape ts,
                    structure st,
                    CMORvar v,
                    var vv
                where rl.mip like '%""" + MIP + """%' and
                      eg.uid=ri.esid and
                      ri.rlid=rl.uid and
                      ri.tab='""" + prov + """' and
                      rl.refid=rvg.uid and
                      rvg.uid=rv.vgid  and
                      v.stid = st.uid and
                      st.spid = ss.uid and
                      st.tmid = ts.uid and
                      v.uid=rv.vid and
                      v.vid=vv.uid
                order by eg.label,ex.label;"""
        self.c.execute(cmd)
        variables = self.c.fetchall()

        return variables

    # --------------------------------------------------------------------
    #      getAxis()
    # --------------------------------------------------------------------
    def getAxis(self, axis):
        '''
        Return Axis information from axisEntry
        '''
        cmd = """select * from axisEntry ae
                where ae.name ='""" + axis + """';"""
        self.c.execute(cmd)
        axis = self.c.fetchall()
        return axis

    # --------------------------------------------------------------------
    #      getAllAxes()
    # --------------------------------------------------------------------
    def getAxes(self):
        '''
        Return all available axes
        '''
        cmd = """select name,
                        axis,
                        climatology,
                        formula,
                        long_name,
                        must_have_bounds,
                        out_name,
                        positive,
                        requested,
                        requested_bounds,
                        standard_name,
                        stored_direction,
                        tolerance,
                        type,
                        units,
                        valid_min,
                        valid_max,
                        value,
                        z_bounds_factors,
                        z_factors,
                        bounds_values
                 from axisEntry
                 where origin != 'grid';"""
        self.c.execute(cmd)
        axes = self.c.fetchall()
        return axes

    # --------------------------------------------------------------------
    #      convertVarStructureToDictionary()
    # --------------------------------------------------------------------
    def convertVarStructureToDictionary(self, variable):
        '''
           Take a variable query result and convert it to a dictionary
        '''
        varDict = {'gridID':            variable[0],
                   'label':             variable[1],
                   'frequency':         variable[2],
                   'mipTable':          variable[3],
                   'modeling_realm':    variable[4],
                   'ok_max_mean_abs':   variable[5],
                   'ok_min_mean_abs':   variable[6],
                   'positive':          variable[7],
                   'valid_max':         variable[8],
                   'valid_min':         variable[9],
                   'exptGroupLabel':    variable[10],
                   'experimentLabel':   variable[11]
                   }
        return varDict

    def close(self):
            self.c.close()
