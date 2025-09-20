@echo off
:: 课程提醒系统 - Windows 双击运行版
:: 作者：StellarKitty
:: 功能：自动安装依赖并运行 reminder.py

chcp 65001 >nul
title 课程提醒系统 - 运行中...

echo.
echo 🌟 欢迎使用「课程提醒系统」
echo.
echo 正在检查 Python 是否安装...
echo.

:: 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误：未检测到 Python！
    echo.
    echo 请先安装 Python 3.6+：
    echo 1. 访问 https://www.python.org/downloads/
    echo 2. 下载并安装
    echo 3. 安装时务必勾选 "Add Python to PATH"
    echo.
    echo 安装完成后，重新双击本文件运行。
    echo.
    pause
    exit /b 1
)

:: 检查是否在正确目录
if not exist "reminder.py" (
    echo ❌ 错误：未找到 reminder.py 文件！
    echo.
    echo 请确保以下文件在同一文件夹：
    echo   - 运行课程提醒.bat
    echo   - reminder.py
    echo   - config.py
    echo   - 课表.xlsx
    echo.
    pause
    exit /b 1
)

:: 安装依赖
echo ✅ Python 检测通过
echo.
echo 正在安装所需依赖（pandas, openpyxl, schedule）...
echo.

python -m pip install pandas openpyxl schedule --user

if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败！请检查网络或手动运行：
    echo      pip install pandas openpyxl schedule
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ 所有依赖已安装完成！
echo.
echo 正在运行课程提醒脚本...
echo.

:: 运行主程序
python "reminder.py"

echo.
echo 🎉 脚本执行完毕！
echo.
echo 请检查：
echo   - 老师是否收到邮件
echo   - logs/reminder.log 查看详细日志
echo.
echo 按任意键关闭窗口...
pause >nul