#!/bin/bash

# Purpose of this script:
# 1. Import files to postgresql
# 2. Start postgresql instance

if [ $# -eq 0 ]
  then
    echo "Provide path to data folder"
    exit 1
fi

DATA_DIR="$1"
TIMESTAMP=`basename $DATA_DIR`
OUTPUT_DIR=$PWD/output/postgres/$TIMESTAMP
CSV_FILES_DIR=$PWD/output/csv/$TIMESTAMP

echo "NOT IMPLEMENTED YET"
exit 1
# echo "Starting Postgres import"
# docker run \
#   -v $OUTPUT_DIR/data:/var/lib/postgresql/data \
#   -v $CSV_FILES_DIR:/tmp/files \
#   -v $PWD/scripts/postgresql/initdb.d:/docker-entrypoint-initdb.d \
#   postgres:latest
