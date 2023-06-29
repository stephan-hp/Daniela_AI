@echo off
title Daniela AI Server
mode con cols=80 lines=20
color b
echo.
echo  Daniela AI starting...
echo  github.com/stephan-hp
echo.
cd /d "%~dp0"
call .\virtual\Scripts\activate.bat
python daniela.py 