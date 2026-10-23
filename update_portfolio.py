import os
import json
from datetime import datetime
import google.generativeai as genai

print("--- Portföy Yapay Zeka Güncelleme Botu Başlatıldı ---")
print(f"İşlem Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

try:
    # API Anahtarını al ve Gemini'ı yapılandır
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("HATA: GEMINI_API_KEY bulunamadı!")
        exit(1)

    genai.configure(api_key=api_key)

    # Takip edilen varlıklar listesi (Test için şimdilik ilk 2 varlık ile test edelim)
    assets = [
        {"symbol": "THYAO", "name": "Türk Hava Yolları", "category": "bist"},
        {"symbol": "BTC", "name": "Bitcoin", "category": "crypto"}
    ]

    model = genai.GenerativeModel('gemini-1.5-flash')
    updated_data = []

    for asset in assets:
        print(f"Analiz ediliyor: {asset['symbol']} ({asset['name']})...")
        
        prompt = f"""
        Sen profesyonel bir finans analistisin. {asset['name']} ({asset['symbol']}) için kısa bir günlük analiz özeti hazırla.
        Şu kurallara uy:
        1. Açıklama en fazla 2-3 cümle Türkçe olsun.
        2. Duygu durumu olarak sadece şunu seç: "Olumlu", "Nötr", "Dikkat" (Hangisi uygunsa).
        3. Yanıtı sadece şu JSON formatında ver, başka hiçbir metin ekleme:
        {{"sentiment": "Seçilen Duygu", "summary": "2-3 cümlelik Türkçe özet."}}
        """
        
        response = model.generate_content(prompt)
        text_res = response.text.strip()
        
        if text_res.startswith("```json"):
            text_res = text_res[7:]
        if text_res.endswith("```"):
            text_res = text_res[:-3]
                
        data = json.loads(text_res.strip())
        asset["sentiment"] = data.get("sentiment", "Nötr")
        asset["summary"] = data.get("summary", "Güncel veriler takip ediliyor.")
        updated_data.append(asset)

    # Sonuçları JSON dosyasına kaydet
    with open("portfolio_data.json", "w", encoding="utf-8") as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=4)

    print("Dosya başarıyla oluşturuldu ve kaydedildi!")

except Exception as e:
    print(f"KRİTİK HATA OLUŞTU: {str(e)}")
    raise e

print("--- Güncelleme Tamamlandı ---")
