#!/usr/bin/env bash
SQLITE3=${SQLITE3:-sqlite3}
CMIP6DB=${CMIP6DB:-CMIP6.sql3}

for realm in $(${SQLITE3} "${CMIP6DB}" \
                'select distinct mipTable from CMORvar'); do
    filename="CMIP6_${realm}.json"
    echo $filename
    cp /tmp/$filename .
    cp $filename /software/cmor3/cmor/Tables/
    cp $filename /software/cmip6-cmor-tables/Tables
done
for filename in CMIP6_coordinate.json CMIP6_formula_terms.json; do 
    cmd="cp /tmp/$filename ."
    echo $cmd
    $cmd
    cmd="cp /tmp/$filename /software/cmor3/cmor/Tables/"
    echo $cmd
    $cmd
    cmd="cp /tmp/$filename /software/cmip6-cmor-tables/Tables"
    echo $cmd
    $cmd
done
exit 0
