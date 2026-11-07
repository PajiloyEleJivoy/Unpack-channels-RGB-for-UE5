@echo off
rem Installs the dependencies and adds "Unpack channels" to Explorer's Send To menu.
cd /d "%~dp0"

rem The py launcher works even when python.exe is not on PATH; it sits in Windows or in the user's Programs.
set PY=python
if exist "%LOCALAPPDATA%\Programs\Python\Launcher\py.exe" set PY="%LOCALAPPDATA%\Programs\Python\Launcher\py.exe" -3
if exist "%SystemRoot%\py.exe" set PY="%SystemRoot%\py.exe" -3

for /f "delims=" %%i in ('call %PY% -c "import sys; print(sys.executable)"') do set PYEXE=%%i
if not defined PYEXE goto :fail

"%PYEXE%" -m pip install --user -r requirements.txt || goto :fail

"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -Command "$s = (New-Object -ComObject WScript.Shell).CreateShortcut([Environment]::GetFolderPath('SendTo') + '\Unpack channels.lnk'); $s.TargetPath = '%PYEXE%'; $s.Arguments = '\"%~dp0unpack_channels.py\"'; $s.Save()" || goto :fail

"%PYEXE%" unpack_channels.py --selftest || goto :fail

echo.
echo Done: right-click a texture -^> Send to -^> Unpack channels
pause
exit /b 0

:fail
echo.
echo Install failed, see the error above. Is Python installed?
pause
exit /b 1
