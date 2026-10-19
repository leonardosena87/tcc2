@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\configure-startup.ps1"
if errorlevel 1 goto erro
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\start.ps1"
if errorlevel 1 goto erro
exit /b 0
:erro
pause
exit /b 1
