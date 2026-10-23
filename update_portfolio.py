import os
import json
from datetime import datetime
import google.generativeai as genai

print("--- Portföy Yapay Zeka Güncelleme Botu Başlatıldı ---")
print(f"İşlem Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# API Anahtarını al ve Gemini'ı yapılandır
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("HATA: GEMINI_API_KEY bulunamadı!")
    exit(1)

genai.configure(api_key=api_key)

# Takip edilen varlıklar listesi
assets = [
    {"symbol": "THYAO", "name": "Türk Hava Yolları", "category": "bist"},
    {"symbol": "TUPRS", "name": "Tüpraş", "category": "bist"},
    {"symbol": "ISCTR", "name": "İş Bankası", "category": "bist"},
    {"symbol": "ASELS", "name": "Aselsan", "category": "bist"},
    {"symbol": "TSLA", "name": "Tesla Inc.", "category": "us"},
    {"symbol": "NVDA", "name": "NVIDIA Corp.", "category": "us"},
    {"symbol": "ASTS", "name": "AST SpaceMobile", "category": "us"},
    {"symbol": "UUUU", "name": "Energy Fuels Inc.", "category": "us"},
    {"symbol": "BTC", "name": "Bitcoin", "category": "crypto"},
    {"symbol": "ETH", "name": "Ethereum", "category": "crypto"},
    {"symbol": "SOL", "name": "Solana", "category": "crypto"},
    {"symbol": "XRP", "name": "Ripple", "category": "crypto"},
    {"symbol": "TAO", "name": "Bittensor", "category": "crypto"},
    {"symbol": "NEAR", "name": "Near Protocol", "category": "crypto"}
]

# Gemini modeli seçimi (Ücretsiz ve hızlı model)
model = genai.GenerativeModel('gemini-1.5-flash')

updated_data = []

for asset in assets:
    print(f"Analiz ediliyor: {asset['symbol']} ({asset['name']})...")
    
    prompt = f"""
    Sen profesyonel bir finans analistisin. {asset['name']} ({asset['symbol']}) hissesi/kripto parası için güncel piyasa koşullarını, beklentileri ve genel eğilimi göz önüne alarak kısa bir günlük analiz özeti hazırla.
    
    Şu kurallara kesinlikle uy:
    1. Açıklama net, profesyonel ve Türkçe olsun, en fazla 2-3 cümle sürsün.
    2. Duygu durumu olarak sadece şu üçünden birini seç: "Yüksek Olumlu", "Olumlu", "Nötr", "Dikkat" (Hangisi uygunsa).
    3. Yanıtı sadece şu JSON formatında ver, başka hiçbir metin veya markdown ekleme:
    {{"sentiment": "Seçilen Duygu", "summary": "2-3 cümlelik Türkçe özet metni."}}
    """
    
    try:
        response = model.generate_content(prompt)
        text_res = response.text.strip()
        # Markdown blok işaretlerini temizle
        if text_res.startswith("```json"):
            text_res = text_res[7:]
        if text_res.endswith("```"):
            text_res = text_res[:-3]
            
        data = json.loads(text_res.strip())
        asset["sentiment"] = data.get("sentiment", "Nötr")
        asset["summary"] = data.get("summary", "Güncel piyasa verileri analiz ediliyor.")
        updated_data.append(asset)
    except Exception as e:
        print(f"Hata oluştu ({asset['symbol']}): {e}")
        asset["sentiment"] = "Nötr"
        asset["summary"] = "Piyasadaki mevcut yatay seyir ve sektörel gelişmeler takip ediliyor."
        updated_data.append(asset)

# Sonuçları JSON dosyasına kaydet
with open("portfolio_data.json", "w", encoding="utf-8") as f:
    json.dump(updated_data, f, ensure_ascii=False, indent=4)

print("Tüm varlıklar güncellendi ve 'portfolio_data.json' dosyasına kaydedildi!")
print("--- Güncelleme Tamamlandı ---")
