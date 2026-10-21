@echo off
setlocal enabledelayedexpansion

REM Get the base directory
set "BASE_DIR=%~dp0"
set "NESTED_PATH=%BASE_DIR%Windshield-Dehazing-AV\Windshield-Dehazing-AV\Windshield-Dehazing-AV\Windshield-Dehazing-AV\Windshield-Dehazing-AV\src"

if "%1"=="" (
    echo.
    echo ========================================
    echo  WINDSHIELD DEHAZING - Model Launcher
    echo ========================================
    echo.
    echo Usage: run_model.bat [model_name]
    echo.
    echo Available models:
    echo   run_model.bat orama        - ORAMA (Night Fog King)
    echo   run_model.bat kanet        - KA-Net (42 FPS Beast)
    echo   run_model.bat nighttime    - Nighttime Dehaze (Glare Master)
    echo   run_model.bat daclip       - DACLiP (Universal)
    echo.
    echo Examples:
    echo   run_model.bat orama
    echo   run_model.bat kanet
    echo.
    exit /b 0
)

REM If multiple model names are provided, run them sequentially
set "EXITCODE=0"
for %%M in (%*) do (
    set "MODEL=%%~M"
    if /i "!MODEL!"=="orama" (
        cd /d "%NESTED_PATH%\orama"
        echo Running ORAMA inference...
        python inference.py || set "EXITCODE=!ERRORLEVEL!"
    ) else if /i "!MODEL!"=="kanet" (
        cd /d "%NESTED_PATH%\ka_net\testcode"
        echo Running KA-Net test...
        python KA_net_test.py || set "EXITCODE=!ERRORLEVEL!"
    ) else if /i "!MODEL!"=="nighttime" (
        cd /d "%NESTED_PATH%\nighttime"
        echo Running Nighttime Dehaze...
        python main_test.py || set "EXITCODE=!ERRORLEVEL!"
    ) else if /i "!MODEL!"=="daclip" (
        cd /d "%NESTED_PATH%\daclip"
        echo Running DACLiP...
        python predict.py || set "EXITCODE=!ERRORLEVEL!"
    ) else (
        echo Error: Unknown model "!MODEL!"
        echo Run "run_model.bat" for usage instructions.
        set "EXITCODE=1"
    )
)

exit /b %EXITCODE%
