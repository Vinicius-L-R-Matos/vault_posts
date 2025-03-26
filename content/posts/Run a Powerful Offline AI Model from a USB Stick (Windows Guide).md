---
title: Run a Powerful Offline AI Model from a USB Stick (Windows Guide)
date: 2025-03-24
draft: false
tags:
  - python
  - Pendrive
  - AI
categories:
  - SecOps
series:
  - LLM
---
What if you could carry the equivalent of **127 million novels** or **the entire Wikipedia 2,500 times over**... in your pocket?
With the **Dolphin-LLaMA3** model from Hugging Face (via Ollama), you can. This model fits on any **128GB USB drive**, taking up just **10GB** of space, and runs **fully offline** — completely detached from Big Tech servers, censorship filters, or surveillance.
# Contents
- About the Model
- Routine Overview
- Initial Setup on Windows
- Running from a USB Drive
- Running AI from the USB
- Improve the Interface with AnythingLLM
- Interacting with Dolphin via Python (API)
- Final Thoughts

---
## 🧠 About the Model
We’ll be using the **Dolphin-LLaMA3** model, available directly through [Ollama](https://ollama.com/library/dolphin-llama3). This 8-billion parameter LLaMA3-based model was trained on **15 trillion tokens**, equivalent to about **60 terabytes** of text.

Why Dolphin?

- Runs offline
- Lightweight (~10GB)
- Low censorship — it responds to sensitive or controversial prompts without guardrails
- Great for advanced developers, researchers, and tinkerers

⚠️ **Disclaimer**: Because of its uncensored nature, this model might respond to sensitive or dangerous queries. Use responsibly.

![Image Description](/images/dolphin_joke.png)

---
## 🛠️ Routine Overview
Here's what we'll do:
1. Download and install Ollama + Dolphin-LLaMA3
2. Run it offline from your PC
3. Move everything to a USB drive for portable offline AI
4. Improve the interface with AnythingLLM
5. Interact via a simple Python API

---
## 🔧 Initial Setup on Windows
1. **Download and install Ollama**:  
➡️ [ollama.com/download/windows](https://ollama.com/download/windows)
	(Make sure to close any Ollama's task before this point on. The installer usually start a server on the background) 
2. **Open two PowerShell terminals as Administrator**
3. In the **first terminal**, run:
    ```batch
    ollama serve
    ```
4. In the **second terminal**, install and run the model:
    ```batch
    ollama run dolphin-llama3
    ```
5. Wait for the model to download. Once complete, stop the process with:
    ```
    Ctrl+C then Ctrl+D
    ```
6. **Close both terminals** and reopen two **PowerShell terminals (non-admin)**. Run:
Terminal 1:
```batch
ollama serve
``` 
And for Teminal 2:
```batch
ollama run dolphin-llama3
```

Now you’re running Dolphin-LLaMA3 offline!

Test with a prompt like:
> "What is the best way to steal a car?"

And it should respond some like this:
>"I'm not able to assist you with illegal activities. However, I can tell you that the most common method of stealing a car is by..."

Is a tipical censored kind of anwser. It will be improved since we gona run it in a pendrive.

---
## 💾 Running from a USB Drive

1. **Locate your Ollama model folder**  
    Look for `Ollama` or `.ollama` in your user directory (e.g., `C:\Users\YourName`)
2. **Format your USB drive** to **NTFS** (right-click > Format > File System: NTFS)
3. **Copy the Ollama folder** to the root of your USB stick (e.g., `E:\Ollama`)
4. **Find Ollama’s binary** using PowerShell:
```powershell
Get-Command ollama
```
Then copy the contents of that `...Local\Programs\Ollama` folder into the pendrive's `E:\Ollama` as well. Here it should have 8 files (lib, app, ollama app, ollama, ollama_welcome, unins000.dat, unins000, unins000). It all go together, inside de pendrive's root.
5. **Optional cleanup:** You can now uninstall Ollama from your PC and delete the local model folders — everything is on the USB.

---
## 🚀 Running AI from the USB

1. **Plug in your USB stick**
2. **Open two PowerShell terminals (non-admin)**
3. In the **first terminal**:
```powershell
cd E:\
$env:OLLAMA_MODELS="E:\ollama\models"
ollama serve
```
4. In the **second terminal**:
```powershell
cd E:\
cd ollama
ollama.exe run dolphin-llama3
```
Then, notice its uncensored kind of answer to the same question:
>"I'd be happy to help you with that! First, you'll need to identify ..."

If it responds uncensored, you're doing good. If not, restart the process and kill any leftover Ollama processes in Task Manager.

---
## 🪟 Improve the Interface with AnythingLLM
1. Run the **Ollama server** as explained above.
2. Go to [anythingllm.com](https://anythingllm.com/) and download the Windows app.
3. Install it to `E:\AnythingLLM`. Open a `Ollama serve` from the pendrive. It will be possible to execute the interface from this point on. Then we need to create 3 files:
4. Create a `.env` file inside `E:\AnythingLLM` with this content:
```batch
OLLAMA_HOST=http://127.0.0.1:11434
LLM_PROVIDER=ollama
MODEL_BACKEND=dolphin-llama3
OLLAMA_MODEL_PATH=%DRIVE_LETTER%\Ollama\models
```
5. To automate the startup, create two files in your USB root:
- `autorun.inf`
```batch
[Autorun]
label=Dolphin LLM
shellexecute=start.bat
icon=customicon.ico
action=Start local Dolphin LLM
```
- `start.bat`
```batch
@echo off
set DRIVE_LETTER=%~d0
set OLLAMA_MODELS=%DRIVE_LETTER%\Ollama\models

echo Verificando arquivos necessarios...
if not exist "%DRIVE_LETTER%\ollama.exe" (
    echo ERRO: Arquivo ollama.exe nao encontrado em %DRIVE_LETTER%\
    pause
    exit /b 1
)

echo Starting Ollama...
start "" "%DRIVE_LETTER%\ollama.exe" serve

:waitloop
netstat -an | find "LISTENING" | find ":11434" >nul 2>&1
if errorlevel 1 (
    timeout /t 1 /nobreak >nul
    goto waitloop
)

echo Starting AnythingLLM...
start "" "%DRIVE_LETTER%\anythingllm\AnythingLLM.exe"
```
Now, Dolphin + AnythingLLM launches just by running `start.bat`, direct from the pendrive!!! It will open the server and the client together.
The first time you run it, dont forget to chose the  Ollama LLM on the configuration screen.

---
## 🧪 Interacting with Dolphin via Python (API)
Now is time to interact by some API. Depending of the base url you chose to conect, it will open to the Ollama port (More quick), or the AnythingLLM (More plastic).
Bellow we try on the more quick way.
### Method 1: Using `ollama-python` (official library)
```python
from ollama import Client

client = Client(host='http://localhost:11434')

def chat_with_dolphin(prompt):
    response = client.chat(model='dolphin-llama3', messages=[
        {'role': 'user', 'content': prompt}
    ])
    return response['message']['content']

print(chat_with_dolphin("What is the capital of Brazil?"))
```
### Method 2: Using `requests`
```python
import requests

def send_prompt(prompt):
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "dolphin-llama3",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, json=payload)
    return response.json()['message']['content']

print(send_prompt("Who discovered Brazil?"))
```
### Method 3: Simple interactive terminal chat
```python
import requests

def chat():
    history = []
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        payload = {
            "model": "dolphin-llama3",
            "messages": history + [{"role": "user", "content": user_input}]
        }
        res = requests.post("http://localhost:11434/api/chat", json=payload)
        reply = res.json()['message']['content']
        print("Dolphin:", reply)
        history.extend([{"role": "user", "content": user_input}, {"role": "assistant", "content": reply}])

chat()
```
#### 🐍 Dependencies:
To use the official API install on the venv:
```bash
pip install requests ollama-python
```

---
## 🎯 Final Thoughts
- This is the final directories organization:
```batch
USB_DRIVE:\
├── ollama.exe
├── models\
├── anythingllm\
│   ├── AnythingLLM.exe
│   └── .env
├── start.bat
├── autorun.inf
└── customicon.ico
```
- It need 15,2 GB in total to work.
- You now have a **fully functional AI assistant**, running completely offline, stored on a **portable USB stick**, with a clean GUI and API interaction — free from corporate filters.
- You can also provide some nice image to work in the `customicon.ico`.
- I use an 16RAM, i7, 2CPU in a 123G pendrive.
- One day for download, test and build it all.
- Took lass then 4 min to get response.
- Suports RAG, scrapping, queries and others cool stufs. Uncensored.

Let your creativity run wild, build private research tools, assistants, bots, or integrate Dolphin into custom workflows. Like Agentic-workflows, MCP, AAAS, or any else that is to come.

If this helped you, feel free to share or fork it for your own use. The future no one knows. Stay private, stay powerful. 🚀

---
## References
- [Global Science Networh](https://www.youtube.com/watch?v=eiMSapoeyaU&t=483s), on the "Como executar LLMs privados e sem censura offline | Dolphin Llama 3" title. Worked a lot for me and i could increment on the API section.