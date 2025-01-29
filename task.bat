@echo off
setlocal

for %%I in ("%~f0\..") do (
    set "TSK=%%~fI\tsk"
)

powershell -ExecutionPolicy Bypass -File "%TSK%\task.ps1"

endlocal