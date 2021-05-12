#!/bin/bash

# Purpose of this script:
# 1. Import files to neo4j
# 2. Start neo4j instance

if [ $# -eq 0 ]
  then
    echo "Provide path to data folder"
    exit 1
fi

DATA_DIR="$1"
TIMESTAMP=`basename $DATA_DIR`
OUTPUT_DIR=$PWD/output/neo4j/$TIMESTAMP

# clean up for fresh import
# This is due to some changes in version 4.x
# Details can be found here: 
# https://phpboyscout.uk/pre-populating-neo4j-using-kubernetes-init-containers-and-neo4j-admin-import/
rm -rf $OUTPUT_DIR/data/databases/*
rm -rf $OUTPUT_DIR/data/transactions/*

echo "Starting Neo4J import"

#modified syntax because of v4.x
docker run \
  -v $OUTPUT_DIR/data:/data \
  -v $OUTPUT_DIR/import:/import \
  neo4j:latest \
    bin/neo4j-admin import --database=neo4j\
    	--nodes=ATMS=/import/atms.csv \
    	--nodes=Clinets=/import/clients.csv \
    	--nodes=Companies=/import/companies.csv \
      	--relationships=/import/transactions.csv \
      	--delimiter="|"

echo "Starting Neo4J instance"
docker run \
  -p 7474:7474 -p 7687:7687 \
  -v $OUTPUT_DIR/data:/data \
  -v $OUTPUT_DIR/import:/import \
  --env NEO4J_AUTH=none \
  neo4j:latest
