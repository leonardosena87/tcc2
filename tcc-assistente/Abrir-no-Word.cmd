@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\start.ps1"
if errorlevel 1 goto erro
pushd "%~dp0"
call npx.cmd office-addin-dev-settings sideload manifest.xml desktop --app Word
popd
if errorlevel 1 goto erro
exit /b 0
:erro
pause
