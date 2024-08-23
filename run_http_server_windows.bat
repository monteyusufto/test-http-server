@echo off
REM Get the current directory where the batch file is located
set SCRIPT_DIR=%~dp0

echo Building Docker image...
docker build -t test-http-server %SCRIPT_DIR%
if %ERRORLEVEL% NEQ 0 (
    echo Docker image build failed. Exiting.
    exit /b %ERRORLEVEL%
)

echo Running Docker container...
docker run -d --name test-http-server -p 80:5000 -v %SCRIPT_DIR%:/app/uploads test-http-server
if %ERRORLEVEL% NEQ 0 (
    echo Docker container run failed. Exiting.
    exit /b %ERRORLEVEL%
)

echo Docker container is running. You can access it at http://127.0.0.1.