#!/bin/bash
# The bash version of the script provided in #1805
# Usage: ./fill_dot_checker.sh <Arcticons' root directory>
# Example: ./fill_dot_checker.sh ~/git/Arcticons > report.txt

# Argument checker
if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <Arcticons' root directory>"
    exit 1
fi

# Loop through the directory and do the deed
arcticons_dir=$1
for i in "$arcticons_dir"/icons/white/*.svg; do
	r=$(cat $i | grep -Po '<circle .*?>' | grep -o 'r="[0]*\.[0-9]*' | cut -c 4- | sed 's/^\./0./g' | head -n1 | grep -v "0.75")
	if [[ $r ]]; then
		echo $r : $i
	fi
done
