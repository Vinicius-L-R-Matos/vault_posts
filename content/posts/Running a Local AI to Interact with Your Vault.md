---
title: Running a Local AI to Interact with Your Vault
date: 2023-12-20
draft: false
tags:
  - how_to
  - obsidian
  - AI
categories:
  - tutorials
series:
  - Local
---

## From: Ollama Installation. To: AI Integration
Inspired once more by [NetworkChuck](https://www.youtube.com/watch?v=Wjrdr0NU4Sk), this guide walks you through setting up Ollama on your system, integrating various AI models, and enhancing your workflow with ==Stable Diffusion== and ==BMO== or ==Smart Connections== on obsidian. Whether you're a developer or an AI enthusiast, this step-by-step tutorial will help you harness the power of local AI models effectively.

If you also enjoy configuring your AI environment and exploring different models, this approach will provide you with the control and flexibility you need!

What’s happening here is that you’re setting up a local AI server using Ollama, complemented by a web UI for easier interaction and additional tools like Stable Diffusion for image generation. Once everything is configured, maintaining and expanding your AI capabilities requires minimal effort.

Below, I’ll show you how to set up Ollama, integrate various AI models, and enhance your setup with additional tools. You can follow these steps to create your personalized AI environment.

## Did you ever run an Ollama?
![logo Description](/images/ollama.png)
[Ollama](https://github.com/ollama/ollama/tree/main/docs) is a lightweight, extensible framework for building and running language models on the local machine. It provides a simple API for creating, running, and managing models, as well as a library of pre-built models that can be easily used in a variety of applications.

To get started right away, do the following:

1. **Visit Ollama's Website**
    - Go to [ollama.com](https://ollama.com/).

2. **Install WSL on Windows**
    
    - Open the Windows Command Prompt (CMD) and execute:
        ```
        wsl --install
        ```
    - If is the first time, create some auth there.

3. **Upgrade and Update Packages**
    - In your WSL terminal, run:
        ```
        sudo apt update
        sudo apt upgrade -y
        ```
        
4. **Download the Linux Version**
    - Copy and run the following command from ollama in your terminal:
        ```bash
        curl -fsSL https://ollama.com/install.sh | sh
        ```
        
5. **Verify Ollama is Running**
    - Open your web browser and navigate to:
        ```
        localhost:11434
        ```
    - You should see a message indicating that Ollama is running!
	- *Note: I think "11434" can be transleted as "llama" if you to bend 90º you neek. Once you to figure it out, maybe it won't come back...*

6. **Take care of you llamas**
	- To view all the AI models currently installed in your Ollama setup, use the following command:
        ```
		ollama list
        ```
	- If you don't what one of those anymore, you can always eliminate whit:
        ```
		ollama rm model_name
        ```

9. **Add an AI Model to Ollama**
    - Pull the Llama2 model:
        ```bash
        ollama pull model_name
        ```
        
7. **Run and Test the Model**
    - Execute the following command to test:
        ```bash
        ollama run model_name
        ```
        
    - You can interact with the model here. Press `Ctrl+C` to stop the response and type `/bye` to close the session.

## Local ollama
This is the easy way. Only by installing ollama,it have already star a server, that wait for run ou API calls!
The standard port is 11434, so you can just test some requests. Like:
```python
import requests
import re
import json

# Função para extrair apenas o JSON da resposta
def extrair_json(response_text):
    match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
    if match:
        json_str = match.group(1)
        return json.loads(json_str)
    return None

url = "http://localhost:11434/api/generate"
headers = {"Content-Type": "application/json"}
data = {
    "model": "tinyllama",
    "system": """Como o bot agira e exemplos""",
    "prompt": "A pergunta que deseja saber",
    "stream": False,
    "options": {
        "temperature": 0.05,
        "num_predict": 160,     # Quantidade máxima de resposta
        "top_p": 0.1,           # Reduzir variabilidade
        "top_k": 1,              # Forçar escolhas mais determinísticas
        "repeat_penalty": 1.0,   # Evita penalidades
        "seed": 42              # Mantém consistência nas respostas
    }
}

response = requests.post(url, headers=headers, json=data)

response_data = response.json()
texto_resposta = response_data['response']
resposta_dict = extrair_json(texto_resposta)

print( 'created_at: ', response_data[ 'created_at'])
print( 'model: ', response_data[ 'model'])
print( 'response: ', resposta_dict)
```

## Web UI

The [Web UI](https://github.com/open-webui/open-webui) provides an entire interface to interact with your AI models more conveniently. There are several options available, and for this guide, we'll set up **Open Web UI** using Docker.

### Installing Docker

1. **Add Docker's Official GPG Key and Repository**
    ```bash
    sudo apt-get update
    sudo apt-get install ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    ```

2. **Install Docker**
    ```bash
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    ```

### Running the Web UI Container

1. **Start the Container**
    ```bash
    sudo docker run -d --network=host -v open-webui:/app/backend/data -e OLLAMA_BASE_URL=http://127.0.0.1:11434 --name open-webui --restart always ghcr.io/open-webui/open-webui:main
    ```
	- If you need to stop it:
	```
	sudo docker stop open-webui
	sudo docker rm open-webui
	sudo docker stop $(sudo docker ps -q)
	
	```
1. **Verify the Container is Running**
    ```bash
    sudo docker ps
    ```
    - You should see a list of running containers, indicating that the Web UI is available at:
        ```
        http://localhost:8080/auth
        ```
    - Create a local access credential. The first login uses the `admin` account.
    - Connection settings can be found under `Settings` -> `Connections`.
    
## Adding More Models

1. **Pull Additional Models via Ollama**
    ```bash
    ollama pull codegen
    ```
    - After installation, the model will be available in the Web UI's selection box.

## Managing Access

You can manage user access through the admin panel:
1. **Access the Admin Panel**
    - Click on the bottom-left logo and navigate to the admin section.
2. **Manage Users and Groups**
    - In the `Users` section, create and assign users to specific groups to control access permissions.

## Creating Custom Models
To create your own models:
1. **Access the Workspace**
    - Navigate to the workspace and click the `+` button on the top-right corner to add a new model.

## Using AI into the Vault
### Adding AI to Smart Connections
1. **Configure Local AI in Chat Settings**
    - Select the `Local` option and choose the desired model name from the chat configuration settings.

### BMO option
Installing the BMO plugin will enable the default chosen model. The available commands are:
#### General Commands

- `/clear` or `/c` - Clear chat history.
- `/ref on` - Turn on "reference current note".
- `/ref off` - Turn off "reference current note".
- `/maxtokens [VALUE]` - Set max tokens.
- `/temp [VALUE]` - Change temperature range from 0 to 2.

#### Profile Commands

- `/profile` - List profiles.
- `/profile [PROFILE-NAME] or [VALUE]` - Change profile.

#### Model Commands
- `/model` - List models.
- `/model [MODEL-NAME] or [VALUE]` - Change model.

#### Prompt Commands
- `/prompt` - List prompts.
- `/prompt [PROMPT-NAME] or [VALUE]` - Change prompts.
- `/prompt clear` - Clear prompt.

#### Editor Commands
- `/append` - Append current chat history to the current active note.
- `/save` - Save current chat history to a note.
- `/load` - List or load a chat history into view.

#### Response Commands
- `/stop` or `/s` - Stop fetching response. **Warning:** Anthropic models cannot be aborted. Use with caution.

### Call queries from Python Scripter
If you like to play some hard code, you can to try to run the script direct from the control painel, or even from the cmd. Since none of those solutions worked for me, this is what i build:

```python
"""
##ObsidianAssistant
Solução para chamar a API ollama usando apenas dados sobre as notas do Obsidian em prompt tunning. Lê a nota mais recente no diretório self_questions, devove em estrutura de pastas por date time em self_talk ou em self_graphs.
- Aguarda uma estrutura de diretórios a serem lidos: base_path = self.vault_path / "Notas" / "Tratados".
- Aguarda possuir o Tinyllama instalado como modelo padrão. Pode alterar isso no YAML da própria nota.
- Escreva resuma|explique|desenhe|encontre|relacione e cite o contexto como faria normalmente na nota usando [[]]. 
- Chame o script pelo scripter ou cmd usando o seguinte pip: pip install requests datetime pathlib pyyaml fuzzywuzzy networkx matplotlib numpy pyvis pandas python-Levenshtein community.
- Abra o grafico no navegador e os dados salvos em seu visualizador de .xlsx.

### Armazenamento
- Grafos: self_graphs/YYYY/MM/DD/
- Conversas: self_talks/YYYY/MM/DD/
- Cache: Pickle para armazenamento temporário

### Configuração
Via arquivo YAML em self_questions/:

### Desempenho:
5 a 6 seg em 16GB RAM, sem GPU para modelo tinyllama.
2 a 3 minutos em 16GB RAM, sem GPU para modelo llama2

### Recursos:
1. /resuma [elemento]
- Gera resumos de notas ou diretórios
- Exemplo: /resuma nota.md

2. /explique [elemento]
- Fornece explicações detalhadas
- Exemplo: /explique #conceito

3. /desenhe [elemento]
- Cria visualizações em grafo usando pyvis
- Exemplo: /desenhe diretório Notas

4. /encontre [termo]
- Realiza buscas no vault
- Exemplo: /encontre python

5. /relacione [elemento1], [elemento2]
- Analisa relações entre elementos
- Exemplo: /relacione #tag1, #tag2
"""

import requests
from datetime import datetime
import os
import json
import re
from pathlib import Path
from typing import List, Tuple, Dict, Optional, Set, Tuple
import yaml
from yaml import SafeLoader
from fuzzywuzzy import fuzz
import pickle
from datetime import datetime, timedelta, date
import community
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from pyvis.network import Network
import pandas as pd
import traceback

class ObsidianAssistant:
    def __init__(self, vault_path: str):
        print("\nInicializando ObsidianAssistant...")
        self.vault_path = Path(vault_path)
        print(f"Vault path: {self.vault_path}")
        
        # Registrar handlers
        self.command_handlers = {
            "/desenhe": self.handle_visualization,
            "/explique": self.handle_explain,
            "/resuma": self.handle_summary,
            "/encontre": self.handle_find,
            "/relacione": self.handle_relationships
        }
        
        print(f"Comandos registrados: {list(self.command_handlers.keys())}")
    
    def identify_command(self, prompt: str) -> tuple[str, str]:
        """Identifica comandos com / e sem /"""
        print(f"\nIdentificando comando em: {prompt}")
        
        words = prompt.lower().split()
        if not words:
            print("Prompt vazio")
            return None, prompt
            
        first_word = words[0]
        remaining = ' '.join(words[1:])
        
        # Verificar comando desenhe especificamente
        if first_word in ['desenhe', '/desenhe']:
            print("Comando desenhe identificado")
            return "/desenhe", remaining
            
        # Outros comandos
        if first_word in self.command_handlers:
            print(f"Comando {first_word} identificado")
            return first_word, remaining
            
        print("Nenhum comando identificado")
        return None, prompt    

    def process_command(self, config: dict) -> str:
        try:
            prompt = config['prompt'].strip()  # Adicionar strip()
            
            # Verificar explicitamente se é o comando desenhe
            if prompt.startswith("desenhe") or prompt.startswith("/desenhe"):
                print("\nIniciando geração do grafo...")
                # Remover o comando do prompt
                remaining = prompt.replace("desenhe", "").replace("/desenhe", "").strip()
                # Chamar diretamente o handler de visualização
                return self.handle_visualization(remaining, config)
            
            # Identificação normal de outros comandos
            command, remaining = self.identify_command(prompt)
            if command in self.command_handlers and command != "/desenhe":
                response = self.command_handlers[command](remaining, config)
                self.save_to_md(prompt, response)
                return response
                
            # Fallback para consulta normal
            response = self.query_ollama(config['model'], prompt)
            self.save_to_md(prompt, response)
            return response
                
        except Exception as e:
            print(f"Erro ao processar comando: {str(e)}")
            traceback.print_exc()  # Adicionar para debug
            return f"Erro: {str(e)}"

    def handle_explain(self, content: str, config: dict) -> str:
        """Única função nova realmente necessária"""
        try:
            context = self.get_content_context(content)
            prompt = f"""Explique detalhadamente este conteúdo:
            {context}
            
            Forneça:
            1. Conceitos principais
            2. Exemplos práticos
            3. Relações importantes"""
            
            return self.query_ollama(config['model'], prompt)
        except Exception as e:
            return f"Erro ao explicar: {str(e)}"

    def handle_explain(self, content: str, config: dict) -> str:
        """Handler para /explique"""
        try:
            context = self.get_content_context(content)
            prompt = f"""Explique detalhadamente este conteúdo:
            {context}
            
            Forneça:
            1. Conceitos principais
            2. Exemplos práticos
            3. Relações importantes"""
            
            return self.query_ollama(config['model'], prompt)
        except Exception as e:
            return f"Erro ao explicar: {str(e)}"

    def handle_summary(self, prompt: str, config: dict) -> str:
        try:
            # Limpar o prompt
            clean_prompt = prompt.replace("/resuma", "").strip()
            
            # Remover [[ e ]] se existirem
            if clean_prompt.startswith("[[") and clean_prompt.endswith("]]"):
                clean_prompt = clean_prompt[2:-2]
            
            # Verificar se é diretório
            is_directory = "diretório" in clean_prompt.lower() or "diretorio" in clean_prompt.lower()
            
            if is_directory:
                target_path = (prompt.lower()
                            .replace("/resuma", "")
                            .replace("diretório", "")
                            .replace("diretorio", "")
                            .replace("o", "", 1)
                            .strip())
                
                try:
                    # Converter para Path e resolver caminho
                    dir_path = Path(target_path).resolve()
                    print(f"Caminho completo: {dir_path}")
                    
                    # Se é caminho absoluto, tentar tornar relativo ao vault
                    if dir_path.is_absolute():
                        try:
                            dir_path = dir_path.relative_to(self.vault_path)
                            print(f"Caminho relativo ao vault: {dir_path}")
                        except ValueError:
                            print("Usando caminho absoluto")
                    
                    # Caminho completo para busca
                    full_path = self.vault_path / dir_path
                    print(f"Buscando em: {full_path}")
                    
                    if not full_path.exists():
                        return f"Diretório não encontrado: {full_path}"
                    
                    # Coletar conteúdo de todos os arquivos .md
                    all_content = []
                    file_names = []
                    
                    for md_file in full_path.rglob("*.md"):
                        try:
                            with open(md_file, 'r', encoding='utf-8') as f:
                                content = f.read()
                                if content.startswith('---'):
                                    end_pos = content.find('---', 3)
                                    if end_pos != -1:
                                        content = content[end_pos + 3:].strip()
                                all_content.append(content)
                                file_names.append(md_file.name)
                                print(f"Arquivo processado: {md_file.name}")
                        except Exception as e:
                            print(f"Erro ao ler {md_file}: {e}")
                    
                    if not all_content:
                        return f"Nenhum arquivo markdown encontrado em: {full_path}"
                    
                    # Juntar conteúdo com referências
                    combined_content = ""
                    for i, (content, name) in enumerate(zip(all_content, file_names)):
                        combined_content += f"\n\n=== Arquivo: {name} ===\n{content}"
                    
                    # Criar prompt para resumo
                    summary_prompt = f"""Por favor, faça um resumo abrangente do seguinte conteúdo de um diretório com {len(all_content)} arquivos markdown:

    {combined_content}

    Por favor, forneça um resumo estruturado que inclua:
    1. Principais tópicos abordados
    2. Conceitos-chave
    3. Pontos importantes
    4. Relações entre os diferentes arquivos"""
                    
                    print("Gerando resumo...")
                    summary = self.query_ollama(config['model'], summary_prompt)
                    
                    return f"""Resumo do diretório: {dir_path}
                    
    Total de arquivos processados: {len(all_content)}
    Arquivos incluídos: {', '.join(file_names)}

    {summary}"""
                    
                except Exception as e:
                    print(f"Erro ao processar diretório: {e}")
                    traceback.print_exc()
                    return f"Erro ao processar diretório: {str(e)}"
            else:
                try:
                    # Se não tiver context_notes, usar o prompt limpo
                    file_path = config.get('context_notes', [clean_prompt])[0]
                    print(f"\nProcessando arquivo: {file_path}")
                    
                    content = self.get_content_context(file_path)
                    if not content:
                        return f"Nenhum conteúdo encontrado para: {file_path}"
                    
                    summary_prompt = f"""Por favor, faça um resumo estruturado do seguinte texto:

    {content}

    Por favor, inclua:
    1. Principais pontos
    2. Conceitos-chave
    3. Conclusões importantes"""

                    print("Gerando resumo...")
                    return self.query_ollama(config['model'], summary_prompt)
                    
                except Exception as e:
                    print(f"Erro ao processar arquivo: {e}")
                    traceback.print_exc()
                    return f"Erro ao resumir arquivo: {str(e)}"
                    
        except Exception as e:
            print(f"Erro no handle_summary: {e}")
            traceback.print_exc()
            return f"Erro ao gerar resumo: {str(e)}"

    def handle_find(self, content: str, config: dict) -> str:
        """Busca elementos relacionados ao tema"""
        try:
            results = []
            
            # Buscar em notas
            note_matches = self.fuzzy_find_note(content)
            for note, score in note_matches[:5]:
                results.append(f"📄 Nota: {note.relative_to(self.vault_path)} (relevância: {score}%)")
            
            # Buscar em tags
            if '#' in content:
                tags = re.findall(r'#(\w+)', content)
                tag_notes = self.find_notes_by_tags(tags)
                for path, _ in tag_notes:
                    results.append(f"🏷️ Tag: {path.relative_to(self.vault_path)}")
            
            # Buscar em diretórios
            for dir_path in self.vault_path.rglob("*"):
                if dir_path.is_dir() and content.lower() in dir_path.name.lower():
                    results.append(f"📁 Diretório: {dir_path.relative_to(self.vault_path)}")
            
            return self.format_search_results(results)
        except Exception as e:
            return f"Erro na busca: {str(e)}"

    def handle_relationships(self, prompt: str, config: dict) -> str:
        """Analisa relações entre elementos"""
        try:
            elements = [e.strip() for e in prompt.split(',')]
            if len(elements) < 2:
                return "Por favor, forneça dois ou mais elementos para relacionar."
            
            contents = []
            for element in elements:
                notes = self.get_notes_from_path(element)
                if notes:
                    contents.append("\n".join([content for _, content in notes]))
            
            context = f"""Analise as relações entre os seguintes elementos:
            
            Elementos: {', '.join(elements)}
            
            Conteúdos:
            {'-' * 40}
            {'\n' + '-' * 40 + '\n'.join(contents)}"""
            
            response = self.query_ollama(config['model'], context)
            
            # Manter funcionalidade de visualização da versão antiga
            if "visualize" in prompt.lower():
                G = self.build_knowledge_graph()
                self.visualize_knowledge_graph(G, "Grafo de Relações")
            
            return response
        except Exception as e:
            return f"Erro ao relacionar: {str(e)}"

    def format_search_results(self, results: List[str]) -> str:
        """Formata os resultados da busca"""
        if not results:
            return "Nenhum resultado encontrado."
            
        # Formatar resposta
        response = [
            "# Resultados da Busca\n",
            f"Termo pesquisado: {content}\n",
            "## Resultados encontrados:\n"
        ]
        response.extend(results)
        
        # Adicionar sugestões de próximos passos
        response.extend([
            "\n## Próximos passos sugeridos:",
            "- Use /explique para ver detalhes de uma nota específica",
            "- Use /relacione para ver conexões entre elementos",
            "- Use /desenhe para visualizar as relações em grafo"
        ])
        
        return "\n".join(response)

    def get_content_context(self, file_path: str) -> str:
        """Obtém o conteúdo de um arquivo markdown"""
        try:
            # Converter para Path se for string
            if isinstance(file_path, str):
                file_path = Path(file_path)
                
            # Adicionar extensão .md se não existir
            if not file_path.suffix:
                file_path = file_path.with_suffix('.md')
                
            # Se é caminho absoluto, tentar tornar relativo ao vault
            if file_path.is_absolute():
                try:
                    file_path = file_path.relative_to(self.vault_path)
                except ValueError:
                    pass
                    
            # Caminho completo para o arquivo
            full_path = self.vault_path / file_path
            print(f"Tentando ler arquivo: {full_path}")
            
            # Se não encontrar diretamente, tentar buscar por nome
            if not full_path.exists():
                print("Arquivo não encontrado diretamente, buscando por nome...")
                file_name = file_path.name
                # Buscar em todo o vault
                for found_file in self.vault_path.rglob("*.md"):
                    if found_file.name.lower() == file_name.lower():
                        full_path = found_file
                        print(f"Arquivo encontrado em: {full_path}")
                        break
            
            if not full_path.exists():
                print(f"Arquivo não encontrado: {full_path}")
                return ""
                
            print(f"Lendo arquivo: {full_path}")
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Remover YAML frontmatter se existir
            if content.startswith('---'):
                end_pos = content.find('---', 3)
                if end_pos != -1:
                    content = content[end_pos + 3:].strip()
                    
            return content
            
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}")
            traceback.print_exc()
            return ""
        
    def visualize_knowledge_graph(self, G: nx.Graph, title: str = "Grafo de Conhecimento"):
        """Visualiza o grafo de conhecimento em HTML interativo"""
        try:
            # Criar diretório self_graphs se não existir
            output_dir = self.vault_path / "self_graphs"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            html_path = output_dir / f"graph_{timestamp}.html"
            data_path = output_dir / f"graph_data_{timestamp}.json"
            
            # Criar visualização
            net = Network(
                height="750px", 
                width="100%", 
                bgcolor="#ffffff", 
                font_color="black",
                select_menu=True,
                filter_menu=True,
                cdn_resources='remote'  # Usar CDN remoto
            )

            # Configurar cabeçalho HTML personalizado
            net.html = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                
                <!-- Vis.js CDN -->
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/dist/vis-network.min.css" integrity="sha512-WgxfT5LWjfszlPHXRmBWHkV2eceiWTOBvrKCNbdgDYTHrT2AeLCGbF4sZlZw3UMN3WtL0tGUoIAKsu8mllg/XA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
                <script src="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/vis-network.min.js" integrity="sha512-LnvoEWDFrqGHlHmDD2101OrLcbsfkrzoSpvtSQtxK3RMnRV0eOkhhBN2dXHKRrUU8p2DGRTk35n4O8nWSVe1mQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
                
                <!-- Bootstrap CDN -->
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous" />
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js" integrity="sha384-JEW9xMcG8R+pH31jmWH6WWP0WintQrMb4s7ZOdauHnUtxwoG2vI5DkLtS3qm9Ekf" crossorigin="anonymous"></script>

                <!-- Tom Select CDN -->
                <link href="https://cdn.jsdelivr.net/npm/tom-select@2.2.2/dist/css/tom-select.css" rel="stylesheet">
                <script src="https://cdn.jsdelivr.net/npm/tom-select@2.2.2/dist/js/tom-select.complete.min.js"></script>

                <style type="text/css">
                    #mynetwork {
                        width: 100%;
                        height: 750px;
                        background-color: #ffffff;
                        border: 1px solid lightgray;
                        position: relative;
                        float: left;
                    }
                </style>
            </head>
            <body>
                <div class="container-fluid">
                    <div id="mynetwork"></div>
                </div>
                <script type="text/javascript">
            """

            net.set_options("""
            {
                "nodes": {
                    "font": {"size": 16, "strokeWidth": 2},
                    "borderWidth": 2,
                    "shadow": true,
                    "scaling": {
                        "min": 20,
                        "max": 60
                    }
                },
                "edges": {
                    "color": {
                        "inherit": false,
                        "color": "#666666",
                        "opacity": 0.8
                    },
                    "smooth": {"type": "continuous"},
                    "length": 200,
                    "width": 1.5
                },
                "physics": {
                    "barnesHut": {
                        "gravitationalConstant": -2000,
                        "centralGravity": 0.3,
                        "springLength": 200,
                        "springConstant": 0.04,
                        "damping": 0.09
                    },
                    "solver": "barnesHut",
                    "stabilization": {
                        "enabled": true,
                        "iterations": 1000,
                        "updateInterval": 25
                    }
                },
                "interaction": {
                    "hover": true,
                    "tooltipDelay": 200,
                    "zoomView": true,
                    "dragView": true,
                    "navigationButtons": true
                }
            }
            """)

            # Adicionar nós e arestas aqui
            nodes_data = []
            edges_data = []

            # Adicionar nós ao Network
            for node in G.nodes():
                node_data = G.nodes[node]
                node_label = str(node).split('/')[-1]  # Usar apenas o nome do arquivo como label
                
                net.add_node(
                    str(node),
                    title=node_data.get('title', str(node)),
                    color=node_data.get('color', '#4287f5'),
                    size=node_data.get('size', 30),
                    label=node_label,
                    physics=True,
                    shape='dot'
                )
                
                # Guardar dados do nó para JSON
                nodes_data.append({
                    'id': str(node),
                    'type': node_data.get('type', 'file'),
                    'label': node_label,
                    'full_path': str(node)
                })

            # Adicionar arestas com propriedades específicas
            for edge in G.edges():
                net.add_edge(
                    str(edge[0]), 
                    str(edge[1]),
                    physics=True,
                    smooth={'type': 'continuous'},
                    color={'color': '#666666', 'opacity': 0.8}
                )
                
                # Guardar dados da aresta para JSON
                edges_data.append({
                    'from': str(edge[0]),
                    'to': str(edge[1])
                })

            # Adicionar código de fechamento do HTML
            net.html += """
                    // Inicializar o grafo
                    var network = new vis.Network(container, data, options);
                </script>
            </body>
            </html>
            """
            # Salvar HTML
            with open(str(html_path), 'w', encoding='utf-8') as f:
                f.write(net.html)

            # Salvar dados do grafo
            graph_data = {
                'timestamp': timestamp,
                'nodes': nodes_data,
                'edges': edges_data,
                'stats': {
                    'total_nodes': len(G.nodes()),
                    'total_edges': len(G.edges()),
                    'directory': title.replace("Estrutura do Diretório: ", "")
                }
            }
            
            with open(data_path, 'w', encoding='utf-8') as f:
                json.dump(graph_data, f, indent=2, ensure_ascii=False)

            # Salvar visualização
            print(f"\nSalvando visualização em: {html_path}")
            print(f"Salvando dados do grafo em: {data_path}")
            
            return str(html_path)

        except Exception as e:
            print(f"Erro na visualização: {e}")
            traceback.print_exc()
            raise

    def handle_outline(self, prompt: str, config: dict) -> str:
        """Cria um esquema estruturado ou grafo de diretório"""
        print("\nDebug handle_outline:")
        print(f"Prompt recebido: {prompt}")
        print(f"Config: {config}")
        
        if "diretório" in prompt.lower():
            try:
                # Extrair o nome do diretório do prompt
                parts = prompt.lower().split("diretório")
                if len(parts) > 1:
                    # Pegar a última parte após "diretório" e limpar
                    directory = parts[-1].strip()
                    # Remover palavras comuns que podem aparecer no prompt
                    directory = directory.replace("como é o", "").replace("do", "").replace("da", "").strip()
                else:
                    directory = config.get('context_notes', [''])[0]
                
                print(f"Diretório encontrado: {directory}")
                
                if not directory:
                    return "Erro: Especifique um diretório no prompt ou em context_notes"
                
                print("Construindo grafo...")    
                G = self.build_directory_graph(directory)
                print(f"Grafo construído com {len(G.nodes())} nós e {len(G.edges())} arestas")
                
                print("Visualizando grafo...")
                self.visualize_knowledge_graph(G, f"Estrutura do Diretório: {directory}")
                
                return f"Grafo da estrutura do diretório '{directory}' gerado com sucesso!"
                
            except Exception as e:
                print(f"Erro detalhado ao gerar grafo: {str(e)}")
                traceback.print_exc()
                return f"Erro ao gerar grafo do diretório: {str(e)}"
        
        # Se não for visualização de diretório, criar esquema normal
        context = f"""Crie um esquema estruturado sobre o tema, com:
        - Tópicos principais
        - Subtópicos
        - Pontos-chave
        - Conexões entre conceitos
        
        Tema: {prompt}"""
        return self.query_ollama(config['model'], context)

    def build_directory_graph(self, directory_path: str) -> nx.Graph:
        """Constrói um grafo representando a estrutura de diretórios"""
        G = nx.Graph()
        base_path = self.vault_path / directory_path.strip('/')
        
        if not base_path.exists():
            raise ValueError(f"Diretório não encontrado: {directory_path}")
        
        def add_directory_to_graph(path: Path, parent: Optional[str] = None):
            current = str(path.relative_to(self.vault_path))
            
            if path.is_dir():
                G.add_node(current, type='directory')
            else:
                G.add_node(current, type='file')
                
            if parent:
                G.add_edge(parent, current)
                
            if path.is_dir():
                for item in path.iterdir():
                    if item.is_dir() or item.suffix.lower() == '.md':
                        add_directory_to_graph(item, current)
        
        add_directory_to_graph(base_path)
        return G

    def generate_graph_report(self) -> str:
        """Gera relatório básico do grafo"""
        return f"""# Relatório do Grafo
    Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """

    def load_cache(self):
        """Carrega o cache de resumos"""
        self.cache = {}
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'rb') as f:
                    self.cache = pickle.load(f)
            except Exception as e:
                print(f"Erro ao carregar cache: {e}")

    def save_cache(self):
        """Salva o cache de resumos"""
        self.cache_file.parent.mkdir(exist_ok=True)
        try:
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self.cache, f)
        except Exception as e:
            print(f"Erro ao salvar cache: {e}")

    def get_latest_config_from_vault(self) -> dict:
        """
        Busca a configuração mais recente na pasta self_questions
        
        Returns:
            Dict com configurações encontradas no YAML mais recente
        """
        try:
            config_path = self.vault_path / "self_questions"
            
            latest_file = None
            latest_time = 0
            
            for file in config_path.glob("*.md"):
                file_time = file.stat().st_mtime
                if file_time > latest_time:
                    latest_time = file_time
                    latest_file = file
            
            if not latest_file:
                raise ValueError("Nenhum arquivo de configuração encontrado em self_questions/")
                
            with open(latest_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if not content.startswith('---'):
                raise ValueError(f"Arquivo {latest_file.name} não contém metadados YAML")
                
            yaml_end = content.index('---', 3)
            yaml_content = content[3:yaml_end]
            config = yaml.safe_load(yaml_content)
            
            prompt = content[yaml_end + 3:].strip()
            
            required_fields = ['model', 'temperature']
            missing_fields = [field for field in required_fields if field not in config]
            if missing_fields:
                raise ValueError(f"Campos obrigatórios faltando: {missing_fields}")
                
            final_config = {
                'model': config.get('model', 'tinyllama'),
                'temperature': float(config.get('temperature', 0.1)),
                'context_notes': config.get('context_notes', []),
                'tags': config.get('tags', []),
                'prompt': prompt,
                'max_tokens': int(config.get('max_tokens', 2000)),
                'previous_context': config.get('previous_context', True),
                'file_path': latest_file,
                'data': config.get('data', datetime.now().strftime('%d/%m/%Y')),
                'hora': config.get('hora', datetime.now().strftime('%H:%M:%S'))
            }
            
            return final_config
            
        except Exception as e:
            print(f"Erro ao ler configuração: {str(e)}")
            raise

    def get_notes_from_path(self, path_or_note: str) -> List[Tuple[Path, str]]:
        """
        Obtém notas de um caminho ou nome de nota específico
        
        Args:
            path_or_note: Caminho da pasta ou nome da nota
        Returns:
            Lista de tuplas (caminho, conteúdo)
        """
        notes = []
        base_path = self.vault_path / path_or_note.strip('/')
        
        # Se é um caminho de diretório
        if ('/' in path_or_note) or ('\\' in path_or_note):
            if base_path.is_dir():
                # Busca recursivamente todos os arquivos .md no diretório
                for file_path in base_path.rglob("*.md"):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            notes.append((file_path, content))
                    except Exception as e:
                        print(f"Erro ao ler {file_path}: {e}")
            else:
                # Tenta encontrar arquivo específico
                if base_path.with_suffix('.md').exists():
                    try:
                        with open(base_path.with_suffix('.md'), 'r', encoding='utf-8') as f:
                            content = f.read()
                            notes.append((base_path.with_suffix('.md'), content))
                    except Exception as e:
                        print(f"Erro ao ler {base_path}: {e}")
        else:
            # Busca fuzzy por nome de nota
            matches = self.fuzzy_find_note(path_or_note)
            if matches:
                file_path = matches[0][0]
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        notes.append((file_path, content))
                except Exception as e:
                    print(f"Erro ao ler {file_path}: {e}")
        
        return notes
    
    def _validate_portuguese_response(self, response: str, model: str) -> str:
        """Valida se a resposta está em português e corrige se necessário."""
        spanish_indicators = ['del', 'la', 'el', 'los', 'las', 'una', 'pero', 'como', 'está', 'esta', 'muy']
        max_attempts = 3
        current_response = response
        
        for attempt in range(max_attempts):
            words = current_response.lower().split()
            spanish_count = sum(1 for word in words if word in spanish_indicators)
            
            if spanish_count <= 2:
                return current_response
                
            print(f"Detectada resposta em espanhol. Tentativa {attempt + 1}/{max_attempts}")
            
            # Preparar nova requisição diretamente para a API
            url = "http://localhost:11434/api/generate"
            new_prompt = f"""ATENÇÃO: Reescreva em português brasileiro (pt-BR):
            {current_response}
            
            IMPORTANTE: 
            1. Use APENAS português brasileiro
            2. Mantenha o mesmo conteúdo e estrutura
            3. Preserve termos técnicos
            4. NÃO use espanhol"""
            
            payload = {
                "model": model,
                "prompt": new_prompt,
                "system": "IMPORTANTE: Responda APENAS em português brasileiro (pt-BR).",
                "stream": True,
                "options": {
                    "temperature": 0.1,
                    "num_predict": 2048,
                    "stop": ["Spanish:", "Español:", "En español:"]
                }
            }
            
            try:
                response = requests.post(url, json=payload, stream=True)
                response.raise_for_status()
                
                new_response = ""
                for line in response.iter_lines():
                    if line:
                        try:
                            json_line = line.decode("utf-8")
                            data = json.loads(json_line)
                            new_response += data.get("response", "")
                            if data.get("done"):
                                break
                        except json.JSONDecodeError:
                            continue
                
                current_response = new_response.strip()
                
            except Exception as e:
                print(f"Erro ao tentar traduzir: {str(e)}")
                return current_response
        
        print("Limite de tentativas atingido. Retornando última resposta.")
        return current_response

    def query_ollama(self, model: str, prompt: str, context: Optional[str] = None, previous_context: str = "") -> str:
        """
        Consulta o modelo Ollama para processar comandos do Obsidian Assistant.

        Comandos Suportados:
        -------------------
        /resuma [elemento]
            Gera um resumo conciso do elemento especificado
            - Input: Nota ou conteúdo a ser resumido
            - Output: Resumo em 3 parágrafos com pontos principais
            - Exemplo: /resuma metodologia.md

        /explique [elemento]
            Fornece explicação detalhada do elemento
            - Input: Nota, conceito ou termo
            - Output: Explicação estruturada com conceitos e exemplos
            - Exemplo: /explique #metodologia-agil

        /desenhe [elemento]
            Gera visualização gráfica usando Pyvis
            - Input: Diretório, tag ou nota
            - Output: Arquivo HTML com grafo interativo
            - Exemplo: /desenhe diretório Notas/Projetos
            Nota: Usa funções build_directory_graph() e visualize_knowledge_graph()

        /encontre [termo]
            Realiza busca por termo específico
            - Input: Termo ou expressão de busca
            - Output: Lista ordenada de resultados com contexto
            - Exemplo: /encontre metodologia ágil

        /relacione [elemento1], [elemento2]
            Analisa relações entre elementos
            - Input: Dois elementos (tags, notas ou diretórios)
            - Output: Lista de conexões e suas relevâncias
            - Exemplo: /relacione #agile, #scrum

        Contextos:
        ---------
        context: Optional[str]
            - Contexto adicional para enriquecer a consulta
            - Pode incluir metadados, tags ou conteúdo relacionado
            - Adicionado ao prompt como "Contexto adicional"

        previous_context: str
            - Histórico de interações anteriores
            - Mantém continuidade na conversa
            - Adicionado ao prompt como "Contexto anterior"

        Args:
            model (str): Nome do modelo Ollama a ser usado
            prompt (str): Comando e parâmetros a serem processados
            context (Optional[str]): Contexto adicional para a consulta
            previous_context (str): Contexto de interações anteriores

        Returns:
            str: Resposta processada do modelo ou resultado da visualização

        Exemplos:
            >>> query_ollama("tinyllama", "/resuma nota.md", context="Tag: #projeto")
            "Resumo estruturado da nota..."

            >>> query_ollama("tinyllama", "/desenhe diretório Notas")
            "Grafo gerado em: self_graphs/graph_20240220_123456.html"
        """
        url = "http://localhost:11434/api/generate"

        # Processar referências a notas no prompt
        note_references = re.findall(r'\[\[(.*?)\]\]', prompt)
        note_contents = []
            
        for note_ref in note_references:
            try:
                # Limpar o nome da nota (remover aliases se houver)
                note_name = note_ref.split('|')[0] if '|' in note_ref else note_ref
                
                # Buscar conteúdo da nota
                notes = self.get_notes_from_path(note_name)
                if notes:
                    # Pegar o conteúdo da primeira nota encontrada
                    _, content = notes[0]
                    note_contents.append(f"Conteúdo da nota {note_name}:\n{content}")
            except Exception as e:
                print(f"Erro ao buscar nota {note_ref}: {e}")
                note_contents.append(f"Erro ao buscar nota {note_ref}")

        # Se encontrou conteúdo de notas, adicionar ao contexto
        if note_contents:
            additional_context = "\n\n".join(note_contents)
            if context:
                context = f"{additional_context}\n\n{context}"
            else:
                context = additional_context

        # System prompt mais direto e focado na execução
        system_prompt = """Você é um assistente especializado em análise de conhecimento do Obsidian.
        - Dá respostas ULTRA-CURTAS e diretas
        - Usa máximo 2 linhas para explicar
        - Se usar código, limita a 1 linha
        - Responde em português BR
        - Mantém termos técnicos em inglês
        - É breve e direto.
        - Cita uma explicação curta
        - Usa um uso prático e curto do conceito
        - Insere um ponto final
        - Sua resposta acaba SEMPRE antes do ponto final
        - No total teremos apenas uma explicação e um exemplo de uso do conceito

        IMPORTANTE: Você é sucinto. SEMPRE elabora uma resposta que não atinge o num_predict, pois ela acaba antes disso.
        
        Exemplo:
        - prompt: Como usar list comprehension em Python?
        - resposta: List comprehension (ou compreensão de lista) é um operador Python que permite criar uma lista a partir de outra lista ou iterável. A sintaxe básica para list comprehension é:
        ```python
        x = [i for i in range(10)]
        ```
        """

        # Adicionar instruções específicas baseadas no comando
        if prompt.startswith('/resuma'):
            system_prompt += """
            Ao receber /resuma:
            1. SEMPRE responda em português brasileiro
            2. Se o termo ou conteúdo estiver em outro idioma, não o altere
            3. Crie um resumo conciso em 3 parágrafos
            4 .Mantenha o foco no conteúdo fornecido
            5. Preserve termos técnicos de programação
            6. Finalize antes de atingor o num_predict
            7. Não liste comandos ou explique o processo"""
        
        elif prompt.startswith('/explique'):
            system_prompt += """
            Ao receber /explique:
            1. SEMPRE responda em português brasileiro
            2. Se o termo ou conteúdo estiver em outro idioma, não o altere
            3. Forneça uma explicação detalhada dos principais pontos do texto
            4. Liste os conceitos principais
            5. Inclua exemplos práticos quando possível
            6. Identifique relações importantes
            7. Não liste comandos ou explique o processo"""
        
        if prompt.startswith('/desenhe'):
            try:
                # Extrair o alvo da visualização
                target = prompt.replace('/desenhe', '').strip()
                
                if "diretório" in target.lower():
                    # Extrair o nome do diretório do prompt
                    parts = target.lower().split("diretório")
                    directory = parts[-1].strip()
                    # Remover palavras comuns que podem aparecer no prompt
                    directory = directory.replace("como é o", "").replace("do", "").replace("da", "").strip()
                    
                    print(f"Diretório encontrado: {directory}")
                    
                    if not directory:
                        return "Erro: Especifique um diretório no prompt"
                    
                    print("Construindo grafo...")    
                    G = self.build_directory_graph(directory)
                    print(f"Grafo construído com {len(G.nodes())} nós e {len(G.edges())} arestas")
                    
                    print("Visualizando grafo...")
                    return self.visualize_knowledge_graph(G, f"Estrutura do Diretório: {directory}")
                else:
                    # Para visualizações baseadas em tags ou outros elementos
                    G = self.build_knowledge_graph()
                    return self.visualize_knowledge_graph(G, f"Visualização: {target}")
                    
            except Exception as e:
                print(f"Erro detalhado na visualização: {str(e)}")
                traceback.print_exc()
                return f"Erro ao gerar visualização: {str(e)}"
        
        elif prompt.startswith('/encontre'):
            system_prompt += """
            1. SEMPRE responda em português brasileiro
            2. Se o termo ou conteúdo estiver em outro idioma, não o altere
            Ao receber /encontre:
            3. Busque o termo solicitado
            4. Liste resultados relevantes
            5. Ordene por relevância
            6. Inclua contexto breve para cada resultado
            7. Não liste comandos ou explique o processo"""
        
        elif prompt.startswith('/relacione'):
            system_prompt += """
            Ao receber /relacione:
            1. SEMPRE responda em português brasileiro
            2. Se o termo ou conteúdo estiver em outro idioma, não o altere
            3. Analise os elementos fornecidos
            4. Identifique conexões diretas e indiretas
            5. Liste as relações encontradas
            6. Explique a relevância de cada conexão
            7. Não liste comandos ou explique o processo"""
        
        # Incluir contextos no payload
        full_prompt = prompt
        if context:
            full_prompt += f"\n\nContexto adicional:\n{context}"
        if previous_context:
            full_prompt += f"\n\nContexto anterior:\n{previous_context}"

        num_predict = 2048  # valor padrão
        if context and isinstance(context, dict) and 'num_predict' in context:
            num_predict = context['num_predict']

        payload = {
            "model": model,
            "prompt": full_prompt,
            "system": "IMPORTANTE: Responda APENAS em português brasileiro (pt-BR). " + system_prompt,
            "stream": True,
            "options": {
                "temperature": 0.05,
                "num_predict": num_predict,
            }
        }

        try:
            response = requests.post(url, json=payload, stream=True)
            response.raise_for_status()
            
            full_response = ""
            for line in response.iter_lines():
                if line:
                    try:
                        json_line = line.decode("utf-8")
                        data = json.loads(json_line)
                        full_response += data.get("response", "")
                        if data.get("done"):
                            break
                    except json.JSONDecodeError:
                        continue
            
            return self._validate_portuguese_response(full_response.strip(), model)

        except Exception as e:
            print(f"Erro na consulta: {str(e)}")
            return f"Erro na consulta: {str(e)}"

    def build_knowledge_graph(self) -> nx.Graph:
        """Constrói um grafo de conhecimento baseado nas notas"""
        G = nx.Graph()
        
        # Percorre todas as notas markdown
        for file_path in self.vault_path.rglob("*.md"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Adiciona nó para a nota atual
                current_node = str(file_path.relative_to(self.vault_path))
                G.add_node(current_node)
                
                # Procura links para outras notas
                links = re.findall(r'\[\[(.*?)\]\]', content)
                for link in links:
                    if '|' in link:
                        link = link.split('|')[0]
                    G.add_edge(current_node, link)
                    
            except Exception as e:
                    print(f"Erro ao processar {file_path}: {e}")
        return G

    def validate_output(self, response: str) -> str:
        """Valida e corrige a saída do modelo"""
        if not response:
            return "Nenhuma resposta gerada."

        common_words = ["o", "a", "é", "de", "que", "e", "do", "da"]
        if not any(word in response.lower() for word in common_words):
            return "Erro: Resposta gerada não está em português."

        corrections = {
            "fomulário": "formulário",
            "resutados": "resultados",
            "armazeinar": "armazenar"
        }
        for wrong, correct in corrections.items():
            response = response.replace(wrong, correct)

        return response.strip()

    def handle_outline(self, prompt: str, config: dict) -> str:
        """Cria um esquema estruturado"""
        context = f"""Crie um esquema estruturado sobre o tema, com:
        - Tópicos principais
        - Subtópicos
        - Pontos-chave
        - Conexões entre conceitos
        
        Tema: {prompt}"""
        return self.query_ollama(config['model'], context)
    
    def analyze_vault_data(self, directory_path: Path) -> pd.DataFrame:
        """Analisa os dados do diretório e retorna um DataFrame estruturado"""
        try:
            print(f"\nAnalisando diretório: {directory_path}")
            
            if not directory_path.exists():
                print(f"Diretório não encontrado: {directory_path}")
                return pd.DataFrame()
                
            data = {
                'path': [],
                'name': [],
                'dir': [],
                'tags': [],
                'links': [],
                'n_tags': [],
                'n_links': [],
                'yaml_data': []  # Novo: armazenar metadados YAML
            }

            def extract_yaml_and_content(content: str) -> tuple[dict, str]:
                """Extrai YAML frontmatter e conteúdo do arquivo"""
                yaml_data = {}
                if content.startswith('---'):
                    try:
                        end_pos = content.find('---', 3)
                        if end_pos != -1:
                            yaml_text = content[3:end_pos].strip()
                            yaml_data = yaml.safe_load(yaml_text) or {}
                            content = content[end_pos + 3:].strip()
                    except Exception as e:
                        print(f"Erro ao processar YAML: {e}")
                return yaml_data, content

            def extract_tags(content: str, yaml_data: dict) -> set:
                """Extrai tags do conteúdo e do YAML"""
                # Tags do conteúdo (formato #tag)
                content_tags = set(re.findall(r'#([\w/-]+)', content))
                
                # Tags do YAML
                yaml_tags = set()
                if 'tags' in yaml_data:
                    if isinstance(yaml_data['tags'], list):
                        yaml_tags.update(str(tag) for tag in yaml_data['tags'] if tag)
                    elif isinstance(yaml_data['tags'], str):
                        yaml_tags.add(yaml_data['tags'])
                    elif isinstance(yaml_data['tags'], (int, float)):
                        yaml_tags.add(str(yaml_data['tags']))
                
                # Combinar e limpar tags
                all_tags = content_tags.union(yaml_tags)
                return {tag.strip() for tag in all_tags if tag.strip()}

            def extract_links(content: str) -> set:
                """Extrai links do conteúdo"""
                # Links wiki-style
                wiki_links = re.findall(r'\[\[(.*?)\]\]', content)
                # Links markdown
                md_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
                
                clean_links = set()
                
                # Processar wiki-links
                for link in wiki_links:
                    if '|' in link:
                        link = link.split('|')[0]
                    if '#' in link:
                        link = link.split('#')[0]
                    if link.strip():
                        clean_links.add(link.strip())
                
                # Adicionar links markdown
                for text, url in md_links:
                    if url.startswith(('http', 'https', 'ftp')):
                        continue  # Ignorar links externos
                    clean_links.add(url.strip())
                    
                return clean_links

            def process_file(file_path: Path) -> dict:
                """Processa um único arquivo e retorna seus dados"""
                try:
                    # Converter caminhos para lowercase para consistência
                    relative_path = str(file_path.relative_to(self.vault_path)).lower()
                    file_name = file_path.name.lower()
                    dir_path = str(file_path.parent.relative_to(self.vault_path)).lower()
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Extrair YAML e conteúdo
                    yaml_data, clean_content = extract_yaml_and_content(content)
                    
                    # Extrair tags e links
                    tags = extract_tags(clean_content, yaml_data)
                    links = extract_links(clean_content)
                    
                    # Debug para verificar tags encontradas
                    if tags:
                        print(f"\nTags encontradas em {file_path.name}:")
                        print(f"- Do YAML: {yaml_data.get('tags', [])}")
                        print(f"- Do conteúdo: {set(re.findall(r'#([\w/-]+)', clean_content))}")
                        print(f"- Tags finais: {tags}")

                    return {
                        'path': relative_path,
                        'name': file_name,
                        'dir': dir_path,
                        'tags': ','.join(sorted(tags)),
                        'links': ','.join(sorted(links)),
                        'n_tags': len(tags),
                        'n_links': len(links),
                        'yaml_data': yaml_data
                    }

                except Exception as e:
                    print(f"Erro ao processar {file_path}: {e}")
                    return None

            # Processar cada arquivo no diretório
            for file_path in directory_path.rglob('*.md'):
                file_data = process_file(file_path)
                if file_data:
                    for key in data:
                        data[key].append(file_data[key])

            # Criar DataFrame
            df = pd.DataFrame(data)
            
            # Estatísticas finais
            print(f"\nEstatísticas da análise:")
            print(f"Total de arquivos processados: {len(df)}")
            print(f"Diretórios encontrados: {df['dir'].nunique()}")
            print(f"Total de tags únicas: {len(set(','.join(df['tags'].dropna()).split(',')) - {''})}")
            print(f"Total de links únicos: {len(set(','.join(df['links'].dropna()).split(',')) - {''})}")
            
            return df
            
        except Exception as e:
            print(f"Erro na análise dos dados: {e}")
            traceback.print_exc()
            return pd.DataFrame()

    def handle_visualization(self, prompt: str, config: dict) -> str:
        try:
            print("\n=== Iniciando Visualização ===")
            
            # Limpar e processar o caminho do diretório
            target_dir = prompt.lower().replace('o diretório', '').strip()
            if not target_dir and config.get('context_notes'):
                target_dir = config['context_notes'][0]
            
            if not target_dir:
                return "Erro: Diretório não especificado"

            # Converter para objeto Path e normalizar
            try:
                target_path = Path(target_dir).resolve()
                print(f"Caminho completo: {target_path}")
                
                # Se o caminho é absoluto, tentar torná-lo relativo ao vault
                if target_path.is_absolute():
                    try:
                        target_path = target_path.relative_to(self.vault_path)
                        print(f"Caminho relativo ao vault: {target_path}")
                    except ValueError:
                        print("Usando caminho absoluto")
                
                # Verificar se o diretório existe
                full_path = self.vault_path / target_path
                if not full_path.exists():
                    return f"Erro: Diretório não encontrado: {full_path}"
                    
                print(f"Diretório encontrado: {full_path}")
                
            except Exception as e:
                print(f"Erro ao processar caminho: {e}")
                return f"Erro ao processar caminho do diretório: {str(e)}"

            # Criar estrutura de pastas organizada por data
            timestamp = datetime.now()
            output_dir = self.vault_path / "self_graphs" / timestamp.strftime("%Y/%m/%d")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            print(f"Diretório de saída criado: {output_dir}")
            
            # Nomes dos arquivos com horário
            time_prefix = timestamp.strftime("%H-%M-%S")
            html_path = output_dir / f"graph_{time_prefix}.html"
            excel_path = output_dir / f"data_{time_prefix}.xlsx"
            
            print(f"Arquivos a serem gerados:\n- Grafo: {html_path}\n- Excel: {excel_path}")

            # Analisar diretório
            print("\nAnalisando diretório...")
            df = self.analyze_vault_data(self.vault_path / target_path)
            
            if df.empty:
                return "Nenhum arquivo encontrado no diretório especificado"

            print(f"Encontrados {len(df)} arquivos para análise")

            # Salvar Excel com dados estruturados
            try:
                print("\nGerando arquivo Excel...")
                excel_data = {
                    'Arquivo': df['name'],
                    'Caminho': df['path'],
                    'Diretório': df['dir'],
                    'Tags': df['tags'],
                    'Links': df['links'],
                    'Qtd Tags': df['n_tags'],
                    'Qtd Links': df['n_links']
                }
                excel_df = pd.DataFrame(excel_data)
                excel_df.to_excel(excel_path, index=False, sheet_name='Dados do Vault')
                print(f"Excel salvo com sucesso em: {excel_path}")
            except Exception as e:
                print(f"Erro ao salvar Excel: {e}")
                traceback.print_exc()

            # Criar grafo com estilo aprimorado
            print("\nCriando grafo...")
            G = nx.Graph()
            file_color = '#4287f5'  # Azul
            tag_color = '#f54242'   # Vermelho
            
            # Adicionar nós de arquivo
            print("Adicionando nós de arquivo...")
            for _, row in df.iterrows():
                friendly_id = f"{row['dir']}/{row['name']}".lower()
                
                # Criar caminho absoluto para o arquivo
                file_path = self.vault_path / row['path']
                
                # Criar URL relativa ao servidor web local
                # Usamos caminho absoluto com file:/// para abrir diretamente no navegador
                file_url = f"file:///{str(file_path.absolute())}"
                
                # Tooltip com link direto para o arquivo
                tooltip = f"""<div style='background-color: white; padding: 10px; border-radius: 5px;'>
                    <b>Arquivo:</b> {row['name']}<br>
                    <b>Caminho:</b> {row['dir']}<br>
                    <b>Tags:</b> {row['tags']}<br>
                    <b>Links:</b> {row['links']}<br>
                    <div style='margin-top: 8px;'>
                        <a href='{file_url}' target='_blank' onclick='window.open(this.href); return false;'>
                            Abrir arquivo
                        </a>
                    </div>
                </div>"""
                
                G.add_node(
                    friendly_id,
                    title=tooltip,
                    label=row['name'],
                    color=file_color,
                    size=20,
                    group='file',
                    searchable=f"{row['name']} {row['dir']}".lower()
                )

            # Configurar visualização com permissão para links externos
            net = Network(
                height="750px",
                width="100%",
                bgcolor="#ffffff",
                font_color="black",
                select_menu=True,
                filter_menu=True,
                cdn_resources='remote'
            )

            # Adicionar configuração para permitir links externos
            net.set_options("""
            {
                "nodes": {
                    "font": {"size": 16, "strokeWidth": 2},
                    "borderWidth": 2,
                    "shadow": true
                },
                "edges": {
                    "color": {
                        "inherit": false,
                        "color": "#666666",
                        "opacity": 0.8
                    },
                    "smooth": {"type": "continuous"}
                },
                "interaction": {
                    "hover": true,
                    "tooltipDelay": 200,
                    "hideEdgesOnDrag": true,
                    "multiselect": true
                },
                "physics": {
                    "barnesHut": {
                        "gravitationalConstant": -2000,
                        "centralGravity": 0.3,
                        "springLength": 200
                    },
                    "stabilization": {"iterations": 50}
                }
            }
            """)

            # Finalizar e salvar grafo
            print("Salvando grafo...")
            net.from_nx(G)
            net.save_graph(str(html_path))
            
            print("\n=== Visualização concluída com sucesso! ===")
            
            return f"""Visualização gerada com sucesso!

    Arquivos gerados:
    - Grafo: {html_path.relative_to(self.vault_path)}
    - Dados: {excel_path.relative_to(self.vault_path)}

    Estatísticas:
    - Total de arquivos: {len(df)}
    - Total de tags: {df['n_tags'].sum()}
    - Total de links: {df['n_links'].sum()}
    - Diretórios analisados: {df['dir'].nunique()}"""
                    
        except Exception as e:
            print("\n=== ERRO NA VISUALIZAÇÃO ===")
            print(f"Erro detalhado:")
            traceback.print_exc()
            return f"Erro ao gerar grafo: {str(e)}"

    def process_prompt(self, config: dict) -> str:
        try:
            prompt = config['prompt']
            command, remaining = self.identify_command(prompt)
            
            if command in self.command_handlers:
                response = self.command_handlers[command](remaining, config)
            else:
                response = self.query_ollama(config['model'], prompt)
                
            self.save_to_md(prompt, response)
            return response
            
        except Exception as e:
            print(f"Erro ao processar prompt: {str(e)}")
            return f"Erro: {str(e)}"

    def save_to_md(self, prompt: str, response: str) -> str:
        """Salva a interação em arquivo markdown"""
        folder_name = self.vault_path / "self_talks" / datetime.now().strftime("%Y/%m/%d")
        file_name = f"{datetime.now().strftime('%H-%M-%S')}.md"
        file_path = folder_name / file_name

        folder_name.mkdir(parents=True, exist_ok=True)

        content = f"# Consulta: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n## Pergunta:\n{prompt}\n\n## Resposta:\n{response}\n"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

        print(f"Arquivo salvo em: {file_path}")
        return content

    def find_notes_by_tags(self, tags: List[str], content_filter: Optional[str] = None) -> List[Tuple[Path, str]]:
        """Busca notas por tags e conteúdo"""
        matching_notes = []
        tags = [tag.strip('#') for tag in tags]

        for file_path in self.vault_path.rglob("*.md"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    yaml_data = {}
                    if content.startswith('---'):
                        try:
                            end_yaml = content.index('---', 3)
                            yaml_content = content[3:end_yaml]
                            yaml_data = yaml.safe_load(yaml_content)
                            content = content[end_yaml + 3:]
                        except:
                            pass

                    found_tags = re.findall(r'#[\w/]+', content)
                    found_tags = [tag.strip('#') for tag in found_tags]
                    
                    if yaml_data.get('tags'):
                        found_tags.extend(yaml_data['tags'])

                    if any(tag in found_tags for tag in tags):
                        if content_filter:
                            if content_filter.lower() in content.lower():
                                matching_notes.append((file_path, content))
                        else:
                            matching_notes.append((file_path, content))
            except Exception as e:
                print(f"Erro ao ler {file_path}: {e}")

        return matching_notes

    def fuzzy_find_note(self, query: str) -> List[Tuple[Path, float]]:
        """Busca notas usando correspondência fuzzy"""
        matches = []
        for file_path in self.vault_path.rglob("*.md"):
            ratio = fuzz.ratio(query.lower(), file_path.stem.lower())
            if ratio > 60:
                matches.append((file_path, ratio))
        return sorted(matches, key=lambda x: x[1], reverse=True)

    def summarize_note(self, model: str, content: str, max_length: int = 500) -> str:
        """Gera um resumo da nota"""
        content_hash = hash(content)
        if content_hash in self.cache:
            cache_time, summary = self.cache[content_hash]
            if datetime.now() - cache_time < self.cache_duration:
                return summary

        prompt = f"""Faça um resumo conciso do seguinte texto, destacando os pontos principais:

{content}

Limite o resumo a aproximadamente {max_length} caracteres."""

        summary = self.query_ollama(model, prompt)
        
        self.cache[content_hash] = (datetime.now(), summary)
        self.save_cache()
        
        return summary

def main():
    try:
        vault_path = Path.cwd().parent.parent.parent
        print(f"\nIniciando assistente com vault em: {vault_path}")
        
        assistant = ObsidianAssistant(vault_path)
        
        # Lê configuração
        config = assistant.get_latest_config_from_vault()
        prompt = config['prompt'].lower()
        
        # Tratar comando desenhe diretamente
        if any(prompt.startswith(cmd) for cmd in ['desenhe', '/desenhe']):
            print("\nComando de visualização detectado")
            # Remover 'desenhe' ou '/desenhe' do prompt
            clean_prompt = prompt.replace('desenhe', '').replace('/desenhe', '').strip()
            response = assistant.handle_visualization(clean_prompt, config)
            print("\nProcessamento concluído!")
            print(response)
            return  # Importante: retornar aqui para evitar self_talks
            
        # Outros comandos
        response = assistant.process_command(config)
        print("\nProcessamento concluído!")
        print(response)
        
    except Exception as e:
        print(f"\nErro no processamento principal: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
```

This whay i can ask some question, make conection to some ideias an talk whit you data. All by your self. It work fine.In my case better than any plugin. 
The last created file on the self_questions folder is anwsered in the self_grahs one. If some graphs are out put, they are stored at self_graphs. Like this one bellow:
![logo Description](/images/self_graph.png)
## Summary
This guide provides a comprehensive walkthrough for setting up Ollama on your local machine, integrating various AI models, managing user access, and enhancing your setup with tools like Stable Diffusion and BMO. By following these steps, you can create a robust and flexible AI environment tailored to your specific needs.

### Common Issues
- **Ollama not running:** Ensure the installation script executed without errors and that WSL is properly installed.
- **Docker issues:** Verify Docker is installed correctly and that the Docker daemon is running.
- **Model not appearing in Web UI:** Ensure the model was pulled successfully using `ollama pull [model_name]`.
- **Stable Diffusion installation errors:** Check that all prerequisites are installed and that Pyenv is configured correctly.

### Regular Tasks
- **Update AI models:** Regularly pull updates for your AI models using Ollama.
- **Backup configurations:** Keep backups of your Docker configurations and AI models.
- **Monitor system resources:** Ensure your system can handle the resource demands of running multiple AI models.

### Considerations
Setting up a local AI environment provides greater control over your data and models. It allows for customization and integration with various tools, enhancing productivity and enabling advanced functionalities. While the initial setup requires technical knowledge, the long-term benefits make it a worthwhile investment for AI enthusiasts and professionals alike.

## References
- [Host All Your AI Locally](https://www.youtube.com/watch?v=Wjrdr0NU4Sk)
