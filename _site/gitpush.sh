#!/bin/bash

# Check if commit message is provided
if [ -z "$1" ]; then
  echo "Error: Commit message is required."
  echo "Usage: ./gitpush.sh 'commit message'"
  exit 1
fi

# Assign the commit message to a variable
message="$1"

# Perform git operations
git add .
git commit -m "$message"
git push
