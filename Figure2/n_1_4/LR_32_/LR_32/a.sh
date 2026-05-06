#!/bin/bash

# Directory containing the files
DIR="."  # or replace with your directory

# Loop over all matching files
for file in "$DIR"/cv_J*_Nsample_*.txt; do
    # Extract the J value using parameter expansion
    base=$(basename "$file")
    # cv_J0.1_Nsample_200.txt → extract 0.1
    Jval=$(echo "$base" | sed -E 's/cv_J([0-9.]+)_Nsample_[0-9]+\.txt/\1/')
    
    # Calculate new J value with bc
    newJ=$(echo "scale=4; $Jval*3.9/4.67" | bc)
    
    # Build new filename
    newfile=$(echo "$base" | sed -E "s/J[0-9.]+/J$newJ/")
    
    # Rename file
    echo "Renaming $file → $newfile"
    mv "$file" "$DIR/$newfile"
done
