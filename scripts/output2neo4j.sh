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
OUTPUT_DIR=$PWD/output/neo4j/$TIMESTAMP

if [ ! -d $OUTPUT_DIR ]; then
  mkdir -p $OUTPUT_DIR/{data,import}

  TRANSACTIONS_HEADER="id:string|source:START_ID|target:END_ID|date:date|time:time|amount:float|currency:string|:TYPE"
  ATMS_HEADER=":ID|latitude:float|longitude:float"
  CLIENTS_HEADER=":ID|first_name:LABEL|last_name:string|age:int|email:string|occupation:string|political_views:string|nationality:string|university:string|academic_degree:string|address:string|postal_code:string|country:string|city:string"
  COMPANIES_HEADER=":ID|type:string|name:LABEL|country:string"

  echo $TRANSACTIONS_HEADER >> $OUTPUT_DIR/import/transactions.csv
  for transactions in `ls $DATA_DIR/nodes.transactions.*`; do
    cat $transactions >> $OUTPUT_DIR/import/transactions.csv
  done

  sed -i.bak 's/$/|transaction/' $OUTPUT_DIR/import/transactions.csv
  sed -i.bak "1 s/.*/$TRANSACTIONS_HEADER/" $OUTPUT_DIR/import/transactions.csv

  cp $DATA_DIR/nodes.atms.csv $OUTPUT_DIR/import/atms.csv
  sed -i.bak "1 s/.*/$ATMS_HEADER/" $OUTPUT_DIR/import/atms.csv

  cp $DATA_DIR/nodes.clients.csv $OUTPUT_DIR/import/clients.csv
  sed -i.bak "1 s/.*/$CLIENTS_HEADER/" $OUTPUT_DIR/import/clients.csv

  cp $DATA_DIR/nodes.companies.csv $OUTPUT_DIR/import/companies.csv
  sed -i.bak "1 s/.*/$COMPANIES_HEADER/" $OUTPUT_DIR/import/companies.csv

  rm $OUTPUT_DIR/import/*.bak
else
  echo "Neo4j files are already generated"
fi

read -p "Do you want to start neo4j service (docker image, see script in ./scripts/neo4j/start.sh)?[Yn]" -n 1 -r
if [[ $REPLY =~ ^[Nn]$ ]]; then
  exit 0;
fi

$PWD/scripts/neo4j/start.sh $DATA_DIR
