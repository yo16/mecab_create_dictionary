@echo off

rem inputフォルダにある入力ファイルを読み込んで
rem MeCabの辞書ファイルを作成し、登録する
rem 2017 (c) y.ikeda

rem Program Filesへアクセスするために、
rem 管理者として実行する必要がある



%~d0
cd %~dp0

:checkMandatoryLevel
for /f "tokens=1 delims=," %%i in ('whoami /groups /FO CSV /NH') do (
	if "%%~i"=="BUILTIN\Administrators" set ADMIN=yes
	if "%%~i"=="Mandatory Label\High Mandatory Level" set ELEVATED=yes
)

if "%ADMIN%" neq "yes" (
	echo このファイルは管理者権限での実行が必要です{Administratorsグループでない}
	if "%1" neq "/R" goto runas
	goto exit1
)
if "%ELEVATED%" neq "yes" (
	if "%1" neq "/R" goto runas
	goto exit1
)





:admins
	rem プログラム本体

	python MakeMecabUserDictionary.py .\input
	rem echo,-- result --
	rem echo %ERRORLEVEL%

	pause

	goto exit1

:runas
    rem 管理者として再実行
    powershell -Command Start-Process -Verb runas "%0" -ArgumentList "/R" 

:exit1
