# Parfüm Koleksiyonu Yönetim Uygulaması

Bu uygulama, kullanıcıların parfüm koleksiyonlarını yönetmelerini sağlayan bir masaüstü uygulamasıdır. Python, PyQt5 ve SQLite teknolojileri kullanılarak geliştirilmiştir.

## Özellikler

- Parfüm ekleme, düzenleme ve silme
- Parfüm bilgilerinin detaylı yönetimi (ad, marka, tür, boyut, fiyat vb.)
- Şişe fotoğrafı ekleme ve görüntüleme
- Arama ve filtreleme
- Markaların ve parfüm türlerinin yönetimi
- Modern ve kullanıcı dostu arayüz

## Teknolojiler

- **Python 3.x**: Ana programlama dili
- **PyQt5**: GUI framework
- **Qt Designer**: Arayüz tasarımı
- **SQLite**: Veritabanı yönetimi
- **DB Browser for SQLite**: Veritabanı tasarımı ve yönetimi
- **MVC Mimari**: Model-View-Controller mimari yapısı

## Proje Yapısı

Proje, MVC (Model-View-Controller) mimarisi kullanılarak oluşturulmuştur:

- **main.py**: Uygulamanın başlangıç noktası
- **models/**: Veri modellerini içerir (parfüm, marka, tür)
- **views/**: Kullanıcı arayüzü bileşenlerini içerir
  - Qt Designer ile oluşturulan UI dosyaları (.ui)
  - Bu UI dosyalarının Python'da kullanılması
- **controllers/**: İş mantığını ve veritabanı işlemlerini yönetir
- **utils/**: Yardımcı fonksiyonlar ve stil bileşenlerini içerir
- **resources/**: İkonlar, görseller ve stil dosyaları
- **parfum_koleksiyonu.db**: SQLite veritabanı dosyası

## Kurulum

1. Python 3.x ve pip kurun
2. Gerekli paketleri yükleyin: `pip install PyQt5`
3. Uygulamayı çalıştırın: `python main.py`

## Veritabanı Tasarımı

Uygulama, SQLite veritabanı kullanmaktadır. Veritabanı tasarımı ve yönetimi için DB Browser for SQLite aracı kullanılmıştır. Veritabanında 3 ana tablo bulunmaktadır:

1. **Parfümler** - Parfüm bilgilerini saklayan ana tablo
2. **Markalar** - Parfüm markalarını saklayan tablo
3. **Parfüm Türleri** - Parfüm türlerini saklayan tablo (Eau de Parfum, Eau de Toilette vb.)

Veritabanı şeması aşağıdaki gibidir:

### Parfümler Tablosu
- parfum_id (PRIMARY KEY)
- ad (TEXT)
- marka_id (FOREIGN KEY -> Markalar.marka_id)
- tur_id (FOREIGN KEY -> "Parfüm Türleri".tur_id)
- boyut_ml (REAL)
- kalan_miktar_ml (REAL)
- edinme_tarihi (DATE)
- fiyat (REAL)
- koku_notalari (TEXT)
- sezon_onerisi (TEXT)
- durum_onerisi (TEXT)
- aciklama (TEXT)
- sise_foto_yolu (TEXT)

### Markalar Tablosu
- marka_id (PRIMARY KEY)
- ad (TEXT)
- kurulus_yili (INTEGER)
- ulke (TEXT)

### Parfüm Türleri Tablosu
- tur_id (PRIMARY KEY)
- ad (TEXT)
- konsantrasyon_araligi (TEXT)

DB Browser for SQLite aracı, veritabanı tasarımı ve test aşamalarında büyük kolaylıklar sağlamıştır. Veritabanı yapısını görsel olarak incelemek, SQL sorgularını test etmek ve verileri manuel olarak görüntülemek için kullanılmıştır.

## Kullanım

1. Uygulama başlatıldığında, mevcut parfümlerin listesi görüntülenir
2. Yeni parfüm eklemek için "EKLE" butonunu kullanın
3. Mevcut bir parfümü düzenlemek için listeden seçin ve "GÜNCELLE" butonunu kullanın
4. Parfüm aramak için üst kısımdaki arama kutusunu kullanın

## Uygulama Geliştirme Süreci

### Arayüz Tasarımı
Bu uygulamanın arayüzü, Qt Designer kullanılarak tasarlanmıştır. Qt Designer, PyQt uygulamaları için görsel bir arayüz tasarlama aracıdır. Uygulamanın arayüzünü oluşturmak için şu adımlar izlenmiştir:

1. Ana pencere (main_window.ui) ve form arayüzü (parfum_form.ui) Qt Designer ile tasarlanmıştır
2. UI dosyaları, Python kodunda `uic.loadUi()` fonksiyonu kullanılarak yüklenmiştir
3. Tasarımdan sonra, oluşturulan arayüze işlevsellik eklemek için PyQt5 kütüphanesi kullanılmıştır

Bu yaklaşım, arayüz tasarımını koddan ayırarak geliştirme sürecini daha verimli hale getirmiştir.

### Veritabanı Geliştirme
Veritabanı geliştirme süreci şu adımları içermiştir:

1. Veritabanı şeması DB Browser for SQLite kullanılarak tasarlanmıştır
2. Tablolar ve ilişkiler oluşturulmuştur
3. Python kodunda SQLite bağlantısı kurularak veritabanı işlemleri gerçekleştirilmiştir
4. Geliştirme aşamasında, DB Browser for SQLite aracı ile veritabanı yapısı ve veriler kontrol edilmiştir

## Lisans

Bu proje açık kaynaklıdır ve eğitim amaçlı olarak kullanılabilir. 