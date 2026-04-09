@echo off
title sindhu.s - Portfolio Server
color 5F
echo.
echo  ============================================
echo    sindhu.s  ^|  Portfolio Server
echo  ============================================
echo.

echo  Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  ERROR: Python is not installed!
    echo  Please install Python from https://python.org
    pause
    exit /b 1
)

echo  Checking Flask...
pip show flask >nul 2>&1
if %errorlevel% neq 0 (
    echo  Installing Flask...
    pip install flask flask-cors
)

echo.
echo  Server starting...


echo  Your browser will open automatically.
echo.
echo  Portfolio:  http://localhost:5000
echo  Admin:      http://localhost:5000/admin
echo.
echo  Keep this window open while using the site.
echo  Press Ctrl+C to stop the server.
echo  ============================================
echo.

cd /d "%~dp0"

REM Open browser after 2 seconds
start /b cmd /c "timeout /t 2 >nul && start http://localhost:5000"

python server.py
pause
