"""
Problem Tanımı
    - Kullanıcılar yazılı olarak soru soracak, gerçek zamanlı ve doğal şekilde yanıtlar alabilecek
    - Akıllı turizm rehberi → TR özelinde
    - Türkiye özelinde tarihi yerler, kültürel etkinlikler, yemekler, ulaşım ... [ÖDEV] Dünya özelinde yapacağız.




LLaMa
    - LLaMa da bir sürü modeli vardır. Her modele ait parametre sayıları farklı alt modeller var. 
    - LLaMa 3.2B kullanacağız. Streamlit ile görselleştireceğiz.
    - Streamlit → UI framework
    LLaMa (Large Language Model Meta AI):
        • GPT benzeri yapay zeka modellerine alternatif olarak geliştirildi.
        • Açık kaynaklı. Akademik ve ticari kullanımlarda uygundur
        • Ticari kullanım için şartlar var. Aylık kullanıcı sayısı limiti, kullanılacak algoritmaların isminde LLaMa geçecek... Gemini ve GPT ye göre avantajı açık kaynaklı olması
        • Daha az parametre ile daha iyi performans sergilediği için → Verimli
        • Modüler → 1B, 3B, 8B, 70B parametreye sahipmodelleri var
        • Lokalde çalışabilir.
        • Bu avantajlardan dolayı ticari projelerde sıklıkla kullanılır.
        Dezavantajları:
        • Türkçe'de sıkıntılar çıkabilmekte

Plan/Program


install libraries:
    pip install langchain==0.3.7
    pip install langchain ollama langchain_community

    pip freeze > requirements.txt
import libraries


ollama -> llama modellerini lokalde çalıştırmayı sağlayan kütüphane. 
    1. ollama indir: https://ollama.com/download
    2. llama3.2:2b indir: https://ollama.com/library/llama3.2:3b
            ```bash
            ollama run llama3.2:3B
            ```
        Win+R → cmd → ollama run llama3.2:3b (sadece ollama yazınca da kurulup kurulmadığını anlayabiliriz ve komutları görebiliriz)
        mevcuttaki modelleri görüntülemek için 
            ```bash
            ollama list
            ```
        
Langchain sürümü farklı olduğu için env yi silip tekrar başlat
    Remove-Item -Recurse -Force .venv

    olmazsa;
    rmdir .venv -r -fo
"""

# import libraries
from langchain_community.chat_models import ChatOllama # ollama llm arayüzü
from langchain.schema import SystemMessage, HumanMessage # chat mesaj sınıfları
from langchain.memory import ConversationBufferMemory # konuşma geçmişi için basit bir hafıza

# llama model 
llm = ChatOllama(model="llama3.2:3b")

# memory
# hafıza ekleme, konuşma geçmişi takip etme
memory = ConversationBufferMemory(return_messages=True) # return_message parametresi trueolduğunda düzgün formatlı, okunabilir gelir.


# welcome message
print("Akıllı turizm rehberine hoş geldiniz.")
print("Size gezilecek yerler, tatil önerileri ve ulasım bilgileri gibi konularda yardımcı olabilirim.")

# terminal üzerinden llama ile konuşma:
while True:
    user_input = input("Siz: ")
    if user_input.lower() == "quit":
        print("Program sonlandırıldı")
        break

    # Software design decision
    # 1. User input memory ye atılsın mı?
    # 2. Chat bittikten sonra mı memory'ye atılsın?

    # kullanıcının mesajlarını hafızaya kaydederiz.
    memory.chat_memory.add_user_message(user_input)


    # model için gerekli olan tüm mesajları oluşturalım: sistem mesajı + memory + human messagr
    messages = [
        SystemMessage(content="Sen bir akıllı turizm rehberisin."
                      "Kullanıcılara Türkiye'deki şehirler, tarihi yerler, yöresel yemekler, ulaşım ve tatil önerileri hakkında yardımcı ol.")
    ] + memory.load_memory_variables({})["history"] +  [HumanMessage(content=user_input)]


# modelden yanıt alma
response = llm(messages)


# modelin cevabını hafızaya ekle
memory.chat_memory.add_ai_message(response.content)


print(f"Rehber AI: {response.content}")

"""
1) Streaming özelliği aktif olmadığı için yazılan her parçayı anında göremiyoruz. LLaMa'nın Türkçe dil desteği yok (önemli çalışma yapabiliriz). Ayrıca yavaş çalışmakta




[NOTE] dinamik yapı için, özellikle etkinlikler hakkında cevap verilirken web search özelliği eklemek gerekir. 
       
"""

# chat on terminal