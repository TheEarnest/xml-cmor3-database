#!/usr/bin/env bash
#ARRAY=(3hr 6hrLev 6hrPlev 6hrPlevpt aerannual aerdaily aerfixed aerhourly aermonthly aero Amon AmonAdj CCMI1_hourly CCMI1_monthly cf3hr cfDay cfMon cfOff cfsites CORDEX_day day em em1hr em1hrclimmon em3hr em3hrpt emDay emDaypt emDayZ emFx emMon emMonclim emMonpt emMonZ emSubhr emYr fx LImon Lmon Oclim Oday Ofx Omon Oyr SIday SImon)
ARRAY=(3hr 6hrLev 6hrPlev 6hrPlevpt aerannual aerdaily aerfixed aerhourly aermonthly aero Amon AmonAdj cf3hr cfDay cfMon cfsites  day em3hr em3hrpt emDay  emDayZ emFx emMon  emMonZ emSubhr emYr fx LImon Lmon Oclim Oday Omon Oyr SImon)

for realm in ${ARRAY[@]}; do
    filename="CMIP6_${realm}.json"
    #echo "Creating: ${filename}"
    echo "python CMORCreateTable.py -r ${realm} -j  > /tmp/${filename}"
    echo "python CMORCreateTable.py -r ${realm} -j  > /tmp/${filename}" |sh
done
exit 0
