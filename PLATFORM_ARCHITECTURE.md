# LogiFlow - Kapsamlı Lojistik Platformu Mimarisi

**Proje Adı:** LogiFlow  
**Versiyon:** 1.0.0  
**Geliştirici:** Manus AI  
**Tarih:** 31 Temmuz 2025

## 1. Platform Vizyonu ve Misyonu

### Vizyon
LogiFlow, Türkiye'nin en kapsamlı ve kullanıcı dostu lojistik hesaplama platformu olmayı hedefler. Konteyner taşımacılığında ardiye ve detention hesaplamalarından konteyner takibine, liman bilgilerinden mobil erişime kadar tüm lojistik ihtiyaçları tek platformda çözmeyi amaçlar.

### Misyon
Lojistik profesyonellerine zaman kazandırmak, maliyetleri optimize etmek ve operasyonel verimliliği artırmak için modern teknolojilerle desteklenmiş, güvenilir ve erişilebilir bir platform sunmak.

## 2. Teknik Mimari

### 2.1 Frontend Mimarisi
- **Framework:** Next.js 15 (React 18 tabanlı)
- **Styling:** Tailwind CSS + Shadcn/UI
- **State Management:** React Context API + Local Storage
- **Form Management:** React Hook Form + Zod Validation
- **Icons:** Lucide React
- **Charts:** Recharts
- **Deployment:** Static Export (Vercel/Netlify uyumlu)

### 2.2 Backend Mimarisi
- **Framework:** Flask 3.0 (Python)
- **Database:** SQLite (geliştirme) / PostgreSQL (production)
- **ORM:** SQLAlchemy
- **Authentication:** JWT (JSON Web Tokens)
- **API:** RESTful API
- **CORS:** Flask-CORS
- **Validation:** Marshmallow

### 2.3 Veritabanı Tasarımı
```sql
-- Kullanıcılar
users (id, username, email, password_hash, role, created_at, updated_at)

-- Limanlar
ports (id, code, name, country, ardiye_free_days, detention_free_days, created_at)

-- Konteyner Tipleri
container_types (id, code, name, size, type, created_at)

-- Nakliye Hatları
shipping_lines (id, code, name, multiplier, created_at)

-- Hesaplamalar
calculations (id, user_id, port_id, container_type_id, line_id, calculation_type, 
              vessel_departure, gate_in, gate_out, is_imo, is_oog, result_date, 
              free_days, remaining_days, created_at)

-- Konteyner Takip
container_tracking (id, user_id, container_no, bl_no, booking_no, vessel_name,
                   loading_port, discharge_port, current_location, status,
                   eta, ata, gate_in_date, gate_out_date, last_update)

-- Blog Yazıları
blog_posts (id, title, slug, content, excerpt, author, status, created_at, updated_at)

-- Sistem Ayarları
settings (id, key, value, description, created_at, updated_at)
```

## 3. Kullanıcı Deneyimi (UX) Tasarımı

### 3.1 Tasarım Prensipleri
1. **Minimalizm:** Temiz, sade ve odaklanmış arayüz
2. **Erişilebilirlik:** WCAG 2.1 AA standartlarına uyum
3. **Responsive:** Mobil-first yaklaşım
4. **Performans:** Hızlı yükleme ve smooth animasyonlar
5. **Kullanılabilirlik:** Sezgisel navigasyon ve açık bilgi mimarisi

### 3.2 Renk Paleti
- **Primary:** #0EA5E9 (Sky Blue) - Güven ve profesyonellik
- **Secondary:** #10B981 (Emerald) - Başarı ve büyüme
- **Accent:** #F59E0B (Amber) - Dikkat ve enerji
- **Neutral:** #64748B (Slate) - Denge ve sakinlik
- **Background:** #F8FAFC (Slate 50) - Temizlik ve açıklık

### 3.3 Tipografi
- **Heading Font:** Inter (Modern, okunabilir)
- **Body Font:** Inter (Tutarlılık için aynı font)
- **Monospace:** JetBrains Mono (Kod ve veriler için)

## 4. Sayfa Yapısı ve Navigasyon

### 4.1 Ana Sayfalar
1. **Ana Sayfa (/)** - Hero section, özellikler, istatistikler
2. **Hesaplama (/hesaplama)** - Ardiye/Detention hesaplama modülleri
3. **Konteyner Takip (/takip)** - Konteyner arama ve takip
4. **Limanlar (/limanlar)** - Liman bilgileri ve detayları
5. **Blog (/blog)** - Lojistik haberleri ve makaleler
6. **Hakkımızda (/hakkimizda)** - Platform bilgileri
7. **İletişim (/iletisim)** - İletişim formu ve bilgiler

### 4.2 Kullanıcı Sayfaları
1. **Giriş (/giris)** - Kullanıcı girişi
2. **Kayıt (/kayit)** - Yeni kullanıcı kaydı
3. **Profil (/profil)** - Kullanıcı profili ve ayarları
4. **Geçmiş (/gecmis)** - Hesaplama geçmişi
5. **Favoriler (/favoriler)** - Favori hesaplamalar

### 4.3 Admin Sayfaları
1. **Admin Panel (/admin)** - Genel yönetim
2. **Kullanıcı Yönetimi (/admin/kullanicilar)** - Kullanıcı CRUD
3. **Liman Yönetimi (/admin/limanlar)** - Liman CRUD
4. **İçerik Yönetimi (/admin/icerik)** - Blog ve sayfa yönetimi
5. **Sistem Ayarları (/admin/ayarlar)** - Platform ayarları

## 5. Özellik Detayları

### 5.1 Hesaplama Modülü
- **Ardiye Hesaplama:** Konteyner limanda kalma süresi hesaplama
- **Detention Hesaplama:** Konteyner dışarıda kalma süresi hesaplama
- **Akıllı Algoritma:** Tatil günleri, hafta sonları, özel durumlar
- **Çoklu Liman Desteği:** Tüm Türkiye limanları
- **Hat Çarpanları:** Nakliye hattına göre özel hesaplama
- **Özel Yük Desteği:** IMO ve OOG yükleri için özel kurallar

### 5.2 Konteyner Takip Sistemi
- **Gerçek Zamanlı Takip:** API entegrasyonları ile güncel bilgi
- **Çoklu Konteyner:** Birden fazla konteyner takibi
- **Bildirim Sistemi:** E-posta ve SMS bildirimleri
- **Geçmiş Takip:** Konteyner hareketlerinin geçmişi
- **Harita Entegrasyonu:** Konteyner konumunun haritada gösterimi

### 5.3 Kullanıcı Yönetimi
- **Rol Tabanlı Erişim:** Admin, Kullanıcı, Misafir rolleri
- **JWT Authentication:** Güvenli token tabanlı kimlik doğrulama
- **Profil Yönetimi:** Kullanıcı bilgileri ve tercihler
- **Aktivite Takibi:** Kullanıcı işlemlerinin loglanması

### 5.4 Raporlama ve Analitik
- **Hesaplama Raporları:** PDF/Excel export
- **Kullanım İstatistikleri:** Platform kullanım metrikleri
- **Maliyet Analizi:** Ardiye/detention maliyet hesaplamaları
- **Trend Analizi:** Zaman bazlı trend grafikleri

## 6. Güvenlik ve Performans

### 6.1 Güvenlik Önlemleri
- **HTTPS Zorunluluğu:** Tüm iletişim şifreli
- **Input Validation:** Tüm girişlerin doğrulanması
- **SQL Injection Koruması:** Parametreli sorgular
- **XSS Koruması:** Output encoding
- **CSRF Koruması:** Token tabanlı koruma
- **Rate Limiting:** API isteklerinin sınırlandırılması

### 6.2 Performans Optimizasyonları
- **Code Splitting:** Sayfa bazlı kod bölünmesi
- **Image Optimization:** Next.js Image component
- **Caching:** Browser ve server-side caching
- **Lazy Loading:** Gerektiğinde yükleme
- **Bundle Optimization:** Webpack optimizasyonları

## 7. Mobil Uyumluluk

### 7.1 Responsive Design
- **Mobile-First:** Önce mobil, sonra desktop
- **Breakpoints:** 320px, 768px, 1024px, 1280px
- **Touch-Friendly:** Dokunmatik ekran optimizasyonu
- **Offline Support:** Service Worker ile offline çalışma

### 7.2 Progressive Web App (PWA)
- **App Manifest:** Uygulama bilgileri
- **Service Worker:** Offline ve caching
- **Push Notifications:** Bildirim desteği
- **Install Prompt:** Ana ekrana ekleme

## 8. API Tasarımı

### 8.1 RESTful API Endpoints
```
Authentication:
POST /api/auth/login
POST /api/auth/register
POST /api/auth/logout
GET  /api/auth/me

Calculations:
GET    /api/calculations
POST   /api/calculations
GET    /api/calculations/:id
PUT    /api/calculations/:id
DELETE /api/calculations/:id

Container Tracking:
GET    /api/tracking
POST   /api/tracking/search
GET    /api/tracking/:id
POST   /api/tracking/:id/subscribe

Ports:
GET    /api/ports
GET    /api/ports/:id
POST   /api/ports (admin)
PUT    /api/ports/:id (admin)
DELETE /api/ports/:id (admin)

Blog:
GET    /api/blog
GET    /api/blog/:slug
POST   /api/blog (admin)
PUT    /api/blog/:id (admin)
DELETE /api/blog/:id (admin)
```

### 8.2 API Response Format
```json
{
  "success": true,
  "data": {},
  "message": "İşlem başarılı",
  "timestamp": "2025-07-31T00:00:00Z",
  "version": "1.0.0"
}
```

## 9. Deployment ve DevOps

### 9.1 Deployment Stratejisi
- **Frontend:** Vercel/Netlify static hosting
- **Backend:** Railway/Heroku container deployment
- **Database:** PostgreSQL (Supabase/Railway)
- **CDN:** Cloudflare
- **Monitoring:** Sentry error tracking

### 9.2 CI/CD Pipeline
- **Version Control:** Git (GitHub)
- **Testing:** Jest + Cypress
- **Build:** GitHub Actions
- **Deployment:** Automatic deployment on main branch
- **Rollback:** Quick rollback capability

## 10. Gelecek Planları

### 10.1 Faz 2 Özellikler
- **API Entegrasyonları:** Gerçek liman API'leri
- **Mobil Uygulama:** React Native app
- **AI Tahminleme:** Makine öğrenmesi ile tahmin
- **Blockchain:** Konteyner takip için blockchain
- **IoT Entegrasyonu:** Sensör verileri

### 10.2 Faz 3 Özellikler
- **Multi-tenant:** Şirket bazlı ayrım
- **White-label:** Özelleştirilebilir platform
- **API Marketplace:** Üçüncü taraf entegrasyonlar
- **Advanced Analytics:** Business intelligence
- **Global Expansion:** Uluslararası limanlar

## 11. Sonuç

LogiFlow platformu, modern web teknolojileri kullanılarak geliştirilecek, kullanıcı odaklı, güvenli ve ölçeklenebilir bir lojistik çözümüdür. Bu mimari dokümanda belirlenen prensipler ve teknolojiler doğrultusunda, sektörün ihtiyaçlarını karşılayan, rekabetçi ve sürdürülebilir bir platform oluşturulacaktır.

Platform, aşamalı geliştirme yaklaşımı ile önce temel özellikler hayata geçirilecek, ardından kullanıcı geri bildirimlerine göre geliştirilecek ve genişletilecektir. Bu yaklaşım, hem geliştirme risklerini minimize edecek hem de kullanıcı memnuniyetini maksimize edecektir.

