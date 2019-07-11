#!/bin/bash

# Purpose of this script:
# 1. Import files to orientdb
# 2. Start orientdb instance

if [ $# -eq 0 ]
  then
    echo "Provide path to data folder"
    exit 1
fi

ORIENTDB_ROOT_PASSWORD="root"
DATA_DIR="$1"
TIMESTAMP=`basename $DATA_DIR`
OUTPUT_DIR=$PWD/output/orientdb/$TIMESTAMP

if [ ! -d "$OUTPUT_DIR/data/transactions" ]; then
  docker run \
    -e ORIENTDB_ROOT_PASSWORD=$ORIENTDB_ROOT_PASSWORD \
    -v $OUTPUT_DIR/etl:/etl \
    -v $OUTPUT_DIR/data:/orientdb/databases \
    -v $OUTPUT_DIR/import:/import \
    -v $OUTPUT_DIR/backup:/orientdb/backup \
      orientdb //orientdb/bin/console.sh "
CREATE DATABASE plocal:/orientdb/databases/transactions
"
fi

docker run -p 2424:2424 -p 2480:2480 \
  -e ORIENTDB_ROOT_PASSWORD=$ORIENTDB_ROOT_PASSWORD \
  -v $OUTPUT_DIR/etl:/etl \
  -v $OUTPUT_DIR/data:/orientdb/databases \
  -v $OUTPUT_DIR/import:/import \
  -v $OUTPUT_DIR/backup:/orientdb/backup \
    orientdb bash -c "
echo \"========IMPORT ATMS========\" &&
/orientdb/bin/oetl.sh /etl/atms.json &&
echo &&
echo &&

echo \"========IMPORT COMPANIES========\" &&
/orientdb/bin/oetl.sh /etl/companies.json &&
echo &&
echo &&

echo \"\n========IMPORT CLIENTS========\" &&
/orientdb/bin/oetl.sh /etl/clients.json &&
echo &&
echo &&

echo \"\n========IMPORT CLIENT SOURCING TRANSACTIONS========\" &&
/orientdb/bin/oetl.sh /etl/transactions.json &&
echo &&
echo &&

/orientdb/bin/server.sh
"