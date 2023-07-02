@echo off
title Daniela AI Server
mode con cols=80 lines=20
color b
echo.
echo  Daniela AI starting...
echo  github.com/stephan-hp
echo.
cd /d "%~dp0"
del /s /q .\virtual\pyvenv.cfg

echo home = %USERPROFILE%\AppData\Local\Programs\Python\Python38>>.\virtual\pyvenv.cfg
echo implementation = CPython>>.\virtual\pyvenv.cfg
echo version_info = 3.8.0.final.0>>.\virtual\pyvenv.cfg
echo virtualenv = 20.23.1>>.\virtual\pyvenv.cfg
echo include-system-site-packages = false>>.\virtual\pyvenv.cfg
echo base-prefix = %USERPROFILE%\AppData\Local\Programs\Python\Python38>>.\virtual\pyvenv.cfg
echo base-exec-prefix = %USERPROFILE%\AppData\Local\Programs\Python\Python38>>.\virtual\pyvenv.cfg
echo base-executable = %USERPROFILE%\AppData\Local\Programs\Python\Python38\python.exe>>.\virtual\pyvenv.cfg

call .\virtual\Scripts\activate.bat
python daniela.py 
