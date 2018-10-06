#!/bin/bash

set -e

if [ "$#" -ne 1 ]; then
  echo "Usage: $(basename $0) <data-dir>"
  exit 1
fi

DATA_DIR=$1

find $DATA_DIR -type f -name "*.csv" \
  | xargs -t -P 4 -I {} sh -c "python pkg/london_crime.py {}" 2>&1
