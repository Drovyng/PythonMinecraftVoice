net.exe session 1>NUL 2>NUL || (
echo This script requires elevated rights. 
powershell -Command "Start-Process ./generate_exe.bat -ArgumentList %CD% -Verb RunAs"
exit
)
cd %1
rmdir /s /q build
del /q "./dist/PythonMinecraftVoiceControl.exe"
pyinstaller --collect-all vosk --onefile --clean main.py -n PythonMinecraftVoiceControl
pause