#!/bin/bash
# Copy the files as shown in the output of fill_dot_checker.sh into icons/ in the current directory
# Usage: ./copier.sh <fill_dot_checker.sh's output text file>"
# Example: ./copier.sh report.txt

# Argument checker
if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <fill_dot_checker.sh's output text file>"
    exit 1
fi

files=$(awk -F ': ' '{print $2}' $1)

while IFS= read -r file; do
    # Copy each file to the current directory
    mkdir -p ./icons
    cp "$file" ./icons
done <<< "$files"
