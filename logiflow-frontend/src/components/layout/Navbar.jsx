import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext'
import { Button } from '../ui/button'
import { Menu, X, Ship, User, LogOut } from 'lucide-react'

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false)
  const { user, logout, isAuthenticated } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <nav className="bg-white shadow-lg border-b border-blue-100">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          <Link to="/" className="flex items-center space-x-2">
            <Ship className="h-8 w-8 text-blue-600" />
            <span className="text-2xl font-bold text-gray-800">LogiFlow</span>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-6">
            <Link to="/" className="text-gray-700 hover:text-blue-600 transition-colors">Ana Sayfa</Link>
            <Link to="/hesaplama" className="text-gray-700 hover:text-blue-600 transition-colors">Hesaplama</Link>
            <Link to="/takip" className="text-gray-700 hover:text-blue-600 transition-colors">Konteyner Takip</Link>
            <Link to="/limanlar" className="text-gray-700 hover:text-blue-600 transition-colors">Limanlar</Link>
            <Link to="/blog" className="text-gray-700 hover:text-blue-600 transition-colors">Blog</Link>
            
            {isAuthenticated ? (
              <div className="flex items-center space-x-4">
                <Link to="/profil" className="flex items-center space-x-1 text-gray-700 hover:text-blue-600">
                  <User className="h-4 w-4" />
                  <span>{user?.username}</span>
                </Link>
                {user?.role === 'super_admin' && (
                  <Link to="/admin" className="text-gray-700 hover:text-blue-600">Admin</Link>
                )}
                <Button variant="outline" size="sm" onClick={handleLogout}>
                  <LogOut className="h-4 w-4 mr-1" />
                  Çıkış
                </Button>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <Link to="/giris">
                  <Button variant="outline" size="sm">Giriş</Button>
                </Link>
                <Link to="/kayit">
                  <Button size="sm">Kayıt Ol</Button>
                </Link>
              </div>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden"
            onClick={() => setIsOpen(!isOpen)}
          >
            {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>

        {/* Mobile Menu */}
        {isOpen && (
          <div className="md:hidden py-4 border-t border-gray-200">
            <div className="flex flex-col space-y-2">
              <Link to="/" className="py-2 text-gray-700 hover:text-blue-600">Ana Sayfa</Link>
              <Link to="/hesaplama" className="py-2 text-gray-700 hover:text-blue-600">Hesaplama</Link>
              <Link to="/takip" className="py-2 text-gray-700 hover:text-blue-600">Konteyner Takip</Link>
              <Link to="/limanlar" className="py-2 text-gray-700 hover:text-blue-600">Limanlar</Link>
              <Link to="/blog" className="py-2 text-gray-700 hover:text-blue-600">Blog</Link>
              
              {isAuthenticated ? (
                <>
                  <Link to="/profil" className="py-2 text-gray-700 hover:text-blue-600">Profil</Link>
                  {user?.role === 'super_admin' && (
                    <Link to="/admin" className="py-2 text-gray-700 hover:text-blue-600">Admin</Link>
                  )}
                  <button onClick={handleLogout} className="py-2 text-left text-gray-700 hover:text-blue-600">
                    Çıkış
                  </button>
                </>
              ) : (
                <>
                  <Link to="/giris" className="py-2 text-gray-700 hover:text-blue-600">Giriş</Link>
                  <Link to="/kayit" className="py-2 text-gray-700 hover:text-blue-600">Kayıt Ol</Link>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}

export default Navbar
