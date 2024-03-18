net.exe session 1>NUL 2>NUL || (
echo This script requires elevated rights. 
powershell -Command "Start-Process ./generate_exe.bat -Verb RunAs"
exit
)
pip install vosk pyaudio keyboard mouse fuzzywuzzy pyinstaller
