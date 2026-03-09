@echo off
setlocal
cd /d %~dp0

echo [schoolcounsel] Launching browser: http://127.0.0.1:8000
start "" http://127.0.0.1:8000
if exist py.exe (
  set PY=py
) else (
  set PY=python
)

%PY% run.py --host 127.0.0.1 --port 8000
endlocal
