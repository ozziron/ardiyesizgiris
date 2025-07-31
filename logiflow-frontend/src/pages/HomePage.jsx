import { Link } from 'react-router-dom'
import { Button } from '../components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Calculator, Search, Ship, BarChart3, Clock, Shield } from 'lucide-react'

const HomePage = () => {
  const features = [
    {
      icon: Calculator,
      title: 'Ardiye & Detention Hesaplama',
      description: 'Tüm Türkiye limanları için doğru ve hızlı hesaplama yapın.'
    },
    {
      icon: Search,
      title: 'Konteyner Takip',
      description: 'Konteynerlerinizi gerçek zamanlı olarak takip edin.'
    },
    {
      icon: Ship,
      title: 'Liman Bilgileri',
      description: 'Detaylı liman bilgileri ve free time kuralları.'
    },
    {
      icon: BarChart3,
      title: 'Raporlama',
      description: 'Hesaplama geçmişinizi analiz edin ve raporlayın.'
    },
    {
      icon: Clock,
      title: '7/24 Erişim',
      description: 'İstediğiniz zaman, istediğiniz yerden erişim.'
    },
    {
      icon: Shield,
      title: 'Güvenli Platform',
      description: 'Verileriniz güvenli ve korumalı ortamda saklanır.'
    }
  ]

  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="text-center py-20">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Lojistik Hesaplamalarınızı 
            <span className="text-blue-600"> Kolaylaştırın</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            LogiFlow ile ardiye ve detention hesaplamalarınızı dakikalar içinde yapın. 
            Türkiye'nin en kapsamlı lojistik platformu.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/hesaplama">
              <Button size="lg" className="w-full sm:w-auto">
                Hesaplamaya Başla
              </Button>
            </Link>
            <Link to="/takip">
              <Button variant="outline" size="lg" className="w-full sm:w-auto">
                Konteyner Takip
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Neden LogiFlow?
          </h2>
          <p className="text-lg text-gray-600">
            Lojistik operasyonlarınızı optimize etmek için ihtiyacınız olan tüm araçlar
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <Card key={index} className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="mx-auto w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                  <feature.icon className="h-6 w-6 text-blue-600" />
                </div>
                <CardTitle className="text-xl">{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-gray-600">
                  {feature.description}
                </CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* Stats Section */}
      <section className="bg-blue-600 text-white py-16 rounded-2xl">
        <div className="text-center">
          <h2 className="text-3xl font-bold mb-12">Platform İstatistikleri</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="text-4xl font-bold mb-2">8+</div>
              <div className="text-blue-100">Türkiye Limanı</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">10+</div>
              <div className="text-blue-100">Nakliye Hattı</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">1000+</div>
              <div className="text-blue-100">Hesaplama</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">24/7</div>
              <div className="text-blue-100">Destek</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="text-center py-16">
        <div className="max-w-2xl mx-auto">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Hemen Başlayın
          </h2>
          <p className="text-lg text-gray-600 mb-8">
            Ücretsiz hesap oluşturun ve LogiFlow'un tüm özelliklerinden yararlanın.
          </p>
          <Link to="/kayit">
            <Button size="lg">
              Ücretsiz Kayıt Ol
            </Button>
          </Link>
        </div>
      </section>
    </div>
  )
}

export default HomePage
