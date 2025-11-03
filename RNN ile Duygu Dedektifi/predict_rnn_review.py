# Kaydedilen modeli test edeceğiz
import numpy as np
import nltk 
from nltk.corpus import stopwords
from tensorflow.keras.models import load_model
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import text_to_word_sequence

# model parameters:
max_features = 10000 # eğitim sırasında kullanılan max kelime sayısı
maxlen = 500 # RNN modelinin beklediği sabit uzunluk → input_length

# stopwords kurtulma ve sözlükleri hazırlama
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

# imdb veri setinden kelime → index sözlüğü
word_index = imdb.get_word_index()

# sayı → kelime sözlüğü oluşturma
index_to_word = {index + 3: word for word, index in word_index.items()}
index_to_word[0] = "<PAD>"
index_to_word[1] = "<START>"
index_to_word[2] = "<UNK>"

# kelime → sayı için ters sözlük
word_to_index = {word: index for index,word in index_to_word.items()}

# load training model
model = load_model("rnn_duygu_model.h5")
print("Model başarıyla yüklendi.")


# predict fun:
def predict_review(text):
    """
        Kullanıcıdan gelen metni temizlenecek
        modele uygun hale getirilecek
        tahmin sonucu yazdırılacak
    """

    # yorumu küçük harfli kelime listesine çevirelim:
    words = text_to_word_sequence(text) # example: This movie is great → ["this", "movie", "is", "great"]

    # stopwords kaldırılır
    cleaned = [word.lower() for word in words if word.isalpha and word.lower() not in stop_words]

    # Her kelime eğitilen sözlükten sayıya çevrilir
    encoded = [word_to_index.get(word, 2) for word in cleaned] # 2 = <UNK>

    # padding: modelin beklediği sabit uzunluk ayarı
    padded = pad_sequences([encoded], maxlen=maxlen)

    # prediction → 0 - 1 arasında bir değer return edecek
    prediction = model.predict(padded)[0][0]

    print(f"Tahmin olasılığı pozitif: {prediction:.4f}")
    if prediction > 0.5:
        print("Pozitif")
    else:
        print("Negatif")

# Kullanıcı girişi konsol üzerinden alınsın
user_review = input("Bir film yorumu girin: ")
predict_review(user_review)
