#!/bin/bash

# Purpose of this script:
# 1. Prepare files for mongo-import command

if [ $# -eq 0 ]
  then
    echo "Provide path to data folder"
    exit 1
fi

DATA_DIR="$1"
TIMESTAMP=`basename $DATA_DIR`
OUTPUT_DIR=$PWD/output/postgres/$TIMESTAMP

echo "Generating default csv files"
$PWD/scripts/output2csv.sh $DATA_DIR

if [ ! -d $OUTPUT_DIR ]; then
  mkdir -p $OUTPUT_DIR/data
else
  echo "Postgres files are already generated"
fi

read -p "Do you want to start postgres service (docker image, see script in ./scripts/startPostgres.sh)?[Yn]" -n 1 -r
if [[ $REPLY =~ ^[Nn]$ ]]; then
  exit 0;
fi

$PWD/scripts/startPostgres.sh $DATA_DIR