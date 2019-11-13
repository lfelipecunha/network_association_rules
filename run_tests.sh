#!/bin/bash

i=0

echo "Cleanning data"
BASEDIR=$(dirname $0)

rm $BASEDIR/data_base/*
rm $BASEDIR/results/*

while [ $i -lt 100 ]; do
    echo "Starting running $((i+1))"
    echo "Generating synthetic data..."
    python3 src/synthetic_data_generator.py
    python3 src/main.py

    FALSES=$(grep 'F' results/accuracy.csv | wc -l)
    echo $FALSES >> results/tests.csv
    i=$((i+1))
    echo "=============================="
done

