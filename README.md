# Kariyer Gelişim Ajanı - Chatbot Uygulaması

Modern, AI destekli kariyer planlama ve danışmanlık chatbot uygulaması.

## 🚀 Özellikler

- **AI Destekli Kariyer Planlaması**: Google Gemini 2.5 Flash modeli ile
- **Streaming Yanıtlar**: Kelime kelime gelen canlı yanıtlar
- **Modern Arayüz**: Bootstrap ve React ile responsive tasarım
- **Avatar & Branding**: Profesyonel görünüm
- **Gerçek Zamanlı Chat**: Anlık mesajlaşma deneyimi

## 📋 Gereksinimler

- Python 3.8+
- Node.js 14+
- npm veya yarn

## 🛠️ Kurulum

### Backend Kurulumu

1. Virtual environment'ı aktive edin:

```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

2. API'yi başlatın:

```bash
python api.py
```

API şu adreste çalışacak: http://localhost:8000

### Frontend Kurulumu

1. Frontend dizinine gidin:

```bash
cd frontend
```

2. Bağımlılıkları yükleyin (zaten yüklü):

```bash
npm install
```

3. React uygulamasını başlatın:

```bash
npm start
```

Uygulama şu adreste açılacak: http://localhost:3000

## 🎯 Kullanım

1. Backend API'yi başlatın (Terminal 1):

```bash
python api.py
```

2. Frontend'i başlatın (Terminal 2):

```bash
cd frontend
npm start
```

3. Tarayıcınızda http://localhost:3000 adresini açın

4. Kariyer hedefinizi chatbot'a yazın ve detaylı planınızı alın!

## 🔑 API Anahtarı

`.env` dosyanızda `GOOGLE_GEMINI_API_KEY` değişkenini ayarladığınızdan emin olun:

```env
GOOGLE_GEMINI_API_KEY=your_api_key_here
```

## 📱 Responsive Tasarım

- Mobil cihazlar için optimize edilmiş
- Tablet ve desktop desteği
- Modern gradient arkaplan
- Smooth animasyonlar

## 🎨 Tasarım Özellikleri

- **Gradient Background**: Mor-mavi gradient arka plan
- **Avatar**: Otomatik oluşturulan profil avatarı
- **Typing Effect**: Kelime kelime gelen mesajlar
- **Status Indicator**: Çevrimiçi durum göstergesi
- **Smooth Animations**: Yumuşak geçişler ve animasyonlar

## 📚 Teknolojiler

### Backend

- FastAPI
- Google Gemini AI
- Python 3.13
- Server-Sent Events (SSE) for streaming

### Frontend

- React 18 (TypeScript)
- Bootstrap 5
- React Bootstrap
- Axios
- CSS3 Animations

## 🤝 Katkıda Bulunma

Projeye katkıda bulunmak isterseniz pull request gönderebilirsiniz.

## 📄 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

## 👤 Yazar

**Bartu**  
Tarih: 21 Ocak 2026  
Versiyon: 1.0.0
