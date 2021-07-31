@REM script/build: Packaging the required components for release.
@REM               Designed to run on the continuous integration server.
@REM
@REM INPUT
@REM     %1: The version number of the release.
@REM
@REM OUTPUT
@REM     Name of the release ZIP file.


@REM Disable the command prompt
@ECHO OFF

@REM Set some variables
SET version=%1
SET components=__init__.py imagepaste LICENSE
SET addon_name=ImagePaste
SET temp=temp
IF "%version%"=="" (
    SET zip_file=%addon_name%.zip
) ELSE (
    SET zip_file=%addon_name%-%version%.zip
)

@REM Move to the root and make directories
CD %~dp0..
IF EXIST %temp% RMDIR /S /Q %temp%
MKDIR %temp%\%addon_name%

@REM Copy the files and folders
FOR %%G IN (%components%) DO (
    IF EXIST %%G\NUL (
        ROBOCOPY %%G %temp%\%addon_name%\%%G /E >NUL
    ) ELSE (
        ROBOCOPY . %temp%\%addon_name% %%G >NUL
    )
)

@REM Create the ZIP file
tar -C %temp% -acf %zip_file% %addon_name%

@REM Remove the temporary directory and return the ZIP file name
RMDIR /S /Q %temp%
IF EXIST %zip_file% ECHO %zip_file%
