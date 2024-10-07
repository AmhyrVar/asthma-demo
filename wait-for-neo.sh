#!/bin/bash

# Attendre que Neo4j soit prêt
until curl -s http://localhost:7474; do
  echo "En attente que Neo4j soit prêt..."
  sleep 5
done

# Exécuter le script kg-load.py
python kg-load.py
