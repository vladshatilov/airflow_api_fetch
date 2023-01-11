#!/bin/bash

#Init the airflow connections

echo "Adding source connections in Airflow"

# replacing env variables in connections.yaml with real connections
rm -f connections_filled.yaml temp.yaml
( echo "cat <<EOF >connections_filled.yaml";
  cat connections.yaml;
  echo "EOF";
) >temp.yaml
. temp.yaml


# creating connections
python3 connections.py

# removing connections.yaml
rm -f connections_filled.yaml temp.yaml