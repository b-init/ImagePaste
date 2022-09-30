#!/bin/bash

# script/build: Packaging the required components for release.
#               Designed to run on the continuous integration server.
#
# INPUT
#     $1: The suffix for the ZIP file name.
#
# OUTPUT
#     Name of the release ZIP file.

# Exit immediately if an error occurs
set -e

# Go to the project directory
cd "$(dirname "$BASH_SOURCE")/.."

# Set some variables for ZIP file name
components=("__init__.py" "imagepaste" "LICENSE")

suffix="$1"
addon_name="ImagePaste"
if [[ -z "$suffix" ]]; then
    zip_name=$addon_name
else
    zip_name="$addon_name-$suffix.zip"
fi

# Create a temporary directories
temporary_directory="$(mktemp -d)"
addon_directory="$temporary_directory/$addon_name"
mkdir "$addon_directory"

# Copy the required components to the created directory
for component in "${components[@]}"; do
    cp -r "$component" "$addon_directory"
done

# Generate ZIP file
root_directory="$(pwd)"
cd "$temporary_directory"
zip -rmqq "$root_directory/$zip_name" "$addon_name"
rm -rf "$temporary_directory"

# Return the name of the ZIP file
echo "$zip_name"
