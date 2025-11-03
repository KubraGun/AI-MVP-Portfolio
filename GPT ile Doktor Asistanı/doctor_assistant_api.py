"""
Fast API ile GPT Doktor Asistan

Her kullanıcı için ayrı bir conversationBufferMemory tutacağız


"""

import os
from typing import Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# ortam değişkenleri
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


# FastAPI uygulamasını başlat
app = FastAPI(title="Doktor Asistanı API")

# LLM conf.
llm = ChatOpenAI(
    model = "gpt-3.5-turbo",
    temperature = 0.7, 
    openai_api_key = api_key
)

# Memory conf.
user_memories: Dict[str, ConversationBufferMemory] = {}

# istek ve yanıt şemaları
class ChatRequest(BaseModel): 
    name: str
    age: int
    message: str

class ChatResponse(BaseModel): 
    response: str


# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat_with_doctor(request: ChatRequest):
    try: 
        # hafıza varsa usermemory de olur. onu getiririz. Yoksa hafızayı yarat
        if request.name not in user_memories:
            user_memories[request.name] = ConversationBufferMemory(return_messages=True)

        memory = user_memories[request.name]

        #intro mesajını 1 kereliğine ekleyelim
        if len(memory.chat_memory.messages) ==  0: # konuşma olmamış
            intro = (
                f"Sen bir doktor asistanısın. Hasta: {request.name}, {request.age} yaşında."
                "Sağlık sorunları hakkında konuşmak istiyor."
                "Yaşına uygun dikkatli ve nazik tavsiyeler ver."
                "Kullanıcıya ismiyle hitap et"
            )       

            memory.chat_memory.add_user_message(intro)

        # llm ile memory birleştir → chain oluşturma
        conversation = ConversationChain(llm=llm, memory=memory, verbose=False)
        reply = conversation.predict(input=request.message)


        # Hafızayı terminale yazdıralım
        print(f"\nMemory: ")
        for idx, m in enumerate(memory.chat_memory.messages, start=1): # indeksi 1 den başlatırız
            print(f"{idx:02d}. {m.type.upper()}: {m.content}")
        print("-------------------------------------------------------------------------------")

        return ChatResponse(response=reply)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        # Bir endpoint oluştururken try-except mutlaka yazılmalı. çünkü kullanıcıdan kaynaklanmayan bir sürü hata çıkabilir