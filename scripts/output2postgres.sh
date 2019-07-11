#!/bin/bash

# Purpose of this script:
# 1. Prepare files for postgres-import command

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

read -p "Do you want to start postgres service (docker image, see script in ./scripts/postgres/start.sh)?[Yn]" -n 1 -r
if [[ $REPLY =~ ^[Nn]$ ]]; then
  exit 0;
fi

$PWD/scripts/postgresql/start.sh $DATA_DIR
