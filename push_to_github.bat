@echo off
echo ========================================
echo Push Momenta to GitHub
echo ========================================
echo.
echo Please enter your GitHub repository URL
echo Example: https://github.com/yourusername/momenta.git
echo.
set /p REPO_URL="Enter GitHub repository URL: "

echo.
echo Adding remote repository...
git remote add origin %REPO_URL%

echo.
echo Pushing to GitHub...
git branch -M main
git push -u origin main

echo.
echo ========================================
echo Done! Your code is now on GitHub
echo ========================================
pause
