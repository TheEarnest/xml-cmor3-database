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
exit 0
