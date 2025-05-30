@echo off

color f0
cd /d %~dp0
chcp 65001 > nul

if not exist "env" (
    echo Ambiente virtual nao encontrado, criando ambiente...
    python -m venv env
)

echo Atualizando pip...
.\env\Scripts\python.exe -m pip install --upgrade pip

if not exist "files" (
    echo Criando pasta 'files'...
    mkdir files
)

if not exist "files\requirements.txt" (
    echo Criando arquivo 'requirements.txt'...
    echo cryptography > files\requirements.txt
    echo python-dotenv >> files\requirements.txt
    echo matplotlib >> files\requirements.txt
)

echo Instalando pacotes do 'requirements.txt'...
.\env\Scripts\python.exe -m pip install -r .\files\requirements.txt

cls

echo Executando o main.py...
where wt > nul 2>&1
if %errorlevel%==0 (
    wt -d . -p "Command Prompt" cmd /c .\env\Scripts\python.exe main.py
) else (
    echo Terminal nao instalado, instalacao recomendada.
    echo Aperte ENTER para abrir no CMD...
    pause > nul
    .\env\Scripts\python.exe main.py
    pause
)
