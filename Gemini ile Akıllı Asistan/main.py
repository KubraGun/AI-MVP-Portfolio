"""
Problem tanımı
    - Gemini ile Akıllı asistan projesi
    - Günlük hayatta notlar, planları unutmamak için dijital uygulamalar kullanıyor (notion, click up)
    - Ancak bu sistemler çoğunlukla rule-based çalışır, doğal dili anlamaz. (benim için bu etkinliği not al tarzı bir akıllı asistan)
    - Notlar, görevler ve etkinlikler için
    - Amaç: yapay zekâ kullanan akıllı asistan geliştirmek.
    - Kullanıcının doğal dilde verdiği komutları anlar. Yani chatbot. 
    - Bir db olacak ve bu db içerisinde daha önceden belirlenmiş olan notlar ve etkinlikler olacak. → en yakın etkinlik sorulduğunda asistan bunları geri döndürecek
    - Rule-based notlar ve etkinlikler oluşturulacak, chatbot ile erişilecek
    - Akıllı asistan ntolara ve etkinliklere erişerek özetleme, bilgi çıkarma, takvim oluşturma özelliklerini sunar.
    

Model Tanımı
    - Google Gemini → Developed by DeepMind
    - Gemini 2.0 Flash kullanılacak gemini-2.0-flash
   

API Tanımlama
    - Google -> Google Gemini API https://aistudio.google.com/api-keys çok sık değiştiriyorlar https://ai.google.dev/gemini-api/docs?hl=tr


Plan/Program
    - assistant: gemini chatbot oluştur
    - database: sqlite database oluştur. notlar ve etkinliklerin saklanması
    - main: bileşenleri bir araya getirir


installation libraries
    pip install requests python-dotenv

    pip freeze > requirements.txt

import libraries

"""

#assistant.py dosyasından gemini api yanıtını alan 
from assistant import get_gemini_response, detect_intent # gemini api yanıtını alır

# db için fonkları içeri aktar
from database import initialize_db, add_event, add_note, get_events, get_notes


# Initialize DB
initialize_db()

# Karşılama mesajı
print("Akıllı Asistana hoş geldiniz")
print("Komutlar: not ekle | etkinllik ekle | notları göster | etkinlikleri göster | sohbet et | çıkış")

# # Program
# Burası kullanıcı sadece belirli komutları girdiği zaman çalıştığı için rule-based olmuş oldu. Ancak bizim sistemimiz AI sistemi
# while True:
#     komut = input("Komut girin: ").strip().lower() # komutu al boşlukları kırp küçük harfe çevir

#     if komut == "not ekle":
#         content = input("Not içeriği nedir? ") # kullanıcıdan not içeriği
#         add_note(content)

#         print("-------------------------")
#         print("Not başarıyla kaydedildi")
#         print("-------------------------")

#     elif komut == "etkinlik ekle":
#         event = input("Etkinlik açıklaması?")
#         date = input("Etkinlik tarihi?")
#         add_event(event, date)
#         print("-----------------------------")
#         print("Etkinlik başarıyla kaydedildi")
#         print("-----------------------------")
    
#     elif komut == "notları göster":
#         notes = get_notes() # dbden tüm notları al
#         if notes:
#             print("-----------------")
#             print("Kaydedilen notlar")
#             print("-----------------")
#             for content, created_at in notes: # her notu ve tarihi yazdır
#                 print(f"- [{created_at}] {content}")
#         else:
#             print("---------------------------")
#             print("Henüz eklenmiş not yok") 
#             print("---------------------------")

#     elif komut == "etkinlikleri göster":
#         events = get_events()

#         if events:
#             print("----------------------")
#             print("Kaydedilen etkinlikler")
#             print("----------------------")
#             for event, event_date in events: # her notu ve tarihi yazdır
#                 print(f"- [{event_date}] {event}")
#         else:
#             print("---------------------------")
#             print("Henüz eklenmiş etkinlik yok") 
#             print("---------------------------")
    
#     elif komut == "sohbet et":
#         message = input("Kullanıcı: ").strip() # kullanıcıdan serbest metin al

#         if message == "not_ozet":
#             notes = get_notes() # notları db den al
#             if not notes:
#                 print("Özetlenecek not yok")
#                 continue

#             all_notes_text = "\n".join([f"- {note[0]}" for note in notes]) # tüm notları birleştir
#             prompt = f"Aşağıda bulunan notları özetler misin? \n\n {all_notes_text}"
#             # gemini den özet isteme
#             # prompt satırı yazılmak zorunda değil 

#             summary = get_gemini_response(prompt) 

#             print("Not Özeti: \n")
#             print(summary)
        
#         elif message == "etkinlik_ozet":
#             events = get_events() # etkinlikleri db den al
#             if not events:
#                 print("Henüze özetlenecek etkinlik bulunamadı")
#                 continue

#             all_events_text = "\n".join([f"- {e[1]} {e[0]}" for e in events]) # tüm notları birleştir
#             prompt = f"Aşağıdaki Takvim etkinliklerini özetler misin? \n\n{all_events_text}"
#             summary = get_gemini_response(prompt)
#             print("Etkinlik özeti: \n")
#             print(summary)
        
#         else:
#             reply = get_gemini_response(message)
#             print(f"Akıllı asistan: {reply}")

#     elif komut == "çıkış":
#         break

#     else:
#         print("Hatalı komut girdiniz")



# Kullanıcının istediğini not özeti mi istediğini, etkinlik özeti mi istediğini anlayan sistem:
while True:
    komut = input("Komut girin: ").strip().lower() # komutu al boşlukları kırp küçük harfe çevir
    #sohbet et
    # intent = detect_intent(message) # kullanıcının isteğini anlayacak - not özet mi etkinlik özet mi yoksa sohbet mi

    if komut == "not ekle":
        content = input("Not içeriği nedir? ") # kullanıcıdan not içeriği
        add_note(content)

        print("-------------------------")
        print("Not başarıyla kaydedildi")
        print("-------------------------")

    elif komut == "etkinlik ekle":
        event = input("Etkinlik açıklaması?")
        date = input("Etkinlik tarihi?")
        add_event(event, date)
        print("-----------------------------")
        print("Etkinlik başarıyla kaydedildi")
        print("-----------------------------")
    
    elif komut == "notları göster":
        notes = get_notes() # dbden tüm notları al
        if notes:
            print("-----------------")
            print("Kaydedilen notlar")
            print("-----------------")
            for content, created_at in notes: # her notu ve tarihi yazdır
                print(f"- [{created_at}] {content}")
        else:
            print("---------------------------")
            print("Henüz eklenmiş not yok") 
            print("---------------------------")

    elif komut == "etkinlikleri göster":
        events = get_events()

        if events:
            print("----------------------")
            print("Kaydedilen etkinlikler")
            print("----------------------")
            for event, event_date in events: # her notu ve tarihi yazdır
                print(f"- [{event_date}] {event}")
        else:
            print("---------------------------")
            print("Henüz eklenmiş etkinlik yok") 
            print("---------------------------")
    
    elif komut == "sohbet et":
        message = input("Kullanıcı: ").strip() # kullanıcıdan serbest metin al
        intent = detect_intent(message)

        if intent == "not_ozet":
            notes = get_notes() # notları db den al
            if not notes:
                print("Özetlenecek not yok")
                continue

            all_notes_text = "\n".join([f"- {note[0]}" for note in notes]) # tüm notları birleştir
            prompt = f"Aşağıda bulunan notları özetler misin? \n\n {all_notes_text}"
            # gemini den özet isteme
            # prompt satırı yazılmak zorunda değil 

            summary = get_gemini_response(prompt) 

            print("Not Özeti: \n")
            print(summary)
        
        elif intent == "etkinlik_ozet":
            events = get_events() # etkinlikleri db den al
            if not events:
                print("Henüze özetlenecek etkinlik bulunamadı")
                continue

            all_events_text = "\n".join([f"- {e[1]} {e[0]}" for e in events]) # tüm notları birleştir
            # prompt = f"Aşağıdaki Takvim etkinliklerini özetler misin? \n\n{all_events_text}" # filtreleme yaptığımızda
                                                                                             # örneğin sadece 2025 tekileri de sorduğumuzda prompt her etkinliği aldığı için filtreleme yapmaz
            prompt = f"Aşağıdaki takvim etkinliklerini kullanıcının isteğine göre özetler misin? Tarih giriş formatı yanlış olabilir (. ya da / kullanımı). tarihler gg/aa/yy şeklinde girilmiştir\n\n{all_events_text} Kullanıcı isteği: {message}"
            summary = get_gemini_response(prompt)
            print("Etkinlik özeti: \n")
            print(summary)
        
        else:
            reply = get_gemini_response(message)
            print(f"Akıllı asistan: {reply}")

    elif komut == "çıkış":
        break

    else:
        print("Hatalı komut girdiniz")