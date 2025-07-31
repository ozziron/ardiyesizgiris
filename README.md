# 🚢 LogiFlow - Kapsamlı Lojistik Platformu

**Türkiye'nin en gelişmiş ardiye ve detention hesaplama platformu**

## ✨ Özellikler

### 🎯 Ana Fonksiyonlar
- **Ardiye Hesaplama**: Konteyner liman kalış süresi hesaplaması
- **Detention Hesaplama**: Konteyner liman dışı kalış süresi hesaplaması  
- **Konteyner Takip**: Gerçek zamanlı konteyner takip sistemi
- **Liman Bilgileri**: 8 Türkiye limanı detaylı bilgileri
- **Blog Sistemi**: Lojistik sektörü haberleri ve makaleleri

### 🔧 Teknik Özellikler
- **Modern React Frontend**: Tailwind CSS, shadcn/ui bileşenleri
- **Flask Backend API**: RESTful API, JWT kimlik doğrulama
- **SQLite Veritabanı**: Hafif ve hızlı veri depolama
- **Responsive Tasarım**: Mobil ve desktop uyumlu
- **Admin Paneli**: Kapsamlı yönetim arayüzü

### 📊 Desteklenen Veriler
- **8 Türkiye Limanı**: İstanbul, İzmir, Mersin, Ambarlı, vb.
- **10+ Konteyner Tipi**: 20DC, 40DC, 40HC, 45HC, vb.
- **10+ Nakliye Hattı**: Maersk, MSC, CMA CGM, COSCO, vb.
- **Free Time Kuralları**: Liman ve hat bazlı özelleştirilebilir

## 🚀 Kurulum

### Backend Kurulumu
```bash
cd logiflow-backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
python src/main.py
```

### Frontend Kurulumu
```bash
cd logiflow-frontend
npm install
npm run dev
```

## 🔐 Giriş Bilgileri

### Admin Hesabı
- **Kullanıcı Adı**: `umutozdemir`
- **Şifre**: `Munafes91!`
- **Rol**: Super Admin

### Test Hesabı
- **Kullanıcı Adı**: `testuser`
- **Şifre**: `test123`
- **Rol**: Normal Kullanıcı

## 📡 API Endpoints

### Kimlik Doğrulama
- `POST /api/auth/login` - Kullanıcı girişi
- `POST /api/auth/register` - Kullanıcı kaydı
- `GET /api/auth/me` - Mevcut kullanıcı bilgileri

### Hesaplama
- `GET /api/calculations` - Kullanıcı hesaplama geçmişi
- `POST /api/calculations` - Yeni hesaplama oluştur
- `GET /api/calculations/{id}` - Hesaplama detayı

### Veri Yönetimi
- `GET /api/ports` - Liman listesi
- `GET /api/container-types` - Konteyner tipi listesi
- `GET /api/shipping-lines` - Nakliye hattı listesi

### Konteyner Takip
- `POST /api/tracking/search` - Konteyner arama
- `GET /api/tracking` - Kullanıcı takip listesi
- `POST /api/tracking` - Takip listesine ekleme

### Blog
- `GET /api/blog` - Blog yazıları listesi
- `GET /api/blog/{slug}` - Blog yazısı detayı
- `GET /api/blog/featured` - Öne çıkan yazılar

### Admin
- `GET /api/admin/dashboard` - Admin dashboard
- `GET /api/admin/users` - Kullanıcı listesi

## 🏗️ Proje Yapısı

```
logiflow-platform/
├── logiflow-backend/          # Flask Backend
│   ├── src/
│   │   ├── models/           # Veritabanı modelleri
│   │   ├── routes/           # API route'ları
│   │   ├── static/           # Frontend build dosyaları
│   │   └── main.py           # Ana uygulama
│   └── requirements.txt      # Python bağımlılıkları
├── logiflow-frontend/         # React Frontend
│   ├── src/
│   │   ├── components/       # React bileşenleri
│   │   ├── pages/           # Sayfa bileşenleri
│   │   ├── contexts/        # React context'leri
│   │   └── hooks/           # Custom hook'lar
│   └── package.json         # Node.js bağımlılıkları
└── README.md                # Bu dosya
```

## 🎨 Tasarım Sistemi

### Renk Paleti
- **Birincil**: Mavi tonları (#3B82F6, #1E40AF)
- **İkincil**: Gri tonları (#6B7280, #374151)
- **Başarı**: Yeşil (#10B981)
- **Uyarı**: Turuncu (#F59E0B)
- **Hata**: Kırmızı (#EF4444)

### Tipografi
- **Ana Font**: Inter (sistem fontu)
- **Başlıklar**: 2xl-5xl boyutları
- **Metin**: sm-lg boyutları

## 🔧 Geliştirme

### Yeni Özellik Ekleme
1. Backend'de model ve route oluştur
2. Frontend'de sayfa/bileşen geliştir
3. API entegrasyonu yap
4. Test et ve commit et

### Veritabanı Güncelleme
1. Model dosyasını güncelle
2. `create_default_*` fonksiyonunu çalıştır
3. Veritabanını yeniden oluştur

## 📈 Performans

- **Backend**: Flask + SQLite (hızlı sorgu yanıtları)
- **Frontend**: React + Vite (hızlı build ve hot reload)
- **Optimizasyon**: Lazy loading, code splitting
- **Caching**: Browser cache, API response cache

## 🛡️ Güvenlik

- **JWT Token**: Güvenli kimlik doğrulama
- **Password Hashing**: Werkzeug güvenli hash
- **CORS**: Cross-origin istekleri kontrol
- **Input Validation**: Form ve API validasyonu

## 📱 Mobil Uyumluluk

- **Responsive Design**: Tüm ekran boyutları
- **Touch Friendly**: Mobil dokunmatik arayüz
- **Progressive Web App**: PWA desteği (gelecek)

## 🌐 Deployment

### Production Deployment
```bash
# Backend
cd logiflow-backend
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.main:app

# Frontend
cd logiflow-frontend
npm run build
# Build dosyalarını web sunucusuna kopyala
```

### Docker Deployment (Gelecek)
```bash
docker-compose up -d
```

## 📞 Destek

- **E-posta**: info@logiflow.com
- **Telefon**: +90 212 555 0123
- **GitHub Issues**: Bu repository'de issue açın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🙏 Katkıda Bulunanlar

- **Geliştirici**: Umut Özdemir (@ozziron)
- **Tasarım**: LogiFlow Tasarım Ekibi
- **Test**: LogiFlow QA Ekibi

---

**© 2025 LogiFlow. Tüm hakları saklıdır.**

*Türkiye'nin en kapsamlı lojistik hesaplama platformu* 🚢

