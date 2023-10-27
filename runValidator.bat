@echo off

REM Check if Python is in the system's PATH
where python > nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo "Python is not in the system's PATH"
    exit /b 1
)

REM Check if the "validator" directory exists
IF NOT EXIST "%cd%\validator" (
    echo "The 'validator' directory does not exist."
    exit /b 1
)

SET "requirements=%cd%\validator\requirements.txt"
python -m pip install -r "%requirements%"

SET "validator=%cd%\validator\validatexml-xsd.py"

python "%validator%" %*
