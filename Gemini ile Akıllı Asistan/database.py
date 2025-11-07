import sqlite3 
import os

# db dosya yolunu oluşturma → data/assistant.db
DB_PATH = os.path.join("data", "assistant.db")

# db initializer
def initialize_db():
    # eğer data klasörü yoksa oluştursun
    os.makedirs("data", exist_ok=True)

    # veritabanına bağlanılacak. assistant.db yoksa oluşturulacak
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # TABLES:
    #       NOTES
    #       EVENTS
     
    # eğer not tablosu yoksa oluştur
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS notes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,             -- otomatik artan birincil anahtar
                        content TEXT NOT NULL,                            -- not içeriği     
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP    -- varsayılan şu anki zaman
                   )
                   """)
    
    # eğer etkinlik tablosu yoksa oluştur
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS calendar (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,             -- oto. art. bir. key
                        event TEXT NOT NULL,                              -- etkinlik açıklaması
                        event_date TEXT NOT NULL                          -- etkinlik tarihi                       
                   )
                 """)

    # değişiklikleri kaydet
    conn.commit()

    # bağlantıyı sonlandır
    conn.close()


# db ye yeni not ekleme işlemi
def add_note(content):
    # db bağlan
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # contenti not tablosuna ekle
    cursor.execute("INSERT INTO notes (content) VALUES (?)", (content,))

    # save changes
    conn.commit()

    # bağlantıyı kapat
    conn.close()

# db ye yeni etkinlik ekleme
def add_event(event, event_date):
    # db connection
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # etkinlik ve tarih bilgilerini calender a ekle
    cursor.execute("INSERT INTO calendar (event, event_date) VALUES (?, ?)", (event, event_date))

    # save changes
    conn.commit()

    # db close
    conn.close()

# Gemini'nin notlara ve eventlere erişmesini sağlayan func    
def get_notes():
    """ DB'den tüm notları sıralı bir şekilde getirir"""

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    # notes tablosundan içerik ve tarih bilgilerini zaman sırasına göre getir
    cursor.execute("SELECT content, created_at FROM notes ORDER BY created_at DESC")

    # sonuçları liste olarak alalım
    notes = cursor.fetchall()

    conn.close()

    return notes
    
def get_events():
    """Tüm etkinlikleri db den sıralı şekilde getiren func"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # calender tablosundan etkinlikleri tarihe göre sırala getir.
    cursor.execute("SELECT event, event_date FROM calendar ORDER BY event_date")

    # Sonuçları al
    events = cursor.fetchall()


    conn.close()


    return events

if __name__ == "__main__":
    initialize_db()
    add_note("eve dönerken su almayı unutma")
    add_event("toplantı var", "15.12.2027")

    print(f"Notes: {get_notes()}")
    print(f"Events: {get_events()}")



# sqlite en basit veri tabanlarından birisidir. Genelde preoje geliştirilirken sqlite ile geliştirme yapılıp sonrasında
# PostgreSQL, SQL, vs hangisi kullanılacaksa o entegre edilir.


