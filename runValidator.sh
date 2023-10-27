#!/bin/bash

# Check if Python is installed
if ! [ -x "$(command -v python3)" ]; then
  echo 'Error: Python3 is not installed.' >&2
  exit 1
fi

# Check if pip is installed
if ! [ -x "$(command -v pip)" ]; then
  echo 'Error: pip is not installed.' >&2
  exit 1
fi

# Check if the validator directory exists
validator_dir="$PWD/validator"
if [ ! -d "$validator_dir" ]; then
  echo 'Error: The "validator" directory does not exist.' >&2
  exit 1
fi

requirements="$validator_dir/requirements.txt"
python3 -m pip install -r "$requirements"

validator_script="$validator_dir/validatexml-xsd.py"

python3 "$validator_script" "$@"
