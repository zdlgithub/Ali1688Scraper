@echo off
cls
title �ռ��๦���޸�
:menu
cls
color 7
echo.
echo ==============================
echo ��ѡ��Ҫ���еĲ�����Ȼ�󰴻س�
echo ==============================
echo.
echo 1.ִ�н���1688��ƷFor Shopee
echo.
echo Q.�˳�
echo.
echo.
:cho
set choice=
set /p choice= ��ѡ�����:
IF NOT "%choice%"=="" SET choice=%choice:~0,1%
if /i "%choice%"=="1" goto ali
if /i "%choice%"=="Q" goto endd
echo ѡ����Ч������������
echo.

:endd
echo "�˳�."

:ali
echo "Begin execute....."
"%CD%\venv\scripts\python.exe" "%CD%\ali1688scrapermain.py" 
echo "end execute."
goto cho