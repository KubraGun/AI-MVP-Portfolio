import streamlit as st
from langchain_community.chat_models import ChatOllama
from langchain.schema import SystemMessage, HumanMessage
from langchain.memory import ConversationBufferMemory

# streaming callbacks
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler # terminale yazmak
from langchain.callbacks.base import BaseCallbackHandler # streamlit ile çalışmak için özel handler. oluşturacağımız class ın base class ı olacak
from typing import Any

# streamlit için özel streaming callback tanımı
class StreamHandler(BaseCallbackHandler):
    def __init__(self, placeholder):
        self.placeholder = placeholder # streamlit içerisindeki mesaj kutusu
        self.final_text = ""
    
    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        self.final_text += token # token ları birleştir
        self.placeholder.markdown(self.final_text + " ") # canlı oalrak yaz.

st.set_page_config(page_title="Akıllı Turist Rehber (Canlı)", page_icon="🌍")
st.title("🌍 Akıllı Turist Rehberi (Streaming Mode)")
st.markdown("Türkiye'ni dört bir yanındaki turistik yerler hakkında bilgi almak için sorular sorabilirsiniz.")

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True) # Mesaj geçmişi

user_input = st.chat_input("Bir şehir, mekan, yemek ya da aktivite sorabilirsiniz...")

for msg in st.session_state.memory.chat_memory.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("👩🏼 Kullanıcı"):
            st.markdown(msg.content)
    else: # mesajı ai göndermişse
        with st.chat_message("🤖 Akıllı Rehber"):
            st.markdown(msg.content)

if user_input: 
    # eğer user input varsa yeni gelen kullanıcı mesajını ilk olarak memory ye ekleriz
    st.session_state.memory.chat_memory.add_user_message(user_input)
    with st.chat_message("👩🏼 Kullanıcı"):
        st.markdown(user_input)

    with st.chat_message("🤖 Akıllı Rehber"):
        response_placeholder = st.empty() # streamlit'te geçici mesaj kutusu
        stream_handler = StreamHandler(response_placeholder)

        llm = ChatOllama(model="llama3.2:3b", streaming = True, callbacks=[stream_handler]) # token geldikçe ekrana yazıdırlır vaziyette

    
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
