---
title: An Obsidian IDE for Python
date: 2025-02-25
draft: false
tags:
  - python
  - obsidian
  - how
  - to
categories:
  - tutorials
series:
  - python
---

## You did what?!
Let me explain: You write your notes in your Vault. Then, you run a command, and the code inside becomes a script and executes! And it does so with the environment of your choice already activated.

## Oh, I see now. This is a notebook!
No, it’s not. It transforms every code block—including comments—into an independent `script.py` inside your `.obsidian\scripts\python` folder. From there, you can grab it and start deploying or packaging it.

![Image Description](/images/obsidianicon.png)
## But the Python Plugin doesn’t work for me here...
No problem! You can also run it directly from your CLI/Cmd/PowerShell/Terminal—whatever you’re used to. When you do so, it will:
- Find the most recently updated note in your vault.
- Open it and extract every code block marked as Python. For example:
```
# path_venv = D:\some_path\venv  look_a_python some_code = "over here
```
- Use the first comment in the first Python block to determine the virtual environment. If none is specified, it will use your default environment.
- Save all extracted code blocks, in order, inside a `.py` file in `.obsidian\scripts\python`, named after the first snake_case word found in the first comment.
- Create a batch file that activates the environment, runs the script, and waits for user input before closing.

## Show this the code
To make this work, save the following script inside `.obsidian\scripts\python`:
```python
# IDE_py_Obsidian.py

import os
import re
from datetime import datetime
import subprocess
import glob
import sys

def normalizar_caminho(caminho):
    """Normaliza o caminho para usar uma única barra, independente de como foi escrito"""
    # Primeiro substitui barras duplas por barras simples
    caminho = caminho.replace('\\\\', '\\')
    # Substitui barras normais por barras invertidas
    caminho = caminho.replace('/', '\\')
    # Remove barras duplas que possam ter sido criadas
    while '\\\\' in caminho:
        caminho = caminho.replace('\\\\', '\\')
    return caminho

def encontrar_arquivo_mais_recente(vault_path):
    """Encontra o arquivo markdown mais recentemente modificado no vault"""
    arquivos = glob.glob(os.path.join(vault_path, '**/*.md'), recursive=True)
    return max(arquivos, key=os.path.getmtime)
  
def extrair_blocos_python(arquivo_md):
    """Extrai blocos de código Python e informações do ambiente virtual"""
    with open(arquivo_md, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    # Encontra blocos de código Python
    padrao = r'```python\s*(.*?)\s*```'
    blocos = re.findall(padrao, conteudo, re.DOTALL)
    print(f"Blocos encontrados: {len(blocos)}")
    # Procura pelo path_venv nos comentários
    path_venv = None
    nome_script = None
    codigo_completo = []
    for bloco in blocos:
        print(f"Analisando bloco:\n{bloco}")
        match = re.search(r'#\s*path_venv\s*=\s*(.*)\s+(\w+)\s*$', bloco, re.MULTILINE)
        if match:
            path_venv = normalizar_caminho(match.group(1).strip())
            nome_script = match.group(2).strip()
            print(f"Path encontrado: {path_venv}")
            print(f"Nome do script encontrado: {nome_script}")
        codigo_completo.append(bloco)
    return '\n'.join(codigo_completo), path_venv, nome_script

def salvar_script_python(codigo, nome_script, pasta_scripts):
    """Salva o código Python extraído em um arquivo .py"""
    if not os.path.exists(pasta_scripts):
        os.makedirs(pasta_scripts)
    caminho_script = os.path.join(pasta_scripts, f"{nome_script}.py")
    with open(caminho_script, 'w', encoding='utf-8') as f:
        f.write(codigo)
    return caminho_script

def criar_batch_script(path_venv, caminho_script):
    """Cria um arquivo batch temporário para ativar o ambiente e executar o script"""
    # Garantir que os caminhos estejam corretos
    path_venv = normalizar_caminho(path_venv)
    caminho_script = normalizar_caminho(caminho_script)
    conteudo_batch = f"""@echo off
chcp 65001 > nul
echo Ativando ambiente virtual em {path_venv}...
call "{path_venv}\\Scripts\\activate.bat"
echo.
echo Executando script {caminho_script}...
echo.
python "{caminho_script}"
echo.
echo Execucao finalizada!
echo.
:PROMPT
set /p CONFIRM="Digite OK para fechar: "
if /i "%CONFIRM%" neq "OK" goto PROMPT
exit
"""
    batch_path = caminho_script.replace('.py', '.bat')
    print(f"Criando batch em: {batch_path}")
    print(f"Conteúdo do batch:\n{conteudo_batch}")
    with open(batch_path, 'w', encoding='utf-8') as f:
        f.write(conteudo_batch)
    return batch_path

def main(vault_path):
    # Configurações
    pasta_scripts = os.path.join(vault_path, '.obsidian', 'scripts', 'python')
    # Encontra o arquivo mais recente
    arquivo_recente = encontrar_arquivo_mais_recente(vault_path)
    print(f"Arquivo mais recente encontrado: {arquivo_recente}")
    # Extrai o código Python
    codigo, path_venv, nome_script = extrair_blocos_python(arquivo_recente)
    if not codigo or not path_venv or not nome_script:
        print("Não foi possível encontrar código Python válido ou informações do ambiente virtual")
        print(f"Código: {bool(codigo)}")
        print(f"Path_venv: {path_venv}")
        print(f"Nome_script: {nome_script}")
        return
    # Salva o script Python
    caminho_script = salvar_script_python(codigo, nome_script, pasta_scripts)
    print(f"Script salvo em: {caminho_script}")
    # Cria e executa o batch script
    batch_path = criar_batch_script(path_venv, caminho_script)
    print(f"Executando batch: {batch_path}")
    try:
        subprocess.run(batch_path, shell=True)
        # Apaga o arquivo batch após a execução
        if os.path.exists(batch_path):
            os.remove(batch_path)
    except Exception as e:
        print(f"Erro ao executar batch: {e}")

if __name__ == "__main__":
    try:
        vault_path = sys.argv[1]
    except IndexError:
        vault_path = "D:\\Trabalho\\obsidian_vaults\\Vault"
    main(vault_path)
```

## Let's code some more!
This was a very satisfying exercise that has now become part of my daily workflow. I hope this helps you as well in the projects you have in mind!

