"""
Vector Database Builder



    Faiss is library for efficient similarity searcch and clustering of dense vectors
"""

import os
import fitz # for pdf
from sentence_transformers import SentenceTransformer # for embedding
import faiss
import numpy as np
import pickle


# load .pdf file
# pdf → text
def extract_text_from_pdf(pdf_path):
    """
        extracting text from pdf file
    """
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    
    return text

# print(extract_text_from_pdf(".\data\sample_contract_novalux.pdf"))

# chunking
# uzun metni daha küçük parçalara ayıracak:
# Genelde hiyerarşik yapılara göre bölünür
# bölünenlerin arasındaki bağlamsal ilişki hesaplanıp yine chunking yapılır
def chunk_text(text, max_length=500):
    """ Belirtilen karakter uzunluğuna göre böl """
    chunks = [
        
    ]
    current = ""
    for line in text.split("\n"):
        if len(current) + len(line) < max_length:
            current += " " + line.strip()
        else:
            chunks.append(current.strip())
            current = line.strip()
        
    if current: 
        chunks.append(current.strip())
    
    return chunks

# # TEST
# text_dummy = extract_text_from_pdf(".\data\sample_contract_novalux.pdf")
# print(chunk_text(text_dummy, max_length=500))

# embedding with sentence tranformer → huggingface embedding models (search google)
# en çok kullanıla (huggingface e göre) all-MiniLM-L6-v2
model  = SentenceTransformer("all-MiniLM-L6-v2") # pretrained

# pdf path
pdf_file_path = ".\data\sample_contract_novalux.pdf"

text = extract_text_from_pdf(pdf_file_path)

chunks = chunk_text(text, max_length=500)

# her chunk için emb. vec
embeddings = model.encode(chunks, convert_to_tensor=True)


print(f"embeddings shape: {embeddings.shape}")
# faiss index
dimension = embeddings.shape[1] # embedding dimension
index = faiss.IndexFlatL2(dimension) # similarity with Euclidean distance 

# index.add(np.array(embeddings)) # embeddingler index e eklendi
# Yukarıdaki satır çalışmadı. Sebebi pytorch un gpu da çalışması olabilir (sentencetransformer pytorch kullanır)
# Control 1
import torch

# print("CUDA available:", torch.cuda.is_available())
# if torch.cuda.is_available():
#     print("GPU name:", torch.cuda.get_device_name(0))
#     print("Number of GPUs:", torch.cuda.device_count())
# else:
#     print("GPU kullanılmıyor.")
# CUDA available: False
# GPU kullanılmıyor.

# Control 2
# device = "cuda" if torch.cuda.is_available() else "cpu"
# print(f"Model şu anda {device.upper()} üzerinde.")

# # Modelin içeri taşındığını garantiye almak için:
# model = model.to(device)
# # output: Model şu anda CPU üzerinde.
# encode metodu pytorch tensor return eder
# çalışmama sebebi numpy 2.0'da np.array(tensor) (tensor → numpy array) copy ve dtype parametrelerini zorunlu hale getirmiş
index.add(embeddings.cpu().numpy())

# faiss index i ve chunkları kaydet
faiss.write_index(index, "data/contract_index.faiss")

with open("data/contract_chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print("[INFO] Faiss index ve chunklar kaydedildi")