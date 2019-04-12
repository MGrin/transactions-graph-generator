#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "Provide path to data folder"
    exit 1
fi

DATA_DIR="$1"
TIMESTAMP=`basename $DATA_DIR`
OUTPUT_DIR=$PWD/output/$TIMESTAMP

rm -rf $OUTPUT_DIR
mkdir -p $OUTPUT_DIR

echo "id,source,target,date,time,amount,currency" >> $OUTPUT_DIR/transactions.csv

perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' < $DATA_DIR/nodes.transactions.patterns.circular.csv >> $OUTPUT_DIR/transactions.csv
perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' < $DATA_DIR/nodes.transactions.patterns.flow.csv >> $OUTPUT_DIR/transactions.csv
cat $DATA_DIR/nodes.transactions.client-sourcing.csv >> $OUTPUT_DIR/transactions.csv
perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' < $DATA_DIR/nodes.transactions.company-sourcing.csv >> $OUTPUT_DIR/transactions.csv
perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' < $DATA_DIR/nodes.transactions.patterns.time.csv >> $OUTPUT_DIR/transactions.csv

cp $DATA_DIR/nodes.atms.csv $OUTPUT_DIR/atms.csv
cp $DATA_DIR/nodes.clients.csv $OUTPUT_DIR/clients.csv
cp $DATA_DIR/nodes.companies.csv $OUTPUT_DIR/companies.csv
