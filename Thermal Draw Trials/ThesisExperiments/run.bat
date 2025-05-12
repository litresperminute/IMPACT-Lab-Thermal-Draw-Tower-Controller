@echo off
setlocal

:: Step 1: Optional dependency install
echo --------------------------------------
echo Do you want to install required Python packages?
echo (Recommended if this is your first time running the tool)
echo.
echo [Y] Yes, install dependencies now
echo [S] Skip and go to menu
echo.

set /p depchoice=Install dependencies? (Y/S): 
if /I "%depchoice%"=="Y" (
    if exist requirements.txt (
        echo Installing dependencies from requirements.txt...
        pip install -r requirements.txt
        if errorlevel 1 (
            echo Failed to install packages. Please ensure Python and pip are installed.
            pause
            exit /b
        )
    ) else (
        echo requirements.txt not found. Skipping installation.
    )
)

:: Step 2: Menu
:MENU
echo --------------------------------------
echo      Thesis Experiment Logger Menu
echo --------------------------------------
echo.
echo [1] Run drawlogger (start a new experiment)
echo [2] View experiment summary table
echo [3] Generate metadata for legacy files
echo [4] Plot a single experiment
echo [5] Compare multiple draw trials
echo [Q] Quit
echo.

set /p choice=Choose an option (1-5 or Q): 
if "%choice%"=="1" python drawlogger.py
if "%choice%"=="2" python summarize_metadata.py
if "%choice%"=="3" python generate_metadata_for_legacy_logs.py
if "%choice%"=="4" python plot_single_experiment.py
if "%choice%"=="5" python compare_draw_trials.py
if /I "%choice%"=="Q" exit

goto MENU
