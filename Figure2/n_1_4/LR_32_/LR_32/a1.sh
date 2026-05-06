#!/bin/bash

# Directory containing the files
DIR="."  # Change to your directory if needed

# Loop over all matching files
for file in "$DIR"/cv_J*_Nsample*.txt; do
    # Skip if no files match
    [ -e "$file" ] || continue

    # Extract the basename
    base=$(basename "$file")

    # Extract the J value (handles decimals)
    # cv_J0.1_Nsample.txt → extract 0.1
    Jval=$(echo "$base" | sed -E 's/cv_J([0-9.]+)_Nsample.*\.txt/\1/')

    # Calculate new J value with 4 decimal places
    newJ=$(echo "scale=4; $Jval*3.9/4.67" | bc)

    # Replace old J value in the filename with the new one
    newfile=$(echo "$base" | sed -E "s/J[0-9.]+/J$newJ/")

    # Rename the file
    echo "Renaming '$file' → '$newfile'"
    mv "$file" "$DIR/$newfile"
done
