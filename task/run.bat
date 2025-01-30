@echo off
setlocal

for %%I in ("%~f0\..\..") do (
    set "TASK=%%~fI\task"
)

powershell -ExecutionPolicy Bypass -File "%TASK%\run.ps1"

endlocal