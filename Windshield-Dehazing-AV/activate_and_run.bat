@echo off
REM Activate virtual environment and run models
setlocal enabledelayedexpansion

set "BASE_DIR=%~dp0"

REM Activate venv
if exist "%BASE_DIR%.venv\Scripts\activate.bat" (
    echo [*] Activating virtual environment...
    call "%BASE_DIR%.venv\Scripts\activate.bat"
) else (
    echo [!] Virtual environment not found at %BASE_DIR%.venv
    echo [!] Please ensure you have created the venv with: python -m venv .venv
    exit /b 1
)

REM Now run python with the user's arguments
python -m run_model %*
exit /b !ERRORLEVEL!
