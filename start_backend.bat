@echo off
echo ========================================
echo Starting Backend Server...
echo ========================================
cd /d %~dp0

echo Checking virtual environment...
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run: py -m venv venv
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Checking Python...
py --version
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

echo Checking database connection...
py -c "from database import engine; engine.connect(); print('Database connection OK!')" 2>nul
if errorlevel 1 (
    echo WARNING: Database connection failed, but continuing...
)

echo.
echo Starting FastAPI server on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
py -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause
