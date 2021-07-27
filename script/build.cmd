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
set temp=temp
if "%version%"=="" (
    set zip_file=%addon_name%.zip
) else (
    set zip_file=%addon_name%-%version%.zip
)

@REM Move to the root and make directories
cd %~dp0..
if exist %temp% rm -rd %temp%
mkdir %temp%\%addon_name%

@REM Copy the files
for %%G in (%components%) do cp -r %%G %temp%\%addon_name%\

@REM Create the ZIP file
tar -C %temp% -acf %zip_file% %addon_name%

@REM Remove the temporary directory and return the ZIP file name
rm -rd %temp%
if exist %zip_file% echo %zip_file%
