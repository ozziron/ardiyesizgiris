import { Link } from 'react-router-dom'
import { Ship, Mail, Phone, MapPin } from 'lucide-react'

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <Ship className="h-8 w-8 text-blue-400" />
              <span className="text-2xl font-bold">LogiFlow</span>
            </div>
            <p className="text-gray-400 mb-4">
              Türkiye'nin en kapsamlı lojistik hesaplama platformu. 
              Ardiye ve detention hesaplamalarınızı kolayca yapın.
            </p>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">Hızlı Linkler</h3>
            <ul className="space-y-2">
              <li><Link to="/hesaplama" className="text-gray-400 hover:text-white transition-colors">Hesaplama</Link></li>
              <li><Link to="/takip" className="text-gray-400 hover:text-white transition-colors">Konteyner Takip</Link></li>
              <li><Link to="/limanlar" className="text-gray-400 hover:text-white transition-colors">Limanlar</Link></li>
              <li><Link to="/blog" className="text-gray-400 hover:text-white transition-colors">Blog</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">Şirket</h3>
            <ul className="space-y-2">
              <li><Link to="/hakkimizda" className="text-gray-400 hover:text-white transition-colors">Hakkımızda</Link></li>
              <li><Link to="/iletisim" className="text-gray-400 hover:text-white transition-colors">İletişim</Link></li>
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Gizlilik Politikası</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Kullanım Şartları</a></li>
            </ul>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">İletişim</h3>
            <ul className="space-y-2">
              <li className="flex items-center space-x-2">
                <Mail className="h-4 w-4 text-blue-400" />
                <span className="text-gray-400">info@logiflow.com</span>
              </li>
              <li className="flex items-center space-x-2">
                <Phone className="h-4 w-4 text-blue-400" />
                <span className="text-gray-400">+90 212 555 0123</span>
              </li>
              <li className="flex items-center space-x-2">
                <MapPin className="h-4 w-4 text-blue-400" />
                <span className="text-gray-400">İstanbul, Türkiye</span>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8 text-center">
          <p className="text-gray-400">
            © 2025 LogiFlow. Tüm hakları saklıdır.
          </p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
