@REM script/bootstrap: Resolve all dependencies the application requires to run.

@echo off

cd %~dp0..

where pipenv >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Command 'pipenv' not found. Aborting.
    exit 1
)

set PIPENV_VENV_IN_PROJECT=1
pipenv install --dev --skip-lock
