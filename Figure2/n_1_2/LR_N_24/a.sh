#!/bin/bash

DIR="."  # change if needed

for file in "$DIR"/cv_J*_Nsample.txt; do
    base=$(basename "$file")

    # Extract J value (e.g., 0.3 from cv_J0.3_Nsample.txt)
    Jval=$(echo "$base" | sed -E 's/cv_J([0-9.]+)_Nsample\.txt/\1/')

    # Compute new J
    newJ=$(echo "scale=4; $Jval*3.9/4.67" | bc)

    # Build new filename
    newfile=$(echo "$base" | sed -E "s/J[0-9.]+/J$newJ/")

    echo "Renaming $file → $newfile"
    mv "$file" "$DIR/$newfile"
done
