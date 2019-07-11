#!/bin/bash

# Purpose of this script:
# 1. Prepare files for neo4j-import command

if [ $# -eq 0 ]
  then
    echo "Provide path to data folder"
    exit 1
fi

DATA_DIR="$1"
TIMESTAMP=`basename $DATA_DIR`
OUTPUT_DIR=$PWD/output/orientdb/$TIMESTAMP

if [ ! -d $OUTPUT_DIR ]; then
  mkdir -p $OUTPUT_DIR/{data,import,backup,etl}

  TRANSACTIONS_HEADER="id|source|target|date|time|amount|currency"
  ATMS_HEADER="id|latitude|longitude"
  CLIENTS_HEADER="id|first_name|last_name|age|email|occupation|political_views|nationality|university|academic_degree|address|postal_code|country|city"
  COMPANIES_HEADER="id|type|name|country"

  echo $TRANSACTIONS_HEADER >> $OUTPUT_DIR/import/transactions.csv
  for transactions in `ls $DATA_DIR/nodes.transactions.*`; do
    cat $transactions >> $OUTPUT_DIR/import/transactions.csv
  done

  sed -i.bak "1 s/.*/$TRANSACTIONS_HEADER/" $OUTPUT_DIR/import/transactions.csv

  cp $DATA_DIR/nodes.atms.csv $OUTPUT_DIR/import/atms.csv
  sed -i.bak "1 s/.*/$ATMS_HEADER/" $OUTPUT_DIR/import/atms.csv

  cp $DATA_DIR/nodes.clients.csv $OUTPUT_DIR/import/clients.csv
  sed -i.bak "1 s/.*/$CLIENTS_HEADER/" $OUTPUT_DIR/import/clients.csv

  cp $DATA_DIR/nodes.companies.csv $OUTPUT_DIR/import/companies.csv
  sed -i.bak "1 s/.*/$COMPANIES_HEADER/" $OUTPUT_DIR/import/companies.csv

  rm $OUTPUT_DIR/import/*.bak

  cp $PWD/scripts/orientdb/*.json $OUTPUT_DIR/etl/
else
  echo "OrientDB files are already generated"
fi

read -p "Do you want to start OrientDB service (docker image, see script in ./scripts/orientdb/start.sh)?[Yn]" -n 1 -r
if [[ $REPLY =~ ^[Nn]$ ]]; then
  exit 0;
fi
echo
$PWD/scripts/orientdb/start.sh $DATA_DIR