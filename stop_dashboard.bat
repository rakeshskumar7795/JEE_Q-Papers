@echo off
rem Stops whatever is listening on port 8501 (the dashboard).
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 8501 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }"
echo Dashboard stopped.
pause
