@echo off
REM Find deeply nested src directory and run models
setlocal enabledelayedexpansion

if "%1"=="" (
    echo Usage: run_model_smart.bat [model] [args...]
    echo.
    echo Available models:
    echo   kanet      - KA-Net
    echo   nighttime  - Nighttime Dehaze
    echo   orama      - ORAMA
    echo   daclip     - DACLiP
    echo.
    echo Examples:
    echo   run_model_smart.bat kanet
    echo   run_model_smart.bat nighttime
    exit /b 0
)

REM Find src directory
for /r . %%D in (.) do (
    if exist "%%D\src\ka_net" (
        set "SRC_DIR=%%D\src"
        goto :found
    )
    if exist "%%D\src\nighttime" (
        set "SRC_DIR=%%D\src"
        goto :found
    )
)

:found
if not defined SRC_DIR (
    echo Error: Could not find src directory
    exit /b 1
)

echo Found src at: %SRC_DIR%

set MODEL=%1
set ARGS=%*
setlocal enabledelayedexpansion
set "ARGS=!ARGS:%MODEL% =!"

if /i "%MODEL%"=="kanet" (
    echo Running KA-Net...
    cd /d "%SRC_DIR%\ka_net\testcode"
    python KA_net_test.py !ARGS!
    exit /b !ERRORLEVEL!
)

if /i "%MODEL%"=="nighttime" (
    echo Running Nighttime Dehaze...
    cd /d "%SRC_DIR%\nighttime"
    python main_test.py !ARGS!
    exit /b !ERRORLEVEL!
)

if /i "%MODEL%"=="orama" (
    echo Running ORAMA...
    cd /d "%SRC_DIR%\orama"
    python inference.py !ARGS!
    exit /b !ERRORLEVEL!
)

if /i "%MODEL%"=="daclip" (
    echo Running DACLiP...
    cd /d "%SRC_DIR%\daclip"
    python predict.py !ARGS!
    exit /b !ERRORLEVEL!
)

echo Unknown model: %MODEL%
exit /b 1
