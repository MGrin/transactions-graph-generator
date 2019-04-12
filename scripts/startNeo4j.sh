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

echo "Starting Neo4J import"

docker run \
  -v $OUTPUT_DIR/data:/data \
  -v $OUTPUT_DIR/import:/import \
  neo4j:latest \
    bin/neo4j-admin import \
      --nodes:ATMs /import/atms.csv \
      --nodes:Clients /import/clients.csv \
      --nodes:Companies /import/companies.csv \
      --relationships /import/transactions.csv \
      --delimiter "|"

echo "Starting Neo4J instance"
docker run \
  -p 7474:7474 -p 7687:7687 \
  -v $OUTPUT_DIR/data:/data \
  -v $OUTPUT_DIR/import:/import \
  --env NEO4J_AUTH=none \
  neo4j:latest