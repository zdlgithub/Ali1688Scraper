@echo off
cls
title 终极多功能修复
:menu
cls
color 7
echo.
echo ==============================
echo 请选择要进行的操作，然后按回车
echo ==============================
echo.
echo 1.执行解析1688产品For Shopee
echo.
echo Q.退出
echo.
echo.
:cho
set choice=
set /p choice= 请选择操作:
IF NOT "%choice%"=="" SET choice=%choice:~0,1%
if /i "%choice%"=="1" goto ali
if /i "%choice%"=="Q" goto endd
echo 选择无效，请重新输入
echo.

:endd
echo "退出."

:ali
echo "Begin execute....."
"%CD%\venv\scripts\python.exe" "%CD%\ali1688scrapermain.py" 
echo "end execute."
goto cho