"""
Problem Tanımı:
Kullanıcının sağlıkla ilgili sorularınıanlayan ve yanıtlayan GPT tabanlı doktor asistanı chatbot
    - Kullanıcının yaşını ve adını dikkate alan cevaplar üretilecek
    - Mesaj geçmişini hatırlayarak diyaloğu ona göre sürdürmeli "memory"
    - Langchain ve OPENAI GPT
    - İlk olarak terminal tabanlı olarak, sonrasında FastAPI tabanlı web service
    - Python request ile client tarafını test edeceğiz

    LANGCHAIN
        - LLM ile proje gerçekleştirilen açık kaynaklı LLM kütüphanesi. Ticari uygulamalarda her dil modelinin sağladığı API ler yerine LangChain daha kolaylık sağlar. Bütün LM'ler için bütün yöntemler aynıdır. Ekstra doc okumaya gerek kalmaz
        - prompt yönetimi
        - memory
        - tool entegrasyonu: ai agents için tool kullanımı
        - chain yapısı: multi-agent process'ler yönetilebilir, RAG gibi yöntemleri chain ile yönetebiliriz.
        
Veri Seti:
    - Veri seti yok. Hazır GPT modelini kullanarak prompt ayarlaması yapılacak. (Gerçek hayattaki kritik halüsinasyonları önlemek için fine tune işlemi yapılabilir.)

Model Tanıtımı:
    - GPT (Generative Pre-Trained Transformer) ile oluşturulan gpt-3.5-turbo (bu şnsan gibi metin üretebiliyor, sorulara mantıklı cevaplar üretebiliyor, önerilierde bulunabiliyor, sohbet edebilir, kod yazabiliyor.)
    - API üzerinden iletişim kurarak gerçek zamanlı sağlık önerileri alınacak

API tanımlama:
    - Search on google "openai api pricing"
            https://openai.com/tr-TR/api/pricing/ → 3.5 turboyu buradan kaldırmışlar
            https://platform.openai.com/docs/pricing → gpt 3.5 turbo input maliyeti 4 ten fazla 
             Bu projeyi bir de gpt-4.1-nano-2025-04-14 ile geliştirip performans karşılaştırması yap
    


install libraries:
    - fastapi : Web uygulamaları geliştirmek için modern hızlı framework (asenkron)
    - uvicorn : fastapi yi çalıştımak için gereken sunucu
    - langchain
    - python-dotenv: .env'den gizli bilgileri almak için
    - langchain_community

import libraries
"""

# import libraries → fast api
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain



# Ortam değişkenleri
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")



# LLM + memory
llm = ChatOpenAI(
    model = "gpt-3.5-turbo",
    temperature = 0.7, # ne kadar gerçekçi ne kadar hayal ürünü 0 - 1  0 a yakınsa garanti cevap verir 1 e yakınsa daha çok düşünür halüsinasyon riski artar
    openai_api_key= api_key
)

# hafıza
memory = ConversationBufferMemory(return_messages=True)


# chain'de birleştirilir
conversation = ConversationChain(llm=llm, memory=memory, verbose=True)


# Kullanıcı bilgilerini al → isim ve yaş
name = input("İsminiz: ")
age = input("Yaşınız: ")

# intro ve outro mesajlarını buradan manuel yazalım, boşuna maliyeti artırmayalım
intro = (
    f"Sen bir doktor asistanısın. Hasta {name}, {age} yaşında."
    "Sağlık sorunları hakkında konuşmak istiyor."
    "Yaşına uygun dikkatli ve nazik tavsiyeler ver; ismi ile hitap et."
)
# introyu llm e gönderelim
memory.chat_memory.add_user_message(intro)

print("Merhaba, ben bir doktor asistanıyım, size nasıl yardımcı olabilirim?")

# identification chatbot loop
while True:
    # Hasta sorar
    user_msg = input(f"{name}: ")
    if user_msg.lower() == "quit": # konuşmayı sonlandır
        print("Sana yardımcı olabildiysem ne mutlu bana, görüşmek üzere")
        break

    # Asistan cevap verir
    reply = conversation.predict(input = user_msg) # llm cevabı
    print(f"Doktor Asistanı: {reply}")

    # bu ana kadar memory yoktu. ilk mesaj haricinde. Hasta soracak asistan cevap verecek ve memory ye gidecek
    # verilen cevabı kaydet (terminal için yazdıralım)
    print("Hafiza: ")
    for idx, m in enumerate(memory.chat_memory.messages, start = 1):
        print(f"{idx:02d}. {m.type.upper()}: {m.content}")
    print("___________________________________________________________")

"""
İsminiz: Kübra
Yaşınız: 25
Merhaba, ben bir doktor asistanıyım, size nasıl yardımcı olabilirim?
Kübra: Merhaba, karnım ağrıyor

[NOTE1] Burada verbose=True dediğimiz için aşağıdaki bilgileri veriyor
> Entering new ConversationChain chain...
Prompt after formatting:
The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.

Current conversation:
[HumanMessage(content='Sen bir doktor asistanısın. Hasta Kübra, 25 yaşında.Sağlık sorunları hakkında konuşmak istiyor.Yaşına uygun dikkatli ve nazik tavsiyeler ver; ismi ile 
hitap et.')]
Human: Merhaba, karnım ağrıyor
AI:

> Finished chain.
Doktor Asistanı: Merhaba Kübra, karnın nerede ağrıyor? Ağrının şiddeti ne kadar? Ne zamandan beri bu ağrıyı hissediyorsun? Beslenme alışkanlıkların hakkında biraz bilgi verebilir misin? Bu bilgiler ışığında sana daha iyi bir tavsiyede bulunabilirim.
Hafiza:
01. HUMAN: Sen bir doktor asistanısın. Hasta Kübra, 25 yaşında.Sağlık sorunları hakkında konuşmak istiyor.Yaşına uygun dikkatli ve nazik tavsiyeler ver; ismi ile hitap et.   
02. HUMAN: Merhaba, karnım ağrıyor
03. AI: Merhaba Kübra, karnın nerede ağrıyor? Ağrının şiddeti ne kadar? Ne zamandan beri bu ağrıyı hissediyorsun? Beslenme alışkanlıkların hakkında biraz bilgi verebilir misin? Bu bilgiler ışığında sana daha iyi bir tavsiyede bulunabilirim.
___________________________________________________________

....
"""