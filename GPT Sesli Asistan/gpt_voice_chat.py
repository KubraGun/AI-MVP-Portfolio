"""
Problem tanımı: GPT ile Sesli Sohbet
    - Kullanıcının mikrofona konuşarak soru sorması
    - OpenAI Whisper modeli
    - Metnin GPT 3.5 Turbo ile analiz edilmesi
    - Security: Zararlı dil filtreleme

Kullanılan Teknolojiler: 
    - Ses kaydı
    - Ses → text: OpenAI whisper
    - Generation response: OpenAI gpt 3.5 Turbo
    - Logging module : Loglama
    - Re → Zararlı içerik filtreleme

Model tanıtımı
    • OpenAI Whisper
        - Çok dilli konuşma tanıma modeli -> 90 dan fazla 
        - Konuşmaları yazıya döker -> Toplantı notları için geliştirdiğim otomasyonda alternatif olarak kullanıp test et
                                       [NOTE]: SaaS tabanlı entegrasyon için OpenAI üzerinden Whisper API
        - Birden çok dili destekleri
        - Otomatik dil algılama
        - Whisper 1 tanımlama
        - OpenAI Whisper alternatifleri

    • GPT 3.5 Turbo

                                       
    [NOTE 2] -> Hem bu projeyi hem diğer ses tabanlı projeleri Entegre etmeden önce API test et
                → Performans: cevap süresi, gecikme, accuracy, CPU/GPU kullanımı
                → Ses kalitesi test et

    - Burada OpenAI server ları kullanılıyor. ama on-prem de çalıştırılabilir. bunun için openai whisper ı open
      source olarak paylaştı. ancak çok büyük bir model, bilgisayar kaldırmayabilir
      bunun için whisper light kullanacağız
        • hafif, hızlı ve offline
        • open source
        • özellikle düşük donanımlı sistemlerde ve local app 

        
Installation libraries
    pip install openai python-dotenv sounddevice scipy
"""  

# import libraries
from openai import OpenAI # openai api istemcisi sınıfını içeri aktarır
import sounddevice as sd # mic erişimi
from scipy.io.wavfile import write # ses kaydını wav dosyasına yazdırma
import os
import uuid # unique id
import re # filtering
from datetime import datetime # loglamada, 
from dotenv import load_dotenv
import logging

# log conf
now = datetime.now().strftime("%Y%m%d_%H%M%S") # for log file name
log_file = f"logs/konusma_{now}.log"
os.makedirs("logs", exist_ok=True)

# log format and level
# log level
#   DEBUG - development
#   INFO - development
#   WARNING - deoplyment 
#   ERROR - deployment
#   CRITICAL -deployment
logging.basicConfig(
    level = logging.INFO, # info ve sonraki level → info warning error critical 
    format = "%(asctime)s [%(levelname)s] %(message)s", # Standard format
    handlers = [
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler() # konsola yazdırma
    ]
)

logger = logging.getLogger(__name__) # logger obj

# .en load
load_dotenv()
client = OpenAI() # OpenAI istemcisi .env den key alır

DURATION = 5     # tek seferde kaç saniye kayıt
FS = 44100       # ses kaydı için frekans değeri


# filtering - rule-based
BANNED_WORDS = ["zararlı"] # filtrelenecek kelimeler yazıldı

def filter_bad_words(text):
    filtered_text = text
    for word in BANNED_WORDS:
        if re.search(rf"|b{word}\b", text, flags= re.IGNORECASE):
            logger.warning(f"Zararlı kelime tespiti: {word}")
        
        # *** ile değiştirilecek
        filtered_text = re.sub(rf"\b{word}\b", "***", filtered_text, flags=re.IGNORECASE)

    return filtered_text 

# test
# filter_bad_words("Merhaba, zararlı bir kelime var mı?")
# test was successfully



# get voice record and whisper conf, speech to text
def record_audio(filename="recorded.wav", duration=DURATION): # mic record
    logger.info("Mikrofonda ses kaydı başlatıldı.")
    recording = sd.rec(int(duration*FS), samplerate=FS, channels=1)
    sd.wait() # kayıt bitene kadar bekler
    write(filename, FS, recording)
    logger.info(f"Ses kaydı tamamlandı: {filename}")


def transcribe_with_whisper(audio_path): 
    """ wav file whisper ile metne dönüştürülür """
    logger.info("Whisper ile ses yazıya çevriliyor")
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model = "whisper-1",
            file = audio_file,
            language = "tr"
        )
    
    return transcript.text

def get_gpt_response(messages):
    logger.info("GPT yanıt üretiyor")
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    return response.choices[0].message.content 

# test
#print(get_gpt_response([{"role": "user", "content": "merhaba, yapay zeka nedir? bana anlat"}]))
# test başarılı. eksiği gpt den gelen mesajın loglanmaması


# gpt 3.5 conf - create lm




# run
if __name__ == "__main__":
    logger.info("--- --- GPT Sesli Chatbot Başladı --- ---")
    logger.info(f"Konuşma log dosyası: {log_file}")

    # mesaj geçmişini sistem mesajıyla başlat
    messages =[ 
        {
            "role": "system",
            "content": "Sen yardımsever bir sesli asistansın. Konuşmalara uygun cevap ver."
        }
    ]

   # while True:
    #     uid = str(uuid.uuid4()) # her kayıt için benzersiz kimlik oluşturur
    #     audio_file = f"record_{uid}.wav" # geçici dosya
    #     record_audio(audio_file, DURATION) # mikrofon kaydı yap
    #     question = transcribe_with_whisper(audio_file) # wav dosyasını metne çevir
    #     logger.info(f"Kullanıcı (raw): {question}")

    #     filtered_question  = filter_bad_words(question)
    #     if filtered_question != question: # filtreleme yapıldıysa
    #         logger.info(f"Kullanıcı (filtreli): {filtered_question}")
        
    #     if "çık" in filtered_question.lower():
    #         logger.info("Çıkış komutu algılandı, program kapatılıyor")
    #         break

    #     messages.append({"role":"user", "content": filtered_question}) # kullanıcı mesajını ekle
    #     answer = get_gpt_response(messages)
    #     logger.info(f"GPT: {answer}")

    #     os.remove(audio_file) # geçici wav dosyası silinir

    # logger.info("GPT Sesli sohbet bitti")


# TesT:
uid = str(uuid.uuid4()) # her kayıt için benzersiz kimlik oluşturur
audio_file = f"record_{uid}.wav" # geçici dosya
record_audio(audio_file, DURATION) # mikrofon kaydı yap
question = transcribe_with_whisper(audio_file) # wav dosyasını metne çevir
logger.info(f"Kullanıcı (raw): {question}")

filtered_question  = filter_bad_words(question)
if filtered_question != question: # filtreleme yapıldıysa
    logger.info(f"Kullanıcı (filtreli): {filtered_question}")
        
if "çık" in filtered_question.lower():
    logger.info("Çıkış komutu algılandı, program kapatılıyor")

messages.append({"role":"user", "content": filtered_question}) # kullanıcı mesajını ekle
answer = get_gpt_response(messages)
logger.info(f"GPT: {answer}")

os.remove(audio_file) # geçici wav dosyası silinir
logger.info("GPT Sesli sohbet bitti")