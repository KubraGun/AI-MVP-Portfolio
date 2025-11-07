import os # ortamn değişkenleri ve dosya yolu
import requests # http istekleri için
from dotenv import load_dotenv #.env den env variable yüklemek için

# load .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# API control
if not api_key:
    raise ValueError("GEMINI_API_KEY .env dosyasında tanımlı değil")
# try catch, assert, raise

# 2 yol var 1. google impoert et
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# API call
headers = {
    "Content-Type": "application/json", # JSON formatında veri göndereceğimi belirttim
    "X-Goog-Api-Key": api_key, # yetkilendirme için api anahtarı
}

def get_gemini_response(prompt: str) -> str: # gemini apisine prompt gönderip yanıt redurn eden fonk
    # api'ye gönderilecek json yapısı
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt # kullanıcıdan gelen mesajı içeren bölüm → bu dict
                    }
                ]
            }
        ]
    }

    # gemini api yehttp post isteği gönderelim
    response = requests.post(url, headers=headers, json=payload)

    # istek başarılıysa → HTTP 200
    if response.status_code == 200:
        try:
            # gelen cevap ayıklanır
            result = response.json() # json formatındaki yanıt → dict

            return result["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            # eğer json yapısı beklenildiği gibi değilse hata döndürür
            return f"Yanıt hatası: {e}"
    
    else:
        return f"api hatası {response.status_code}: {response.text}"
    
def detect_intent(message):
    """ Kullanıcı mesajına göre istek sınıflandırır """
    # Gemini için özel görev promptu: mesajın hangi komut kategorisine ait olduğunu tespit eder
    prompt = f"""
                Kullanıcının aşağıdaki cümlesini sınıflandır:

                Etiketlerden sadece birini döndür:
                - not_ozet (eğer notlarını özetlemesini istiyorsa)
                - etkinlik_ozet (eğer etkinlikleri görmek ya da özet istiyorsa)
                - normal (diğer her şey)

                Cümle: "{message}"
                Yalnızca etiket döndür: (örnek: not_ozet)      
    """
    # promptu gemini ye gönder ve yanıt al
    response = get_gemini_response(prompt)

    return response.strip().lower()



if __name__ == "__main__":
    user_input = input("Kullanıcı sorusu: ") # Kullanıcıdan terminal üzerinde girdi almak için
    yanit = get_gemini_response(user_input) # gemini'den alınan yanıt return edilir
    print(f"Akıllı Asistan yanıtı: {yanit}")
