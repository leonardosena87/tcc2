@echo off
pushd "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "scripts\configure-word-autoopen.ps1" enable
if errorlevel 1 pause
popd
