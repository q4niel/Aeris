@echo off
for %%i in (%~dp0..) do set "projDir=%%~fi"
py -B %projDir%/build/src/main.py 2 %projDir%