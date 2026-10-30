@echo off
title My Savings Bank - Web Server
echo Starting My Savings Bank on http://localhost:8080 ...
start http://localhost:8080/savings-app-1/index.html
python -m http.server 8080
