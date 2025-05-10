@echo off
setlocal enabledelayedexpansion

title Customer Churn Analysis Server Host
cd /d "%~dp0"

echo Checking for Python installation . . .
python --version >nul 2>&1
if !ERRORLEVEL! neq 0 (
    echo(
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/ or add Python to path and try again.
    goto END
)
echo(
echo Python installation found...
echo(
echo Activating the virtual environment...
if not exist "venv\Scripts\activate.bat" (
    echo(
    echo ERROR: Virtual environment not found at venv\Scripts\activate.bat.
    echo Please run the "venv_creator.bat" file first and then run this file. 
    goto END
)
call venv\Scripts\activate
if !ERRORLEVEL! neq 0 (
    echo(
    echo ERROR: Failed to activate virtual environment. Make sure the virtual environment folder exists. 
    echo Please run the "venv_creator.bat" file first and then run this file.
    goto END
)
echo(
echo Once the host is started you'll be redirected to the webpage. 
echo(
set TEMP_OUTPUT=tmp\app_output.txt
python app.py 2>"%TEMP_OUTPUT%"
if !ERRORLEVEL! eq 0 (
    type "%TEMP_OUTPUT%"
) else (
    echo(
    echo ERROR: An error occurred while running app.py.
    echo Check the console output below for details:
    type "%TEMP_OUTPUT%"
    echo(
    echo Possible causes: missing dependencies, invalid dataset, or server issues.
    echo Log file app.log may contain more details.
    goto END
)

:END
echo(
echo Exiting the process . . .
echo(
pause
del "%TEMP_OUTPUT%"
exit /b 1
