## client kullanımı
ask_question.py dosyasında ve genel eğitimlerde kullanılan response şablonu production-safe değil. [ÖDEV] hata bloğu ve logging ile kullan. RAG pipelineına kolayca entegre edebileceğim wrapper class oluştur. async+concurrecy management. (GPT için):

```python
response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[{"role": "user", "content": "Merhaba"}],
    temperature=0.7
)
print(response.choices[0].message["content"])

```
Böylece hızlı, tekseferde herhangi bir kontrol mekanizması olmadan cevap alınır
- Hata kontrolü yok
- Logging yok
- Rate limiting ve timeout management yok
- retry mechanism yok
- ve en önemlisi güvenli değil

Sistem düzeyinde böyle kullanmıyoruz. Katmanlara ayırırız:
### Wrapper/Client Abstraction
- API çağrısı direkt yapılmaz
- ChatClient sınıfı yazarız
```python
class ChatClientWrapper:
    def __init__(self, client):
        self.client = client
    
    def generate(self, messages, model="gpt-5-mini", temperature=0.7):
        try:
            response = self.client.chat.completions.create(
                model = model,
                messages = messages,
                temperature = temperature,
                timeout = 10 # production için ekleriz
            )
            return response.choices[0].message["content"]
```

### Logging ve Monitoring
- her aşama, çağrı loglrız; latency, hata kayıt altına alırız
- ops ekibi sorun olduğunda kolayca trace eder
```python
import logging

logging.basicConfig(filename="chat_api.log", level=logging.INFO)

result = chat_client.generate([{"role": "user", "content": "Merhaba"}])
logging.info(f"Prompt: Merhaba | Response: {result}")
```
### Rate limiting ve concurrency
- sistemlerde aynı anda çok çok istek gelir. bu yüzden API rate limitleri göz önüne alırız
- async ve queue based yapılar kurulur
```python
import asyncio

async def call_chat(prompt):
    return await chat_client.generate_async(prompt)
```

### retry ve fallback

### secure key management
HashiCorp Vault
