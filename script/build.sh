#!/bin/bash

# script/build: Packaging the required components for release.
#               Designed to run on the continuous integration server.
#
# INPUT
#     $1: The version number of the release.
#
# OUTPUT
#     Name of the release ZIP file.

# Exit immediately if an error occurs
set -e

# Go to the project directory
cd "$(dirname "$BASH_SOURCE")/.."

# Set some variables for ZIP file name
version="$1"
components=("__init__.py" "imagepaste" "LICENSE")
addon_name="ImagePaste"
if [ -z "$version" ]; then zip_name=$addon_name;
else zip_name="$addon_name-$version.zip"; fi

# Generate ZIP file
[ -d "$addon_name" ] && rm -rf "$addon_name"
mkdir "$addon_name"
cp -r $(echo ${components[@]} | xargs) "$addon_name"
[ -f "$zip_name" ] && rm -f "$zip_name"
zip -rmqq "$zip_name" "$addon_name"

# Return the name of the ZIP file
echo "$zip_name"
