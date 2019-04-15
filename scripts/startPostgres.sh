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

echo "POSTGRES IMPORT IS NOT IMPLEMENTED YET!"
exit 1
# echo "Starting Postgres import"
# docker run \
#   -v $OUTPUT_DIR/data:/var/lib/postgresql/data \
#   postgres:latest \
#     psql -c """
# CREATE TABLE atms(id: char(36), latitude: double precision, longitude: double precision);
# CREATE TABLE clients(id: char(36), first_name: text, last_name: text, age: integer, email: text, occupation: text, political_views: text, nationality: text, university: text, academic_degree: text, address: text, postal_code: integer, country: char(50), city: text);
# CREATE TABLE companies(id: char(36), type: text, name: text, country: char(50));
# CREATE TABLE transactions(id: char(36), source: char(36), target: char(36), date: char(10), time: char(10), amount: integer, currency: char(4));
#     """