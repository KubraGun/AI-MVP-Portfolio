NOT1: Langchain in ayrıldığı güncellemeden önceki son versiyon kullanılıyor. 
[ÖDEV] v1 Langchain ile bu projeyi yeniden yap

## Flowchart
Library installation
↓
import libraries


## Streamlit
ML/AI Engineering uygulamaları için geliştirilmiş bir UI framework'üdür. Geliştirilen projelerin web arayüzünü basitçe oluşturmamızı sağlar. Alternatif Gradio



## Error
ValueError: Ollama call failed with status code 500. Details: {"error":"model requires more system memory than is currently available unable to load full model on GPU"}
Koddan kaynaklı değil hata. Sistem belleği yetmiyor. buluta bağlayarak tekrar çalıştır.
RAM'de modelin "quantized" sürümü değil tam sürümü çağırılıyor olabilir.

→ Çözüm için daha küçük model kullanılabilir. ChatOllama oluşturulduğu yerde modeli değiştir.

→ GPU VRAM yetersiz olduğunda CPU yu zorlamak için:
```bash
ollama run --num-thread --gpu false llama3.2:3b
```

Bu işlemi kod dosyasında en kullanarak yapabilirim
```python
import os

os.environ["OOLAMA_NUM_THREAD"] = "6"
os.environ["OLLAMA GPU"] = "false"
```


→ Tüm sürüm yerine quantized sürümü indir ve kullan
```bash
ollama pull llama3.2:3b-q4_K_M
```

ardından;

```python
llm = ChatOllama(model="llama3.2:3b-q4_K_M")
```

→ Daha önce çalıştırdığım LLaMa ile çakışıyor olabilir
```bash
ollama stop all
```
Ardından;
```bash
ollama list
```


Kısaca karşılaştığım hatanın sabebi:

|Neden                               |Çözümü                          |
|------------------------------------|--------------------------------|
|GPU bellek yetersizliği             | llama3.2:1b veya 3b-q4_K_M     |
|Ollama eski çalışan model çakışması | ollama stop all                |
|CPU yetersiz (Chrome çok harcıyor)  | ollama run --gpu false         | 
|Model tam sürümde (quantized değil) | ollama pull llama3.2:3b-q4_K_M |


## Terminal Tourist Bot (`terminal_tourist_bot.py`)
START

│

├─ Import libraries (ChatOllama, SystemMessage, HumanMessage, ConversationBufferMemory)

│

├─ Initialize LLM with llama3.2:3b model

│

├─ Create memory buffer for conversation history

│

├─ Display welcome message

│

└─ ENTER MAIN LOOP:

│

├─ Wait for user input

│

├─ IF input == "quit" → BREAK LOOP

│

├─ ELSE:

│ │

│ ├─ Add user message to memory

│ │

│ ├─ Construct messages array:

│ │ 1. System role instruction

│ │ 2. Conversation history from memory

│ │ 3. Current user input

│ │

│ ├─ Send to LLM for processing

│ │

│ ├─ Receive complete response

│ │

│ ├─ Add AI response to memory

│ │

│ └─ Display response in terminal

│

└─ REPEAT LOOP

## Basic Streamlit Bot (`streamlit_tourist_bot.py`)

START

│

├─ Import Streamlit and LangChain components

│

├─ Configure Streamlit page (title, icon, description)

│

├─ INITIALIZE SESSION STATE:

│ │

│ └─ IF no memory exists → Create ConversationBufferMemory

│

├─ Load Llama model

│

├─ Display chat input field

│

├─ RENDER EXISTING CHAT HISTORY:

│ │

│ ├─ FOR each message in memory:

│ │ │

│ │ ├─ IF HumanMessage → Display in user bubble

│ │ │

│ │ └─ ELSE → Display in AI bubble

│

└─ ON NEW USER INPUT:

│

├─ Add user message to memory

│

├─ Build messages array:

│ System prompt + History + Current input

│

├─ Get response from LLM (complete generation)

│

├─ Store AI response in memory

│

└─ Trigger UI refresh to show new messages


## Streaming Streamlit Bot (`streamlit_tourist_bot_streaming.py`)
START

│

├─ Import streaming-specific callbacks

│

├─ DEFINE StreamHandler class:

│ │

│ ├─ init: Store placeholder reference

│ │

│ └─ on_llm_new_token: Append token and update UI

│

├─ Streamlit page configuration

│

├─ Initialize session memory

│

├─ Display chat history (same as basic version)

│

└─ ON USER INPUT:

│

├─ Store user message in memory

│

├─ Display user message immediately

│

├─ Create empty response placeholder

│

├─ Initialize StreamHandler with placeholder

│

├─ Configure LLM with streaming enabled + callback

│

├─ Build messages array

│

├─ Send to LLM → Tokens stream to handler in real-time

│

└─ Final response stored in memory after completion


## Core Algorithm Pattern 
Memory Management:

User Input → Add to Memory → Process → AI Response → Add to Memory

↑ │
└──────────────────────────────────────┘


Message Construction:

[System Role] + [Message History] + [Current Query] → LLM → Response

System Role Constant:

"You are a smart tourism guide specializing in Turkish destinations,
historical sites, local cuisine, and travel recommendations."


## Key Technical Decisions

1. **Memory Strategy**: ConversationBufferMemory preserves full context
2. **Model Choice**: Llama 3.2 3B balances performance and local operation
3. **Streaming vs Batch**: Trade-off between responsiveness and simplicity
4. **State Management**: Session state for web, object persistence for terminal
5. **Error Handling**: Basic input validation with graceful degradation