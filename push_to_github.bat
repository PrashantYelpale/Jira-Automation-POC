@echo off
echo ========================================
echo Pushing to GitHub
echo ========================================
echo.
echo Repository: https://github.com/PrashantYelpale/Jira-Automation-POC.git
echo.
echo When prompted:
echo Username: prashantyelpale63@gmail.com
echo Password: [Your GitHub password or Personal Access Token]
echo.
echo Note: GitHub requires Personal Access Token (not password)
echo Get token from: https://github.com/settings/tokens
echo.
pause
echo.
echo Pushing...
git push -u origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================
    echo SUCCESS! Code pushed to GitHub!
    echo ========================================
    echo.
    echo Next steps:
    echo 1. Go to: https://github.com/PrashantYelpale/Jira-Automation-POC
    echo 2. Add secrets (see COMPLETE_SETUP_GUIDE.txt)
    echo 3. Enable Actions
    echo 4. Run workflow
    echo.
) else (
    echo ========================================
    echo FAILED! Could not push to GitHub
    echo ========================================
    echo.
    echo Possible reasons:
    echo 1. Wrong username/password
    echo 2. Need Personal Access Token instead of password
    echo 3. Repository doesn't exist
    echo.
    echo Solutions:
    echo 1. Use GitHub Desktop (easier)
    echo 2. Generate Personal Access Token from: https://github.com/settings/tokens
    echo 3. Try again with token as password
    echo.
)
pause
