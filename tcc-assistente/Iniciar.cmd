@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\start.ps1"
if errorlevel 1 pause
pushd "%~dp0"
call npx.cmd office-addin-dev-settings register manifest.xml
if errorlevel 1 goto erro
call npx.cmd office-addin-dev-settings sideload manifest.xml desktop --app Word
if errorlevel 1 goto erro
popd
exit /b 0
:erro
popd
pause
