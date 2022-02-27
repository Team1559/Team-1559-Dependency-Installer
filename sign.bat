@echo off
title exe signer

set dir=%cd%
echo please enter the filename
set /p name=""
cd "C:\Program Files (x86)\Windows Kits\10\bin\10.0.22000.0\x64\"
powershell .\signtool.exe sign /fd SHA256 /a '%dir%\%name%'
cd %dir%
pause