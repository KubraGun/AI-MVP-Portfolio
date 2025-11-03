"""
RNN ile Duygu Dedektifi (Sentiment analysis with RNN)
Problem tanımı:
    Bir yorum olumlu mu olumsuz mu olduğunu anlamak. Özellikle e-ticaret sitelerinde
        IMDB film yorumları veri seti ile bir metnin duygusal analizi gerçekleştirilecek
            - this movie is awesome → pozitif
            - it was terrible movie → negatif

RNN - Recurrent Neural Network
    Sıralı veriler üzerinde çalışan ANN (Artificial Neural Network)
    Metin, zaman serisi, ses gibi sıralamanın önemli olduğu verilerde önceki bilgileri hatırlayarak sonraki tahmin edilir.
        Girdi: film → çok → kötüydü 
        Bellek:
        Çıktı: anlam anlam olumsuz



Veri Seti
    IMDB veri seti: film yorumları içeren veri seti. 2 sınıf var.
                    50000 adet
                    0 negatif, 1 pozitif


Plan/program


Gerekli kurulumlar


import Libraries


"""

# import libraries
import numpy as np
import nltk
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from tensorflow.keras.models import Sequential # Sequential
from tensorflow.keras.layers import Embedding, SimpleRNN, Dense
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences


# Stop words belirle
nltk.download("stopwords") # İngilizce stopwords 
stop_words = set(stopwords.words("english")) # küçük ve anlamsız kelimeler ayıklanır


# model parameters
max_features = 10000 # en sık geçen 10000 kelime kullanılacak
maxlen = 500

# load data
(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=max_features)
# keras içinden gelen veri seti train test ayılmış olarak gelir. bu yüzden load_data
# return değeri 2 tuple'dır. İlk tuple → eğitim, ikinci tuple → test

# reiview sample data 
original_word_index = imdb.get_word_index()
# tokenlar halinde zaten. ancak bizim inceleyebilmemiz için token → text yapmamız gerek
inv_word_index = {index + 3: word for word, index in original_word_index.items()}
inv_word_index[0] = "<PAD>" # 0: boşluk padding
inv_word_index[1] = "<START>" # 1: cümle başlangıcı
inv_word_index[2] = "<UNK>" # 2: bilinmeyen kelime
# ÖRNEK: inv_word_index[3] → great: 65

def decoder_review(encoded_review):
    return " ".join([inv_word_index.get(i, "?") for i in encoded_review])



movie_index = 0
#first trainig data 
print("İlk yorum: (sayı dizisi)")
print(X_train[movie_index])
"""
İlk yorum: (sayı dizisi)
[1, 14, 22, 16, 43, 530, 973, 1622, 1385, 65, 458, 4468, 66, 3941, 4, 173, 36, 256, 5, 25, 100, 43, 838, 112, 50, 670, 2, 9, 35, 480, 284, 5, 150, 4, 172, 112, 167, 2, 336, 385, 39, 4, 172, 4536, 1111, 17, 546, 38, 13, 447, 4, 192, 50, 16, 6, 147, 2025, 19, 14, 22, 4, 1920, 4613, 469, 4, 22, 71, 87, 12, 16, 43, 530, 38, 76, 15, 13, 1247, 4, 22, 17, 515, 17, 12, 16, 626, 18, 2, 5, 62, 386, 12, 8, 316, 8, 106, 5, 4, 2223, 5244, 16, 480, 66, 3785, 33, 4, 130, 12, 
16, 38, 619, 5, 25, 124, 51, 36, 135, 48, 25, 1415, 33, 6, 22, 12, 215, 28, 77, 52, 5, 14, 407, 16, 82, 2, 8, 4, 107, 117, 5952, 15, 256, 4, 2, 7, 3766, 5, 723, 36, 71, 43, 530, 476, 26, 400, 317, 46, 7, 4, 2, 1029, 13, 104, 88, 4, 381, 15, 297, 98, 32, 2071, 56, 26, 141, 6, 194, 7486, 18, 4, 226, 22, 21, 134, 476, 26, 480, 5, 144, 30, 5535, 18, 51, 36, 28, 224, 92, 25, 104, 4, 2
"""


print("İlk yorum: (decoded)")
print(decoder_review(X_train[movie_index]))
"""
İlk yorum: (decoded)
<START> this film was just brilliant casting location scenery story direction everyone's really suited the part they played and you could just imagine being there robert <UNK> is an amazing actor and now the same being director <UNK> father came from the same scottish island as 
myself so i loved the fact there was a real connection with this film the witty remarks throughout the film were great it was just brilliant so much that i bought the film as soon as it 
was released for <UNK> and would recommend it to everyone to watch and the fly fishing was amazing really cried at the end it was so sad and you know what they say if you cry at a film it must have been good and this definitely was also <UNK> to the two little boy's that played 
the <UNK> of norman and paul they were just brilliant children are often left out of the <UNK> list i think because the stars that play them all grown up are such a big profile for the whole film but these children are amazing and should be praised for what they have done don't 
you think the whole story was so lovely because it was true and was someone's life after all 
that was shared with us all
"""

print(f"Label: {'Pozitif' if y_train[movie_index] == 1 else 'Negatif'}")
# [OUTPUT] Label: Pozitif


# gerekli sözlüklerin oluşturulması: word to index ve index to word
word_index = imdb.get_word_index()
index_to_word = {index + 3: word for word, index in word_index.items()} # sayılardan kelimelere geçiş
index_to_word[0] = "<PAD>" # 0: boşluk padding
index_to_word[1] = "<START>" # 1: cümle başlangıcı
index_to_word[2] = "<UNK>" # 2: bilinmeyen kelime

index_to_word[0] = "<PAD>" # 0: boşluk padding
index_to_word[1] = "<START>" # 1: cümle başlangıcı
index_to_word[2] = "<UNK>" # 2: bilinmeyen kelime

word_to_index = {word: index for index, word in index_to_word.items()} 



# data preprocessing 
def preprocess_review(encoded_review):
    # Sayı → text
    words = [index_to_word.get(i, "") for i in encoded_review if i>=3]

    # sadece harflerden oluşan ve stopword'den olmayanları al
    cleaned = [
        word.lower() for word in words if word.isalpha() and word.lower() not in stop_words
    ]

    # tekrardan temizlenmiş metni sayılara çevir
    return [word_to_index.get(word, 2) for word in cleaned]


# buraya kadar olanı test et

# veriyi temizle ve sabit uzunluğu par et
X_train = [preprocess_review(review) for review in X_train]
X_test = [preprocess_review(review) for review in X_test]

# pad sequence
X_train = pad_sequences(X_train, maxlen = maxlen)
X_test = pad_sequences(X_test, maxlen=maxlen)
# Bu işlemin mantığı:
# Elimizde 2 cümle olsun
# 1. merhaba bugün hava çok güzel
# 2.merhaba, naber
# Bu cümleleri RNN'e verirken input dimension olacak ancak RNN sabit uzunlukta inputlar bekler. 
# Bizim cümlelerimiz sabit uzunlukta değil. Padding işlemiyle max olarak belirlediğimiz sayıda 
# cümlelerin geri kalanı tamamlanır. yani bu örnekte maxlen=5 dersek 2. cümle 2 kelimeden 
# oluştuğu için yanına 3 tane 0 alır. ama maxlen 5 iken cümle 8 cümle olsaydı onu da bir sonraki padding e 
# kalan 3 kelimeyi gönderecekti
 

# RNN modeli oluşturma
model = Sequential() # Base model: katmanları sıralı olarak eklemek için

# embedding layer: kelime indexlerini 32 boyutlu bir vektöre dönüştürür
model.add((Embedding(input_dim=max_features, output_dim=32, input_length=maxlen)))

# Simple RNN Layer: metni sırayla işler ve bağlam ilişkisini öğrenir
model.add(SimpleRNN(units=32)) # cell (neuron) sayısı

# output katmanı: binary classification - sigmodi func. 1 tane nöron yeterlidir
model.add(Dense(1, activation="sigmoid"))


# model compile
# optimizerler ağırlık güncellemeri için önemlidir
# binary classification için loss func → binary cross entropy
# Evaluation metric: accuracy
model.compile(
    optimizer = "adam",
    loss = "binary_crossentropy",
    metrics = ["accuracy"]
)

print(model.summary())


# Training
history = model.fit(
    X_train, y_train, #girdi ve çıktı
    epochs = 2, # tüm veri ile yapılacak eğitimin sayısı
    batch_size = 64, # eğitim sırasında aynı anda işlenecek örnek sayısı → büyük verilerde gereklidir
    validation_split = 0.2 
)


# Evaluation
def plot_history(hist):
    # loss ve accuracy grafikleri
    plt.figure(figsize=(12, 4))

    # accuracy
    plt.subplot(1, 2, 1)
    plt.plot(hist.history["accuracy"], label = "Training")
    plt.plot(hist.history["val_accuracy"], label = "Validation")
    plt.title("Accuracy")
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")
    plt.legend() # etiketleri görünür hale getirir


    # Loss
    plt.subplot(1, 2, 2) # 1 satır 2 sütunluda 2.
    plt.plot(hist.history["loss"], label = "Training")
    plt.plot(hist.history["val_loss"], label = "Validation")
    plt.title("Loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend() # etiketleri görünür hale getirir

    plt.tight_layout()
    plt.show()

plot_history(history)

# Evaluation with test data
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f"Test: {test_acc:.2f}")

# eğitilen modelin kaydı
model.save("rnn_duygu_model.h5")
print(f"Model başarıyla kaydedildi: rnn_duygu_model.h5")