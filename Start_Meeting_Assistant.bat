@echo off
title AI Meeting Assistant Server
echo ===================================================
echo Starting AI Meeting Assistant...
echo The dashboard will open automatically in your browser.
echo.
echo IMPORTANT: Keep this black window open while using the app!
echo To shut down the app, just close this window.
echo ===================================================
echo.

.\.venv\Scripts\streamlit.exe run app.py

pause
