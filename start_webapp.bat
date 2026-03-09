@echo off
setlocal
cd /d %~dp0

echo [schoolcounsel] Starting web app...
if exist py.exe (
  set PY=py
) else (
  set PY=python
)

%PY% run.py --host 127.0.0.1 --port 8000
endlocal
