@echo off

rem input�t�H���_�ɂ�����̓t�@�C����ǂݍ����
rem MeCab�̎����t�@�C�����쐬���A�o�^����
rem 2017 (c) y.ikeda

rem Program Files�փA�N�Z�X���邽�߂ɁA
rem �Ǘ��҂Ƃ��Ď��s����K�v������



%~d0
cd %~dp0

:checkMandatoryLevel
for /f "tokens=1 delims=," %%i in ('whoami /groups /FO CSV /NH') do (
	if "%%~i"=="BUILTIN\Administrators" set ADMIN=yes
	if "%%~i"=="Mandatory Label\High Mandatory Level" set ELEVATED=yes
)

if "%ADMIN%" neq "yes" (
	echo ���̃t�@�C���͊Ǘ��Ҍ����ł̎��s���K�v�ł�{Administrators�O���[�v�łȂ�}
	if "%1" neq "/R" goto runas
	goto exit1
)
if "%ELEVATED%" neq "yes" (
	if "%1" neq "/R" goto runas
	goto exit1
)





:admins
	rem �v���O�����{��

	python MakeMecabUserDictionary.py .\input
	rem echo,-- result --
	rem echo %ERRORLEVEL%

	pause

	goto exit1

:runas
    rem �Ǘ��҂Ƃ��čĎ��s
    powershell -Command Start-Process -Verb runas "%0" -ArgumentList "/R" 

:exit1
