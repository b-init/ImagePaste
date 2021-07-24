@REM script/build: Packaging the required components for release.
@REM               Designed to run on the continuous integration server.
@REM
@REM INPUT
@REM     %1: The version number of the release.
@REM
@REM OUTPUT
@REM     Name of the release ZIP file.


@REM Disable the command prompt
@echo off

@REM Set some variables
set version=%1
set components=__init__.py imagepaste LICENSE
set addon_name=ImagePaste
if "%version%"=="" (
    set zip_file=%addon_name%.zip
) else (
    set zip_file=%addon_name%-%version%.zip
)

@REM Move to the root and make directories
cd %~dp0..
if exist temp rm temp
mkdir temp
cd temp

@REM Copy the files
mkdir %addon_name%
for %%G in (%components%) do cp -r ..\%%G %addon_name%\

@REM Create the ZIP file
tar -cf %zip_file% %addon_name% && rm -rd %addon_name%

@REM Remove the temporary directory and return the ZIP file name
mv %zip_file% ..
cd ..
rmdir temp
echo %zip_file%
