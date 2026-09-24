@echo off
pushd "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "scripts\configure-word-autoopen.ps1" disable
if errorlevel 1 pause
popd
