@REM script/bootstrap: Resolve all dependencies the application requires to run.

@ECHO OFF

CD %~dp0..

WHERE pipenv >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    ECHO Command 'pipenv' not found. Aborting.
    EXIT 1
)

SET PIPENV_VENV_IN_PROJECT=1
pipenv install --dev --skip-lock
