@echo off
setlocal enabledelayedexpansion
title 1559 Dependencies Installer

echo Finished Installing Dependencies
echo.
powershell timeout 1 >Nul
echo Do You Want To Remove Temporary Files? (y/n)
set /p remove=""
if "%remove%"=="" (call set remove=n)
if "%remove%"=="N" (call set remove=n)
if "%remove%"=="n" (call echo Leaving Temporary Files) else (call :remove)
echo Installer Has Finished
pause
move nul 2>&0
EXIT /B 0
:remove
	echo Removing Temporary Directory 
	set target=C:\tmp\1559-Dependency-Installer\
	powershell Remove-Item -Path %target% -Force -Recurse >$null
	echo Removed Temporary Files
	exit /b 0