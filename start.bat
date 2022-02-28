
@echo off
title 1559 Dependencies Installer

set target=C:\tmp\1559-Dependency-Installer
set directory=%CD%
powershell mkdir %target% >$null
powershell Remove-Item -Path %target% -Force -Recurse >$null
powershell mkdir %target% >$null
powershell mv clone.bat %target% >Nul
powershell mv ba.zip %target% >Nul
powershell Xcopy /E /I c.exe %target% >Nul
cd %target%
c.exe /c powershell .\clone.bat
cd %directory%
c.exe /c powershell .\rem.bat
exit /b 0
