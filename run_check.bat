@echo off
cd /d "%~dp0"
echo 正在验证 labels.csv 格式...
python check_labels.py
echo.
echo 验证完成，按任意键退出...
pause >nul