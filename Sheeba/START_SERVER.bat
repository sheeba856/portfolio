@echo off
title Sheeba A - Portfolio Server
color 5F
echo.
echo  ============================================
echo    Sheeba A  ^|  Portfolio Server
echo  ============================================
echo.
echo  Checking for Flask...
pip show flask >nul 2>&1
if %errorlevel% neq 0 (
    echo  Installing required packages...
    pip install flask flask-cors
    echo.
)
echo  Starting server...
echo  Open browser at:  http://localhost:5000
echo  Admin panel:       http://localhost:5000/admin
echo.
echo  Press Ctrl+C to stop.
echo  ============================================
echo.
python server.py
pause
