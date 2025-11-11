"""
Problem tanımı:
    - Sözleşmeler uzun ve teknik bilgi içeren belgelerdir.
    - Kullanıcının yüklediği bir sözleşme dosyasından içerik çıkarmak
    - Bu içerikği vekörel olarak temsil edilecek
    - Vector DB: FAISS → hızlı arama
    - User query → Fetch data from DB → Response (gpt-3.5)

    
Kullanılan teknolojiler
    - embedding
    - faiss
    - gpt 3.5

    
RAG
    - özellikle devlet kurumlarında kurum içi belgelerin gizliliği ve çalışanlara kolaylık için kullanılır
    - LM'lere b,lg, desteği sağlayan bir teknik
    - retrieval: Kullanıcı sorusu embedding e dönüştürülür. faiss üzerinden en alakalı içerik (chunk) getirlir.
    - augmentation: zenginleştirmebulunan chunklar llm in anlaabileceği bir formata dönüştürülüyor
    - generation: lm mantıklı yanıt üretir
    

Plan
    - gpt ile sözleşme belgesi hazırlama
    - metin çıkarma ve parçalama
    - embedding ve faiss ile vector db oluşturma
    - soru cevap sistemi

installation libraries
    pip install openai python-dotenv sentence-transformers faiss-cpu numpy PyMuPDF
"""
import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key) 

model = SentenceTransformer("all-MiniLM-L6-v2")

# load faiss index 
index = faiss.read_index(".\data\contract_index.faiss")

# load chunked text data
with open("data/contract_chunks.pkl", "rb") as f:
    chunks =  pickle.load(f)

# user
while True:
    question = input("\n Sorunuzu girin: (EN)")

    # çıkmak için döngüyü sonlandır
    if question.lower() in ["exit", "quit", "q"]:
        print("Çıkış yapılıyor...")
        break
    # kullanıcı sorularını vektöre çevir
    question_embedding = model.encode([question])

    # faiss ten en yakın 3 chunk ı ara
    k = 3 # ne kadar çok maliyet o kadar fazla, ne kadar az bilgiyi o kadar kaçırma
    # distances, indices = index.search(np.array(question_embedding), k)
    #distances, indices = index.search(question_embedding.cpu().numpy(), k)
    distances, indices = index.search(np.array(question_embedding), k)


    retrieved_chunks = [chunks[i] for i in indices[0]]
    context = "\n -------------- \n".join(retrieved_chunks)

    # llm e gönderen sistem prompt
    prompt = f"""
                You are a contract lawyer assistant. Based on the contract context below,
                answer the user's question clearly.

                Context:
                {context}

                Question:
                {question}

                Answer:
"""
    
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages= [
            {"role": "user", "content": prompt}
        ],
        temperature=0.2, # düşük halüsinasyon için
    )

    print("AI Assistant: \n", response.choices[0].message.content.strip())



# NOT!!
# Embedding tip dönüşümü (PyTorch → NumPy) ve faiss CPU/GPU senkronizayonunun yönetimi sıkıntılı
# deployment-level roustness eksik

# GPU Troubleshooting Notes
# -------------------------
# - SentenceTransformer otomatik olarak CUDA destekler.
# - FAISS’in GPU sürümü farklıdır (faiss-gpu). CPU sürümü yüklüyse, embedding GPU’da olsa bile index işlemleri CPU’da yapılır.
# - Eğer FAISS GPU kullanılacaksa:
#     1. pip uninstall faiss-cpu
#     2. pip install faiss-gpu
#     3. index_gpu = faiss.index_cpu_to_gpu(res, 0, index)
# - PyTorch tensörleri FAISS’e direkt verilmez, her zaman .cpu().numpy() yapılmalıdır.
# - Embedding tipi bilinmiyorsa to_numpy() fonksiyonu kullanılmalıdır.
# - Büyük veri setlerinde FAISS index'i RAM’e yüklenmeden önce disk tabanlı olarak kaydedilebilir (.faiss dosyası).
