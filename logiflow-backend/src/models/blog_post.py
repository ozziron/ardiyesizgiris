from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re

db = SQLAlchemy()

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(250), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.Text)
    
    # Yazar bilgileri
    author = db.Column(db.String(100), default='LogiFlow Editörü')
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Kategori ve etiketler
    category = db.Column(db.String(50))
    tags = db.Column(db.String(200))  # Virgülle ayrılmış etiketler
    
    # SEO bilgileri
    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.String(300))
    featured_image = db.Column(db.String(300))
    
    # Durum ve görünürlük
    status = db.Column(db.String(20), default='draft')  # draft, published, archived
    is_featured = db.Column(db.Boolean, default=False)
    
    # İstatistikler
    view_count = db.Column(db.Integer, default=0)
    like_count = db.Column(db.Integer, default=0)
    
    # Tarih bilgileri
    published_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'content': self.content,
            'excerpt': self.excerpt,
            'author': self.author,
            'author_id': self.author_id,
            'category': self.category,
            'tags': self.tags.split(',') if self.tags else [],
            'meta_title': self.meta_title,
            'meta_description': self.meta_description,
            'featured_image': self.featured_image,
            'status': self.status,
            'is_featured': self.is_featured,
            'view_count': self.view_count,
            'like_count': self.like_count,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_summary_dict(self):
        """Özet bilgiler için kısaltılmış dict"""
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'excerpt': self.excerpt,
            'author': self.author,
            'category': self.category,
            'tags': self.tags.split(',') if self.tags else [],
            'featured_image': self.featured_image,
            'is_featured': self.is_featured,
            'view_count': self.view_count,
            'like_count': self.like_count,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @staticmethod
    def generate_slug(title):
        """Başlıktan URL-friendly slug oluştur"""
        # Türkçe karakterleri değiştir
        char_map = {
            'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u',
            'Ç': 'C', 'Ğ': 'G', 'İ': 'I', 'Ö': 'O', 'Ş': 'S', 'Ü': 'U'
        }
        
        slug = title.lower()
        for turkish_char, english_char in char_map.items():
            slug = slug.replace(turkish_char, english_char)
        
        # Özel karakterleri kaldır ve boşlukları tire ile değiştir
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug)
        slug = re.sub(r'-+', '-', slug)
        slug = slug.strip('-')
        
        return slug
    
    def generate_excerpt(self, length=200):
        """İçerikten otomatik özet oluştur"""
        if self.excerpt:
            return self.excerpt
        
        # HTML etiketlerini kaldır
        import re
        clean_content = re.sub(r'<[^>]+>', '', self.content)
        
        # İlk paragrafı al veya belirtilen uzunlukta kes
        if len(clean_content) <= length:
            return clean_content
        
        excerpt = clean_content[:length]
        # Son kelimeyi tam al
        last_space = excerpt.rfind(' ')
        if last_space > 0:
            excerpt = excerpt[:last_space]
        
        return excerpt + '...'
    
    def increment_view_count(self):
        """Görüntülenme sayısını artır"""
        self.view_count += 1
        db.session.commit()
    
    def increment_like_count(self):
        """Beğeni sayısını artır"""
        self.like_count += 1
        db.session.commit()
    
    @staticmethod
    def create_default_posts():
        """Varsayılan blog yazılarını oluştur"""
        default_posts = [
            {
                'title': 'LogiFlow Platformuna Hoş Geldiniz',
                'content': '''
                <h2>Lojistik Dünyasında Yeni Bir Dönem</h2>
                <p>LogiFlow platformu ile konteyner taşımacılığında ardiye ve detention hesaplamalarınızı artık çok daha kolay yapabilirsiniz. Modern teknolojilerle desteklenen platformumuz, lojistik profesyonellerine zaman kazandırmak ve maliyetleri optimize etmek için tasarlandı.</p>
                
                <h3>Neler Sunuyoruz?</h3>
                <ul>
                <li>Tüm Türkiye limanları için ardiye hesaplama</li>
                <li>Detention hesaplama modülü</li>
                <li>Konteyner takip sistemi</li>
                <li>Detaylı raporlama</li>
                <li>Mobil uyumlu arayüz</li>
                </ul>
                
                <p>Platformumuz sürekli geliştirilmekte ve yeni özellikler eklenmektedir. Geri bildirimleriniz bizim için çok değerli.</p>
                ''',
                'category': 'Duyuru',
                'tags': 'platform,duyuru,özellik',
                'status': 'published',
                'is_featured': True,
                'published_at': datetime.utcnow()
            },
            {
                'title': 'Ardiye ve Detention Hesaplama Rehberi',
                'content': '''
                <h2>Ardiye ve Detention Nedir?</h2>
                <p>Konteyner taşımacılığında en önemli maliyet kalemlerinden biri olan ardiye ve detention ücretlerini doğru hesaplamak, lojistik operasyonlarının karlılığı açısından kritik öneme sahiptir.</p>
                
                <h3>Ardiye (Demurrage)</h3>
                <p>Ardiye, konteynerin limanda belirlenen süreyi aşarak kalması durumunda ödenen ücrettir. Her liman ve nakliye hattının kendine özgü ardiye kuralları vardır.</p>
                
                <h3>Detention</h3>
                <p>Detention ise konteynerin liman dışında (müşteri deposunda) belirlenen süreyi aşarak kalması durumunda ödenen ücrettir.</p>
                
                <h3>Hesaplama Faktörleri</h3>
                <ul>
                <li>Liman politikaları</li>
                <li>Nakliye hattı kuralları</li>
                <li>Konteyner tipi</li>
                <li>Özel yük durumları (IMO, OOG)</li>
                <li>Tatil günleri ve hafta sonları</li>
                </ul>
                
                <p>LogiFlow platformu tüm bu faktörleri dikkate alarak en doğru hesaplamayı yapar.</p>
                ''',
                'category': 'Rehber',
                'tags': 'ardiye,detention,hesaplama,rehber',
                'status': 'published',
                'is_featured': False,
                'published_at': datetime.utcnow()
            },
            {
                'title': 'Türkiye Limanlarında Free Time Süreleri',
                'content': '''
                <h2>Türkiye Limanlarında Free Time Politikaları</h2>
                <p>Türkiye'nin başlıca limanlarında uygulanan free time süreleri ve özel durumlar hakkında detaylı bilgiler.</p>
                
                <h3>İstanbul Limanı</h3>
                <p>Ardiye: 7 gün, Detention: 10 gün. Türkiye'nin en büyük limanı olan İstanbul Limanı, yoğunluğu nedeniyle standart free time süreleri uygular.</p>
                
                <h3>İzmir Limanı</h3>
                <p>Ardiye: 7 gün, Detention: 10 gün. Ege Bölgesi'nin en önemli limanı olan İzmir, ihracat yoğunluğu nedeniyle rekabetçi free time süreleri sunar.</p>
                
                <h3>Mersin Limanı</h3>
                <p>Ardiye: 10 gün, Detention: 12 gün. Akdeniz'in en büyük limanı olan Mersin, daha uzun free time süreleri ile öne çıkar.</p>
                
                <h3>Özel Durumlar</h3>
                <ul>
                <li>IMO yüklerde genellikle 2 gün azalma</li>
                <li>OOG yüklerde 1 gün azalma</li>
                <li>Soğutmalı konteynerlerde özel kurallar</li>
                <li>Tatil günleri hesaplama dışı</li>
                </ul>
                
                <p>Güncel free time bilgileri için platformumuzu kullanabilirsiniz.</p>
                ''',
                'category': 'Bilgi',
                'tags': 'liman,free time,türkiye,politika',
                'status': 'published',
                'is_featured': False,
                'published_at': datetime.utcnow()
            }
        ]
        
        for post_data in default_posts:
            # Slug oluştur
            post_data['slug'] = BlogPost.generate_slug(post_data['title'])
            
            # Özet oluştur
            if 'excerpt' not in post_data:
                # HTML etiketlerini kaldırarak özet oluştur
                import re
                clean_content = re.sub(r'<[^>]+>', '', post_data['content'])
                post_data['excerpt'] = clean_content[:200] + '...' if len(clean_content) > 200 else clean_content
            
            # SEO bilgileri
            post_data['meta_title'] = post_data['title']
            post_data['meta_description'] = post_data['excerpt']
            
            existing_post = BlogPost.query.filter_by(slug=post_data['slug']).first()
            if not existing_post:
                blog_post = BlogPost(**post_data)
                db.session.add(blog_post)
        
        db.session.commit()

