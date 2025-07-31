import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { Button } from '../components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Input } from '../components/ui/input'
import { Label } from '../components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs'
import { Checkbox } from '../components/ui/checkbox'
import { useToast } from '../hooks/use-toast'
import { Calculator, Calendar, Ship, Package } from 'lucide-react'

const CalculationPage = () => {
  const { token, isAuthenticated } = useAuth()
  const { toast } = useToast()
  const [loading, setLoading] = useState(false)
  const [ports, setPorts] = useState([])
  const [containerTypes, setContainerTypes] = useState([])
  const [shippingLines, setShippingLines] = useState([])
  const [result, setResult] = useState(null)

  const [formData, setFormData] = useState({
    port_id: '',
    container_type_id: '',
    shipping_line_id: '',
    calculation_type: 'ardiye',
    vessel_departure: '',
    gate_in_date: '',
    gate_out_date: '',
    is_imo: false,
    is_oog: false
  })

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [portsRes, typesRes, linesRes] = await Promise.all([
        fetch('/api/ports'),
        fetch('/api/container-types'),
        fetch('/api/shipping-lines')
      ])

      const [portsData, typesData, linesData] = await Promise.all([
        portsRes.json(),
        typesRes.json(),
        linesRes.json()
      ])

      if (portsData.success) setPorts(portsData.data)
      if (typesData.success) setContainerTypes(typesData.data)
      if (linesData.success) setShippingLines(linesData.data)
    } catch (error) {
      toast({
        title: "Hata",
        description: "Veriler yüklenirken hata oluştu",
        variant: "destructive"
      })
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!isAuthenticated) {
      toast({
        title: "Giriş Gerekli",
        description: "Hesaplama yapmak için giriş yapmalısınız",
        variant: "destructive"
      })
      return
    }

    setLoading(true)
    
    try {
      const response = await fetch('/api/calculations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      })

      const data = await response.json()

      if (data.success) {
        setResult(data.data)
        toast({
          title: "Başarılı",
          description: "Hesaplama tamamlandı"
        })
      } else {
        toast({
          title: "Hata",
          description: data.message,
          variant: "destructive"
        })
      }
    } catch (error) {
      toast({
        title: "Hata",
        description: "Hesaplama sırasında hata oluştu",
        variant: "destructive"
      })
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Ardiye & Detention Hesaplama
        </h1>
        <p className="text-lg text-gray-600">
          Konteyner taşımacılığında ardiye ve detention hesaplamalarınızı yapın
        </p>
      </div>

      <Tabs value={formData.calculation_type} onValueChange={(value) => handleInputChange('calculation_type', value)}>
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="ardiye">Ardiye Hesaplama</TabsTrigger>
          <TabsTrigger value="detention">Detention Hesaplama</TabsTrigger>
        </TabsList>

        <TabsContent value="ardiye" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Calculator className="h-5 w-5" />
                Ardiye Hesaplama Formu
              </CardTitle>
              <CardDescription>
                Konteynerin limanda kalma süresine göre ardiye hesaplaması yapın
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <Label htmlFor="port">Liman</Label>
                    <Select value={formData.port_id} onValueChange={(value) => handleInputChange('port_id', value)}>
                      <SelectTrigger>
                        <SelectValue placeholder="Liman seçin" />
                      </SelectTrigger>
                      <SelectContent>
                        {ports.map(port => (
                          <SelectItem key={port.id} value={port.id.toString()}>
                            {port.name} ({port.code})
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="container_type">Konteyner Tipi</Label>
                    <Select value={formData.container_type_id} onValueChange={(value) => handleInputChange('container_type_id', value)}>
                      <SelectTrigger>
                        <SelectValue placeholder="Konteyner tipi seçin" />
                      </SelectTrigger>
                      <SelectContent>
                        {containerTypes.map(type => (
                          <SelectItem key={type.id} value={type.id.toString()}>
                            {type.name} ({type.code})
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="shipping_line">Nakliye Hattı</Label>
                    <Select value={formData.shipping_line_id} onValueChange={(value) => handleInputChange('shipping_line_id', value)}>
                      <SelectTrigger>
                        <SelectValue placeholder="Nakliye hattı seçin" />
                      </SelectTrigger>
                      <SelectContent>
                        {shippingLines.map(line => (
                          <SelectItem key={line.id} value={line.id.toString()}>
                            {line.name} ({line.code})
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="vessel_departure">Gemi Kalkış Tarihi</Label>
                    <Input
                      type="date"
                      value={formData.vessel_departure}
                      onChange={(e) => handleInputChange('vessel_departure', e.target.value)}
                      required
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="gate_out_date">Gate Out Tarihi</Label>
                    <Input
                      type="date"
                      value={formData.gate_out_date}
                      onChange={(e) => handleInputChange('gate_out_date', e.target.value)}
                    />
                  </div>
                </div>

                <div className="flex flex-col space-y-4">
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="is_imo"
                      checked={formData.is_imo}
                      onCheckedChange={(checked) => handleInputChange('is_imo', checked)}
                    />
                    <Label htmlFor="is_imo">IMO Yük (Tehlikeli Madde)</Label>
                  </div>

                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="is_oog"
                      checked={formData.is_oog}
                      onCheckedChange={(checked) => handleInputChange('is_oog', checked)}
                    />
                    <Label htmlFor="is_oog">OOG Yük (Taşmalı Yük)</Label>
                  </div>
                </div>

                <Button type="submit" className="w-full" disabled={loading}>
                  {loading ? 'Hesaplanıyor...' : 'Hesapla'}
                </Button>
              </form>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="detention" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Calculator className="h-5 w-5" />
                Detention Hesaplama Formu
              </CardTitle>
              <CardDescription>
                Konteynerin liman dışında kalma süresine göre detention hesaplaması yapın
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <Label htmlFor="port">Liman</Label>
                    <Select value={formData.port_id} onValueChange={(value) => handleInputChange('port_id', value)}>
                      <SelectTrigger>
                        <SelectValue placeholder="Liman seçin" />
                      </SelectTrigger>
                      <SelectContent>
                        {ports.map(port => (
                          <SelectItem key={port.id} value={port.id.toString()}>
                            {port.name} ({port.code})
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="container_type">Konteyner Tipi</Label>
                    <Select value={formData.container_type_id} onValueChange={(value) => handleInputChange('container_type_id', value)}>
                      <SelectTrigger>
                        <SelectValue placeholder="Konteyner tipi seçin" />
                      </SelectTrigger>
                      <SelectContent>
                        {containerTypes.map(type => (
                          <SelectItem key={type.id} value={type.id.toString()}>
                            {type.name} ({type.code})
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="shipping_line">Nakliye Hattı</Label>
                    <Select value={formData.shipping_line_id} onValueChange={(value) => handleInputChange('shipping_line_id', value)}>
                      <SelectTrigger>
                        <SelectValue placeholder="Nakliye hattı seçin" />
                      </SelectTrigger>
                      <SelectContent>
                        {shippingLines.map(line => (
                          <SelectItem key={line.id} value={line.id.toString()}>
                            {line.name} ({line.code})
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="vessel_departure">Gemi Kalkış Tarihi</Label>
                    <Input
                      type="date"
                      value={formData.vessel_departure}
                      onChange={(e) => handleInputChange('vessel_departure', e.target.value)}
                      required
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="gate_in_date">Gate In Tarihi</Label>
                    <Input
                      type="date"
                      value={formData.gate_in_date}
                      onChange={(e) => handleInputChange('gate_in_date', e.target.value)}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="gate_out_date">Gate Out Tarihi</Label>
                    <Input
                      type="date"
                      value={formData.gate_out_date}
                      onChange={(e) => handleInputChange('gate_out_date', e.target.value)}
                    />
                  </div>
                </div>

                <div className="flex flex-col space-y-4">
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="is_imo_detention"
                      checked={formData.is_imo}
                      onCheckedChange={(checked) => handleInputChange('is_imo', checked)}
                    />
                    <Label htmlFor="is_imo_detention">IMO Yük (Tehlikeli Madde)</Label>
                  </div>

                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="is_oog_detention"
                      checked={formData.is_oog}
                      onCheckedChange={(checked) => handleInputChange('is_oog', checked)}
                    />
                    <Label htmlFor="is_oog_detention">OOG Yük (Taşmalı Yük)</Label>
                  </div>
                </div>

                <Button type="submit" className="w-full" disabled={loading}>
                  {loading ? 'Hesaplanıyor...' : 'Hesapla'}
                </Button>
              </form>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Sonuç Kartı */}
      {result && (
        <Card className="border-green-200 bg-green-50">
          <CardHeader>
            <CardTitle className="text-green-800">Hesaplama Sonucu</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center p-4 bg-white rounded-lg">
                <div className="text-2xl font-bold text-blue-600">{result.free_days}</div>
                <div className="text-sm text-gray-600">Free Time (Gün)</div>
              </div>
              <div className="text-center p-4 bg-white rounded-lg">
                <div className="text-2xl font-bold text-orange-600">{result.used_days}</div>
                <div className="text-sm text-gray-600">Kullanılan Gün</div>
              </div>
              <div className="text-center p-4 bg-white rounded-lg">
                <div className="text-2xl font-bold text-green-600">{result.remaining_days}</div>
                <div className="text-sm text-gray-600">Kalan Gün</div>
              </div>
            </div>
            
            {result.result_date && (
              <div className="text-center p-4 bg-white rounded-lg">
                <div className="text-lg font-semibold text-gray-800">
                  Free Time Bitiş Tarihi: {new Date(result.result_date).toLocaleDateString('tr-TR')}
                </div>
              </div>
            )}

            {result.total_cost > 0 && (
              <div className="text-center p-4 bg-red-50 rounded-lg border border-red-200">
                <div className="text-lg font-semibold text-red-800">
                  Toplam Maliyet: ${result.total_cost.toFixed(2)}
                </div>
                <div className="text-sm text-red-600">
                  Günlük Ücret: ${result.cost_per_day.toFixed(2)}
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  )
}

export default CalculationPage
