@echo off
echo ========================================
echo Nalisa Event Management System Setup
echo ========================================
echo.

echo [1/5] Installing dependencies...
pip install -r requirement.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo [2/5] Running database migrations...
python manage.py migrate
if %errorlevel% neq 0 (
    echo ERROR: Failed to run migrations
    pause
    exit /b 1
)
echo.

echo [3/5] Populating sample data...
python manage.py populate_data
if %errorlevel% neq 0 (
    echo WARNING: Failed to populate sample data
)
echo.

echo [4/5] Creating superuser...
echo Please enter admin credentials:
python manage.py createsuperuser
echo.

echo [5/5] Setup complete!
echo.
echo ========================================
echo You can now run the server with:
echo     python manage.py runserver
echo.
echo Then visit: http://127.0.0.1:8000/
echo Admin panel: http://127.0.0.1:8000/admin/
echo ========================================
pause
