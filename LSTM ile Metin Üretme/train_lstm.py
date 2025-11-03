"""
Problem tanımı:
    - LSTM ile Metin Üretme 
    - Transformers ile metin üretimi yapılmaktadır. 
    - Dil modeli verilen başlangıç kelimelerden anlamlı ve doğal dil kurallarına uygun şekilde yeni cümleler oluşturmasıdır
        → ben yarın ...... (buradaki kelime tahmin edilir.)

LSTM:



Veri seti:
    - ChatGPT ile oluşturulmuş 100 adet günlük hayat cümlesi


Plan program:




install & import libraries
    requirements.txt → pip freeze > requirements.txt
"""
# import libraries
import numpy as np
import tensorflow as tf # LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Eğitim verisi chatGPT ile oluşturulacak 
# Not veri seti bulma yöntemi
#   1. Public olarak yayınlanmış veri setleri
#   2. Gerçek hayatta toplanan veri seti (probleme özgü)
#   3. Simülasyon verisi → bunu kullanacağız
"""
Context: LSTM tabanlı bir metin üretim modeli eğitiyorum. Bu yüzden gerçek hayata uygun, doğal, karmaşık, farklı bağlamlarda kullanılan çeşitli Türkçe cümlelere ihtiyacım var. Task: Türkçe konuşma dilinde kullanılan en az 50 ve en fazla 500 adet cümle oluştur. Cümleler: Günlük hayattan alınacak (ev, okul, iş, ulaşım, arkadaşlık, aile, alışveriş, duygular, şikayetler…) Kişiden kişiye değişebilen doğal dil varyasyonları içerecek Gerektiğinde argo, kısaltma, dolaylı anlatım, konuşma hatası barındırabilecek Duygu ve ton farklılıkları (mutlu, kızgın, şaşkın, endişeli vb.) içerecek Farklı uzunluklarda olacak (kısa, orta, uzun) Aynı şablonun tekrar eden kopyaları olmayacak Instruction: Çıktıyı yalnızca şu Python formatında ver: data = [ "cümle 1", "cümle 2", ... ] Başka hiçbir açıklama, numara, başlık ekleme. Clarify (Üretim Kuralları): Her cümle büyük harfle başlasın Noktalama hataları, günlük dilde makul olduğu sürece kabul Özel isim kullanacaksan anonimize et (Ayşe yerine “arkadaşım” gibi) Tekrar eden anlam veya yapı tespit edersen kendin düzelt Refine: Veri setini oluşturmadan önce: “Hazırım: Kaç cümle üreteyim?” diye sor. Ben sayı verdiğimde üretime başla.
"""
data = [
    "Sabah alarmı duymadım, işe yine geç kaldım.",
    "Otobüs tam önümden kaçtı, sinir oldum.",
    "Kahve makinesi yine bozulmuş, kimse ilgilenmemiş.",
    "Bugün hava bir garip, ne sıcak ne soğuk.",
    "Arkadaşım aradı, dışarı çıkalım mı dedi ama hiç halim yok.",
    "Annem sürekli evi topla diyor, halbuki zaten topluyorum.",
    "Marketin önünde o kadar sıra vardı ki vazgeçtim.",
    "Ders çalışmak istiyorum ama konsantre olamıyorum.",
    "Akşam ne yesem diye bir saat düşündüm, yine makarna yaptım.",
    "Şu müziği duyunca çocukluğum aklıma geldi.",
    "Telefonumun şarjı hep en lazım olduğunda bitiyor.",
    "Bugün herkes bana ters yaptı, anlamıyorum.",
    "Yeni ayakkabılarımı giydim ama ayağımı vurdu.",
    "Ofiste herkes sessiz, garip bir hava var.",
    "Dün gece çok garip bir rüya gördüm, hâlâ etkisindeyim.",
    "Otobüste yer buldum diye sevinirken yaşlı amca geldi, hemen kalktım.",
    "Kedim sabah beşte mırlamaya başladı, uykum kaçtı.",
    "Sabah kahvaltıda çay döküldü, masa battı.",
    "Okulda sınav vardı ama kimse düzgün hazırlanmamış.",
    "Yeni gelen stajyer çok heyecanlıydı, biz de gülmemek için zor tuttuk.",
    "Yine yağmur yağdı, çamaşırlar mahvoldu.",
    "Bir mesaj attı ama ne demek istediğini çözemedim.",
    "Sabah kahvemi içmeden konuşmamam gerektiğini artık herkes biliyor.",
    "Bugün yolda eski bir arkadaşla karşılaştım, yıllar olmuş.",
    "İnternette bir şey ararken başka şeylere daldım yine.",
    "Bu trafiğe alışamayacağım galiba.",
    "Kargo bekliyorum, üç gündür yolda yazıyor.",
    "Gece dizi izlerken bir baktım sabah olmuş.",
    "Komşu yine yüksek sesle müzik açmış, delireceğim.",
    "Bütün gün temizlik yaptım ama hâlâ bitmedi.",
    "Bir kahve içelim dedik, üç saat oturduk.",
    "Dün toplantı uzadı, eve geç kaldım.",
    "Telefonu elime alıyorum, ne yapacağımı unutuyorum.",
    "Yeni saçımı kimse fark etmedi, moralim bozuldu.",
    "Bugün pazara gittim, fiyatlar uçmuş resmen.",
    "Akşam yemeğini yakmadan pişirdiğim için kendimle gurur duydum.",
    "Bir mail geldi, ama o kadar karmaşık ki anlamadım.",
    "Otobüste yer bulamayınca yarım saat ayakta kaldım.",
    "Birden rüzgar çıktı, saçlarım darmadağın oldu.",
    "Gece telefon elimde uyuyakalmışım yine.",
    "Arkadaş grubunda biri alındı, ortam buz kesti.",
    "Sabah yürüyüşüne çıktım, hava mis gibiydi.",
    "İş yerinde kahkaha attım, herkes bana baktı.",
    "Ders anlatırken biri esnedi, moralim bozuldu.",
    "Bugün çok üretken hissettim kendimi.",
    "Yeni tarif denedim ama sonuç facia oldu.",
    "Bir an sustum, herkes bana bakıyordu.",
    "Kütüphanede sessizlik o kadar güzeldi ki çıkmak istemedim.",
    "Kahve döküldü, bilgisayarın üstüne geldi neredeyse.",
    "Sabah spora gidecektim ama alarmı erteledim, tabii ki gitmedim.",
    "Bugün her şey tam istediğim gibi gitti, keyfim yerinde.",
    "Sabah yağmur yağdı ama ben tam zamanında işe yetiştim.",
    "Yeni aldığım kulaklık harika, ses kalitesi müthiş.",
    "Kargom beklediğimden erken geldi, şaşırdım doğrusu.",
    "Akşam yemeğini dışarıda yedik, ortam çok güzeldi.",
    "Bugün enerjim yüksek, her işe yetişiyorum.",
    "Uzun zamandır aradığım kitabı sonunda buldum.",
    "Arkadaşımın sürpriz doğum günü partisi efsane oldu.",
    "Hafta sonu tatile çıkıyoruz, çok heyecanlıyım.",
    "Kedim sabah yanıma gelip mırıldandı, o kadar tatlı ki.",
    "Sabah spor yaptım, kendimi çok dinç hissediyorum.",
    "Bütün gün işlerimi bitirdim, sonunda içim rahatladı.",
    "Yeni dizime başladım, bayıldım konusu çok sürükleyici.",
    "Bugün mutfağı baştan aşağı temizledim, parlıyor resmen.",
    "Yürüyüşe çıktım, hava mis gibi kokuyordu.",
    "Patron toplantıda beni övdü, moralim yerine geldi.",
    "Kardeşim sınavdan yüksek not almış, çok gururlandım.",
    "Yeni tarif denedim, beklediğimden güzel oldu.",
    "Markette indirim vardı, bayağı karlı çıktım.",
    "Güneşli bir gün olunca modum hemen değişiyor.",
    "Sabah otobüs hemen geldi, bu sefer şanslıydım.",
    "Bugün kimseyle tartışmadan günü bitirdim, zafer gibi.",
    "Evin camlarını sildim, dışarısı kristal gibi görünüyor.",
    "Uzun zamandır görmediğim bir arkadaşımla denk geldim, çok mutlu oldum.",
    "Çiçeklerim nihayet açtı, emeklerim boşa gitmedi.",
    "Telefonumda yer açtım, artık kasmıyor.",
    "Bugün hiçbir şey planlamadım ama her şey kendiliğinden güzel gitti.",
    "Kahvemi tam sevdiğim kıvamda yaptım, keyifli başladım güne.",
    "Yeni kıyafetimi giydim, herkes beğendi.",
    "Toplantı kısa sürdü, kimse sıkılmadı.",
    "Evde sessizlik var, kitap okumak için mükemmel zaman.",
    "Kütüphanede yeni kaynaklar buldum, araştırmam hızlandı.",
    "Bugün kendime vakit ayırdım, çok iyi geldi.",
    "Birden yağmur yağdı ama ben şemsiyemi almıştım, denk geldi.",
    "Arkadaş grubumuzla kahkahaya boğulduk, stresim gitti.",
    "İş yerinde yeni proje bana verildi, güvenmeleri hoşuma gitti.",
    "Sabah güneş doğarken balkonda çay içtim, huzur doluydu.",
    "Bugün hiçbir aksilik çıkmadı, nadir bir gün resmen.",
    "Komşum tatlı getirdi, tam da canım çekiyordu.",
    "Yeni saç modelimi herkes beğendi, moralim tavan.",
    "Ders sunumum çok iyi geçti, öğretmenim teşekkür etti.",
    "Bugün resmen şans benden yanaydı.",
    "Kardeşimle uzun zamandır ilk kez kavga etmedik.",
    "Evde film gecesi yaptık, çok keyifliydi.",
    "Uzun süredir ilk kez erken uyandım ve harika hissettim.",
    "Kütüphanede tam aradığım makaleyi buldum, inanamadım.",
    "Birine yardım ettim, yüzündeki gülümseme çok güzeldi.",
    "Bugün kendimi motive hissettim, yapılacaklar listemi tamamladım.",
    "Günün sonunda yorgunum ama mutluyum, buna değerdi.",
    "Her şey istediğim gibi gitmedi ama yine de güzel bir gündü."
]
# [TODO] → spor siyaset sanat tarih olmak üzere 1000 tane kelime ürettir. bunun için agent kullanıp her alanla ilgili güncel olacak şekilde
# eşit oranda dağılıma sahip sentetik cümleler ürettir


# ----- PREPROCESSING -------
# Tokenizer (kelimeler indexlere çevrilir )
tokenizer = Tokenizer() # standart kullanım. [NOTE] → LR notlarımda bütün tokenization teknikleri var
tokenizer.fit_on_texts(data) # fit_on_texts() input: oluşturulan metinler 
total_words = len(tokenizer.word_index) + 1 # padding işleminden dolayı +1 yaptık

print(f"total_words: {total_words}")
# output: 454 → unique word


# Embedding
# n-gram diziler oluşturulacak (embedding) → kelimeler sayısal vektörlere dönüştürülür.
input_sequences = []
for text in data:
    token_list = tokenizer.texts_to_sequences([text])[0]
    for i in range(1, len(token_list)):
        n_gram_sequences = token_list[: i+1] # token list in i+1 e kadar olan kısmı
        input_sequences.append(n_gram_sequences)


print(f"Input sequences: \n{input_sequences}")

"""
[5, 53], [5, 53, 105], [5, 53, 105, 29], [5, 53, 105, 29, 8], [5, 53, 105, 29, 8, 54], [5, 53, 105, 29, 8, 54, 30]
"Sabah alarmı duymadım, işe   yine   geç   kaldım."
   5     53     105      29     8     54     38
"""

# Padding → NLP'de NN kullanıyorsak padding kullanmak önemli!! Farklı uzunluktaki diziler sabitlenir.
max_sequence_length = max(len(x) for x in input_sequences) # bu çalışmada maxlen dizinin içindeki maksimum uzunluğa sahip eleman olsun
input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_length, padding="pre")
print(f"After padding input_sqequences: \n{input_sequences}")
"""
[OUTPUT]
After padding input_sqequences:
[[  0   0   0 ...   0   5  53]
 [  0   0   0 ...   5  53 105]
 [  0   0   0 ...  53 105  29]
 ...
 [  0   0  26 ...   8  67  52]
 [  0  26  13 ...  67  52   1]
 [ 26  13  87 ...  52   1 453]]
"""


# input ve target ayırımı
X = input_sequences[:, :-1] # n - 1 kelime giriş olarak seçilir.
y = input_sequences[:, -1] #n. kelimeyi tahmin et
"""
[  0   0   0 ...   0   5  53  105]
X = [  0   0   0 ...   5  53]
y = [105]
"""


# one hot encoding to target variable
y = tf.keras.utils.to_categorical(y, num_classes=total_words)
print(f"hede değişken: {y}")


# ------- LSTM Training ---------
# LSTM model

# girdi katmanında embedding katmanı olacak, sonra lstm layer son olarak çıkış katmanı dense layer ile kurulum tamamlanacak
model = Sequential() 
model.add(Embedding(total_words, 50, input_length=X.shape[1])) # embedding katmanı
model.add(LSTM(100))
model.add(Dense(total_words, activation = "softmax")) # multiclass classification → softmax

# compile
model.compile(optimizer = "adam", loss= "categorical_crossentropy", metrics = ["accuracy"]) # optimizer → adaptive momentum
print(model.summary()) # https://stackoverflow.com/questions/68083287/why-does-keras-model-summary-not-work-for-my-model


# eğitimi başlat
model.fit(X, y, epochs=100, verbose=1)


# Test
def generate_text(seed_text, next_words):
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0] # tokenization
        token_list = pad_sequences([token_list], maxlen=max_sequence_length - 1, padding="pre") # padding
        predicted_probs = model.predict(token_list, verbose=0)
        predicted_index = np.argmax(predicted_probs, axis=-1)[0]
        predicted_word = tokenizer.index_word[predicted_index]
        seed_text = seed_text + " " + predicted_word# seed text tahmin edilen kelime eklenerek güncellendi
    return seed_text

#print(generate_text("Bu sabah", 2)) # Bu sabahtan sonra 2 tane kelime üretsin
print(generate_text("Bugün", 5))
# modeli kaydetmedim
"""
(1)
seed_text = bu sabah
predicted_word = okula

(2)
seed_text = bu sabah okula
predicted_word = geç

(return)
seed_text = bus abah okula geç
"""