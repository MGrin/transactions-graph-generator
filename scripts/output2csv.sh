#!/bin/bash

# Purpose of this script:
# 1. Shuffle transactions and store them in one .csv file
# 2. Copy 4 .csv files into output folder

if [ $# -eq 0 ]; then
  echo "Provide path to data folder"
  exit 1
fi

DATA_DIR="$1"
TIMESTAMP=`basename $DATA_DIR`
OUTPUT_DIR=$PWD/output/csv/$TIMESTAMP

if [ -d $OUTPUT_DIR ]; then
  echo "CSV files are already generated"
  exit 0
fi

mkdir -p $OUTPUT_DIR

echo "id|source|target|date|time|amount|currency" >> $OUTPUT_DIR/transactions.csv

perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' < $DATA_DIR/nodes.transactions.patterns.circular.csv >> $OUTPUT_DIR/transactions.csv
perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' < $DATA_DIR/nodes.transactions.patterns.flow.csv >> $OUTPUT_DIR/transactions.csv
cat $DATA_DIR/nodes.transactions.client-sourcing.csv >> $OUTPUT_DIR/transactions.csv
perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' < $DATA_DIR/nodes.transactions.company-sourcing.csv >> $OUTPUT_DIR/transactions.csv
perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' < $DATA_DIR/nodes.transactions.patterns.time.csv >> $OUTPUT_DIR/transactions.csv

cp $DATA_DIR/nodes.atms.csv $OUTPUT_DIR/atms.csv
cp $DATA_DIR/nodes.clients.csv $OUTPUT_DIR/clients.csv
cp $DATA_DIR/nodes.companies.csv $OUTPUT_DIR/companies.csv
