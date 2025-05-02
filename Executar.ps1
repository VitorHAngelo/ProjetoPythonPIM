# Política para autorizar a execução de scripts só pra essa run
Set-ExecutionPolicy Unrestricted -Scope Process -Force

# Criar ambiente
python -m venv env
Write-Output "Ambiente virtual criado."

# Ativar ambiente virtual
Write-Host "Ativando ambiente virtual..."
& .\env\Scripts\activate

# Atualizar PIP
python -m pip install --upgrade pip

# Criar pasta files
if (-Not (Test-Path -Path "./files")) {
    New-Item -ItemType Directory -Path "./files"
    Write-Output "Pasta 'files' criada."
}

# Criar requirements.txt
if (-Not (Test-Path -Path "./files/requirements.txt")) {
    "cryptography`npython-dotenv" | Out-File -Encoding UTF8 "./files/requirements.txt"
    Write-Output "Arquivo 'requirements.txt' criado."
}

# Instalar as libraries definidas pelo req.
Write-Host "Instalando pacotes do requirements.txt..."
pip install -r .\files\requirements.txt

# Cria o KeyGen pra pepper e fernet em Python
if (-Not (Test-Path -Path "./files/.env")) {
$keygen = @"
import secrets
from cryptography.fernet import Fernet

pepper = secrets.token_hex(8)
fernet_key = Fernet.generate_key().decode()

with open('./files/.env', 'w') as env_file:
    env_file.write(f'PEPPER={pepper}\nFERNET_KEY={fernet_key}')
"@

# Escreve o código no arquivo
$keygen | Out-File -FilePath "./keygen.py" -Encoding utf8

# Roda o script Python
python ./keygen.py

# Apaga o keygen.py depois de rodar
Remove-Item "./keygen.py"
Write-Output "Arquivo .env criado"
}

cls

# Executando arquivo .py
#Write-Host "Iniciando o programa Python..."
python main.py