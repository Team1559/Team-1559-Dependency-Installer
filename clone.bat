
@echo off
setlocal enabledelayedexpansion
title 1559 Dependencies Installer
powershell timeout 2 >Nul

mkdir tmp >Nul
cd tmp
set directory=%CD%
set mp=""
cd..
move ba.zip %directory% >Nul
cd %directory%
powershell Expand-Archive ba.zip -DestinationPath %directory%\ >Nul
echo Do You Want To Install All Dependencies?
echo "Y" To Install All Dependencies Automatically "N" To Pick Which Dependencies To Install
set /p ask=""
if "%ask%"=="" (call set ask=n)
if "%ask%"=="N" (call set ask=n)
if "%ask%"=="n" (echo Please Pick Which Components You Want To Install) else (call :autoselected)
if "%ask%"=="n" (call :manual) else (call :auto)
echo Finished Installing Dependencies
echo Do You Want To Remove Temporary Files?
set /p remove=""
if "%remove%"=="" (call set remove=n)
if "%remove%"=="N" (call set remove=n)
if "%remove%"=="n" (call echo Leaving Temporary Files) else (call :remove)
pause
move nul 2>&0
EXIT /B 0

:autoselected
    echo The Installer Will Now Install All The Dependencies Automatically
    pause
	exit /b 0

:manual
    echo Do You Want To Install The Wpilib Suite? (y/n)
	set /p doWpi=""
	if "%doWpi%"=="N" (call set doWpi=n)
	if "%doWpi%"=="n" (echo Skipping WpiLib) else (
		echo Ready To Install The Wpilib Suite
		pause
		powershell %directory%\bitsadmin.exe /transfer WPI /download /priority foreground https://www.rylanswebdav.cf/publicdocuments/files/frc/wpilib.iso %directory%\wpilib.iso
		powershell Mount-DiskImage -ImagePath "%directory%\wpilib.iso" >Nul
		for %%a in (D E F G H I J K L M N O P Q R S T U V W X Y Z) do if exist %%a:\WPILibInstaller.exe (call set mp=%%a)
		powershell Copy-Item -Path !mp!:\* -Destination %directory% -PassThru >Nul
		powershell Dismount-DiskImage -ImagePath "%directory%\wpilib.iso" >Nul
		powershell %directory%\WPILibInstaller.exe
		echo Finished Installing Wpilib Suite)

	echo Do You Want To Install The Navx SDK? (y/n)
	set /p doNavX=""
	if "%doNavX%"=="N" (call set doNavX=n)
	if "%doNavX%"=="n" (echo Skipping The Navx SDK) else (
		echo Ready To Install The Navx SDK
		pause
		powershell %directory%\bitsadmin.exe /transfer NAVX /download /priority foreground https://www.rylanswebdav.cf/publicdocuments/files/frc/navx.zip %directory%\navx.zip
		powershell Expand-Archive navx.zip -DestinationPath %directory%\navx
		powershell %directory%\navx\setup.exe
		echo Finished Installing navx)

	echo Do You Want To Install The CTRE Phoenix API (y/n)
	set /p doCtr=""
	if "%doCtr%"=="N" (call set doCtr=n)
	if "%doCtr%"=="n" (echo Skipping The CTRE Phoenix API) else ( 
		echo Ready To Install The CTRE Phoenix API
		pause
		powershell %directory%\bitsadmin.exe /transfer CTRE /download /priority foreground https://www.rylanswebdav.cf/publicdocuments/files/frc/cf.zip %directory%\cf.zip
		cd %directory%
		powershell Expand-Archive cf.zip -DestinationPath %directory%
		powershell %directory%\cf.exe
		echo Finished Installing CTRE)

	echo Do You Want To Install The SparkMax API? (y/n)
	set /p doSprkmx=""
	if "%doSprkmx%"=="N" (call set doSprkmx=n)
	if "%doSprkmx%"=="n" (echo Skipping The SparkMax API) else ( 
		echo Ready To Install The SparkMax API
		pause
		powershell %directory%\bitsadmin.exe /transfer SPARKMAX /download /priority foreground https://www.rylanswebdav.cf/publicdocuments/files/frc/rev.zip %directory%\rev.zip
		cd %directory%
		powershell Expand-Archive rev.zip -DestinationPath %directory%\rev >Nul
		if exist C:\Users\Public\wpilib\2022\maven\com\revrobotics (RMDIR / Q/S C:\Users\Public\wpilib\2022\maven\com\revrobotics\frc >Nul) else (mkdir C:\Users\Public\wpilib\2022\maven\com\revrobotics\frc >Nul)
		(powershell Xcopy /E /I %directory%\rev\maven\com\revrobotics\frc C:\Users\Public\wpilib\2022\maven\com\revrobotics\frc\) >Nul
		if exist C:\Users\Public\wpilib\2021\vendordeps\REVLib.json (DEL /F/Q C:\Users\Public\wpilib\2022\vendordeps\REVLib.json >Nul) else (mkdir C:\Users\Public\wpilib\2022\vendordeps >Nul)
		move %directory%\rev\vendordeps\REVLib.json C:\Users\Public\wpilib\2022\vendordeps >Nul
		echo Finished SparkMax)

	echo Do You Want To Install The Rev Hardware Client? (y/n)
	set /p doRev=""
	if "%doRev%"=="N" (call set doRev=n)
	if "%doRev%"=="n" (echo Skipping The Rev Hardware Client) else ( 
		echo Ready To Install The Rev Hardware Client
		pause
		powershell %directory%\bitsadmin.exe /transfer Rev_Hardware_Client /download /priority foreground https://www.rylanswebdav.cf/publicdocuments/files/frc/revhc.zip %directory%\revhc.zip
		cd %directory%
		powershell Expand-Archive revhc.zip -DestinationPath %directory% >Nul
		powershell start %directory%\rev.exe >Nul)

	echo Do You Want To Install The Driver Station? (y/n)
	set /p doDs=""
	if "%doDs%"=="N" (call set doDs=n)
	if "%doDs%"=="n" (echo Skipping The Driver Station) else ( 
		echo Ready To Install The Driver Station
		pause
		powershell %directory%\bitsadmin.exe /transfer 'Driver Station' /download /priority foreground https://www.rylanswebdav.cf/publicdocuments/files/frc/ds.zip %directory%\ds.zip
		cd %directory%
		powershell Expand-Archive ds.zip -DestinationPath %directory%
		powershell %directory%\driverstation.exe)
	exit /b 0

:auto
	powershell %directory%\bitsadmin.exe /transfer WPI /download /priority foreground https://www.rylanswebdav.cf/publicdocuments/files/frc/wpilib.iso %directory%\wpilib.iso
	powershell Mount-DiskImage -ImagePath "%directory%\wpilib.iso" >Nul
	for %%a in (D E F G H I J K L M N O P Q R S T U V W X Y Z) do if exist %%a:\WPILibInstaller.exe (call set mp=%%a)
	powershell Copy-Item -Path !mp!:\* -Destination %directory% -PassThru >Nul
	powershell Dismount-DiskImage -ImagePath "%directory%\wpilib.iso" >Nul
	powershell %directory%\WPILibInstaller.exe

	powershell %directory%\bitsadmin.exe /transfer NAVX /download /priority foreground https://www.rylanswebdav.cf/publicdocuments/files/frc/navx.zip %directory%\navx.zip
	powershell Expand-Archive navx.zip -DestinationPath %directory%\navx
	powershell %directory%\navx\setup.exe


	powershell %directory%\bitsadmin.exe /transfer CTRE /download /priority foreground https://www.rylanswebdav.cf/publicdocuments/files/frc/cf.zip %directory%\cf.zip
	cd %directory%
	powershell Expand-Archive cf.zip -DestinationPath %directory%
	powershell %directory%\cf.exe

	powershell %directory%\bitsadmin.exe /transfer SPARKMAX /download /priority foreground https://www.rylanswebdav.cf/publicdocuments/files/frc/rev.zip %directory%\rev.zip
	cd %directory%
	powershell Expand-Archive rev.zip -DestinationPath %directory%\rev >Nul
	if exist C:\Users\Public\wpilib\2022\maven\com\revrobotics (RMDIR / Q/S C:\Users\Public\wpilib\2022\maven\com\revrobotics\frc >Nul) else (mkdir C:\Users\Public\wpilib\2022\maven\com\revrobotics\frc >Nul)
	(powershell Xcopy /E /I %directory%\rev\maven\com\revrobotics\frc C:\Users\Public\wpilib\2022\maven\com\revrobotics\frc\) >Nul
	if exist C:\Users\Public\wpilib\2021\vendordeps\REVLib.json (DEL /F/Q C:\Users\Public\wpilib\2022\vendordeps\REVLib.json >Nul) else (mkdir C:\Users\Public\wpilib\2022\vendordeps >Nul)
	move %directory%\rev\vendordeps\REVLib.json C:\Users\Public\wpilib\2022\vendordeps >Nul

	powershell %directory%\bitsadmin.exe /transfer Rev_Hardware_Client /download /priority foreground https://www.rylanswebdav.cf/publicdocuments/files/frc/revhc.zip %directory%\revhc.zip
	cd %directory%
	powershell Expand-Archive revhc.zip -DestinationPath %directory% >Nul
	powershell start %directory%\rev.exe >Nul

	powershell %directory%\bitsadmin.exe /transfer 'Driver Station' /download /priority foreground https://www.rylanswebdav.cf/publicdocuments/files/frc/ds.zip %directory%\ds.zip
	cd %directory%
	powershell Expand-Archive ds.zip -DestinationPath %directory%
	powershell %directory%\driverstation.exe
	exit /b 0

:remove
	echo Removing Temporary Directory 
	set target=C:\tmp\1559-Dependency-Installer\tmp
	powershell Remove-Item -Path %target% -Force -Recurse >$null
	exit /b 0

