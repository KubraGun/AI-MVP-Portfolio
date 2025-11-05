"""
web üzerinde çalışan chatbot ekranı 

"""

import streamlit as st
from langchain_community.chat_models import ChatOllama
from langchain.schema import SystemMessage, HumanMessage # Sohbet mesajları
from langchain.memory import ConversationBufferMemory # hafıza yönetimi

# başlık ve açıklamalar
st.set_page_config(page_title="Akıllı Turist Rehber", page_icon="🌍")
st.title("🌍 Akıllı Turist Rehberi")
st.markdown("Türkiye'ni dört bir yanındaki turistik yerler hakkında bilgi almak için sorular sorabilirsiniz.")

# session state
# Amaç: streamlit'teki kullanıcı geçmişini tutmak
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True) # Mesaj geçmişi

# llama3.2:3b modelini yükle
llm = ChatOllama(model="llama3.2:3b")

# mesaj kutusu 6 kullanıcıdan gelen mesaj (terminal için input)
user_input = st.chat_input("Bir şehir, mekan, yemek ya da aktivite sorabilirsiniz...")

if user_input: 
    # eğer user input varsa yeni gelen kullanıcı mesajını ilk olarak memory ye ekleriz
    st.session_state.memory.chat_memory.add_user_message(user_input)

    # tüm konuşmayı mpdele verecek şekilde mesajları oluşturur → systemmesage+memory+human
    messages = [
        SystemMessage(content="Sen akıllı turizm ve turist rehberisin."
                      "Kullanıcılara Türkiyedeki şehirler, tarihi yerler, yöresel yemekler, ulaşım ve tatil önerileri hakkında güzel bilgiler ver")
    ] + st.session_state.memory.load_memory_variables([])["history"] + [
        HumanMessage(content=user_input)
    ]

    # modelden yanıt al
    response = llm(messages)

    # yanıtı hafızaya kaydet
    st.session_state.memory.chat_memory.add_ai_message(response.content)


# """
# isinstance(object, classinfo, /)
# Return True if the object argument is an instance of the classinfo argument, or of a (direct, indirect, or virtual) subclass thereof. If object is not an
# object of the given type, the function always returns False. If classinfo is a tuple of type objects (or recursively, other such tuples) or a Union Type 
# of multiple types, return True if object is an instance of any of the types. If classinfo is not a type or tuple of types and such tuples, a TypeError 
# exception is raised. TypeError may not be raised for an invalid type if an earlier check succeeds.
# """

# Sohbet geçmişini arayüzde gösterme:
# tüm mesajları sırasıyla gezdirip ekrana bastıralım
for msg in st.session_state.memory.chat_memory.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("👩🏼 Kullanıcı"):
            st.markdown(msg.content)
    else: # mesajı ai göndermişse
        with st.chat_message("🤖 Akıllı Rehber"):
            st.markdown(msg.content)
