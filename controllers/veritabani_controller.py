import sqlite3
from models.parfum_model import Parfum
from models.marka_model import Marka
from models.tur_model import ParfumTuru

class VeritabaniController:
    """
    Veritabanı işlemleri için kontrolcü sınıfı
    
    Bu sınıf, SQLite veritabanı ile iletişim kurar ve veri işlemlerini yönetir.
    Veritabanı şeması, DB Browser for SQLite aracı kullanılarak tasarlanmış ve test edilmiştir.
    Tablo yapıları ve ilişkileri, DB Browser for SQLite ile görsel olarak incelenmiştir.
    """
    
    def __init__(self, db_file):
        """Veritabanı bağlantısını oluşturur ve tabloları kontrol eder"""
        try:
            self.conn = sqlite3.connect(db_file)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            print("Veritabanı bağlantısı başarılı")
            
            # Tabloları oluştur
            self.create_tables()
            
            # Varsayılan veri ekle
            self.add_default_data()
            
        except sqlite3.Error as e:
            print(f"Veritabanı hatası: {e}")
            raise
    
    def __del__(self):
        """Veritabanı bağlantısını kapatır"""
        if hasattr(self, 'conn'):
            self.conn.close()
    
    def check_and_add_kullanici_id_column(self):
        """
        Parfümler tablosunda kullanici_id sütunu var mı kontrol eder,
        yoksa bu sütunu ekler
        """
        try:
            # Parfümler tablosunda kullanici_id sütununu kontrol et
            self.cursor.execute("PRAGMA table_info(Parfümler)")
            columns = self.cursor.fetchall()
            
            # Sütun isimlerini kontrol et
            column_names = [column[1] for column in columns]
            
            if 'kullanici_id' not in column_names:
                # kullanici_id sütunu yoksa ekle
                self.cursor.execute('''
                ALTER TABLE Parfümler
                ADD COLUMN kullanici_id INTEGER REFERENCES Kullanicilar(kullanici_id)
                ''')
                
                self.conn.commit()
                print("kullanici_id sütunu Parfümler tablosuna başarıyla eklendi.")
            else:
                print("kullanici_id sütunu zaten Parfümler tablosunda mevcut.")
            
        except sqlite3.Error as e:
            print(f"kullanici_id sütunu kontrolü/ekleme hatası: {e}")
    
    def create_tables(self):
        """
        Gerekli tabloları oluşturur
        
        Not: Tablo yapıları DB Browser for SQLite ile tasarlanmış ve
        uygulama içinde oluşturulmuştur.
        """
        # Kullanıcılar tablosu
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Kullanicilar (
            kullanici_id INTEGER PRIMARY KEY AUTOINCREMENT,
            kullanici_adi TEXT NOT NULL UNIQUE,
            sifre TEXT NOT NULL,
            ad_soyad TEXT,
            email TEXT,
            son_giris_tarihi DATETIME,
            kayit_tarihi DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Markalar tablosu
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Markalar (
            marka_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad TEXT NOT NULL,
            kurulus_yili INTEGER,
            ulke TEXT
        )
        ''')
        
        # Parfüm Türleri tablosu
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS "Parfüm Türleri" (
            tur_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad TEXT NOT NULL,
            konsantrasyon_araligi TEXT
        )
        ''')
        
        # Parfümler tablosu
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Parfümler (
            parfum_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad TEXT NOT NULL,
            marka_id INTEGER,
            tur_id INTEGER,
            boyut_ml REAL,
            kalan_miktar_ml REAL,
            edinme_tarihi DATE,
            fiyat REAL,
            koku_notalari TEXT,
            sezon_onerisi TEXT,
            durum_onerisi TEXT,
            aciklama TEXT,
            sise_foto_yolu TEXT,
            kullanici_id INTEGER,
            FOREIGN KEY (marka_id) REFERENCES Markalar (marka_id),
            FOREIGN KEY (tur_id) REFERENCES "Parfüm Türleri" (tur_id),
            FOREIGN KEY (kullanici_id) REFERENCES Kullanicilar (kullanici_id)
        )
        ''')
        
        self.conn.commit()
    
    def add_default_data(self):
        """Varsayılan marka, tür ve kullanıcı bilgilerini ekler"""
        try:
            # Varsayılan kullanıcı ekle
            self.cursor.execute("SELECT COUNT(*) FROM Kullanicilar")
            kullanici_sayisi = self.cursor.fetchone()[0]
            
            if kullanici_sayisi == 0:
                # Varsayılan admin kullanıcısı ekle (şifre: admin123)
                self.cursor.execute(
                    "INSERT INTO Kullanicilar (kullanici_adi, sifre, ad_soyad, email) VALUES (?, ?, ?, ?)",
                    ("admin", "admin123", "Sistem Yöneticisi", "admin@example.com")
                )
            
            # Markalar tablosunda veri var mı kontrol et
            self.cursor.execute("SELECT COUNT(*) FROM Markalar")
            marka_sayisi = self.cursor.fetchone()[0]
            
            if marka_sayisi == 0:
                # Bazı popüler parfüm markalarını ekle
                markalar = [
                    ("Chanel", 1909, "Fransa"),
                    ("Dior", 1946, "Fransa"),
                    ("Gucci", 1921, "İtalya"),
                    ("Tom Ford", 2005, "ABD"),
                    ("Yves Saint Laurent", 1961, "Fransa"),
                    ("Jo Malone", 1994, "İngiltere")
                ]
                
                self.cursor.executemany(
                    "INSERT INTO Markalar (ad, kurulus_yili, ulke) VALUES (?, ?, ?)",
                    markalar
                )
            
            # Parfüm Türleri tablosunda veri var mı kontrol et
            self.cursor.execute('SELECT COUNT(*) FROM "Parfüm Türleri"')
            tur_sayisi = self.cursor.fetchone()[0]
            
            if tur_sayisi == 0:
                # Parfüm türlerini ekle
                turler = [
                    ("Parfüm (Extrait)", "%15-40"),
                    ("Eau de Parfum", "%15-20"),
                    ("Eau de Toilette", "%5-15"),
                    ("Eau de Cologne", "%2-4"),
                    ("Eau Fraiche", "%1-3")
                ]
                
                self.cursor.executemany(
                    'INSERT INTO "Parfüm Türleri" (ad, konsantrasyon_araligi) VALUES (?, ?)',
                    turler
                )
            
            self.conn.commit()
            
        except sqlite3.Error as e:
            print(f"Varsayılan veri ekleme hatası: {e}")
    
    # ----- Kullanıcı İşlemleri -----
    
    def kullanici_kontrol(self, kullanici_adi, sifre):
        """Kullanıcı adı ve şifre kontrolü yapar, doğruysa kullanıcı bilgilerini döndürür"""
        try:
            self.cursor.execute(
                "SELECT kullanici_id, kullanici_adi, ad_soyad, email FROM Kullanicilar WHERE kullanici_adi = ? AND sifre = ?",
                (kullanici_adi, sifre)
            )
            
            kullanici = self.cursor.fetchone()
            
            if kullanici:
                # Son giriş tarihini güncelle
                self.cursor.execute(
                    "UPDATE Kullanicilar SET son_giris_tarihi = CURRENT_TIMESTAMP WHERE kullanici_id = ?",
                    (kullanici[0],)
                )
                self.conn.commit()
                
                return dict(kullanici)
            else:
                return None
                
        except sqlite3.Error as e:
            print(f"Kullanıcı kontrol hatası: {e}")
            return None
    
    def kullanici_ekle(self, kullanici_adi, sifre, ad_soyad="", email=""):
        """Yeni kullanıcı ekler"""
        try:
            # Kullanıcı adı mevcut mu kontrol et
            self.cursor.execute(
                "SELECT COUNT(*) FROM Kullanicilar WHERE kullanici_adi = ?",
                (kullanici_adi,)
            )
            
            if self.cursor.fetchone()[0] > 0:
                return False, "Bu kullanıcı adı zaten kullanılıyor."
            
            # Yeni kullanıcı ekle
            self.cursor.execute(
                "INSERT INTO Kullanicilar (kullanici_adi, sifre, ad_soyad, email) VALUES (?, ?, ?, ?)",
                (kullanici_adi, sifre, ad_soyad, email)
            )
            
            self.conn.commit()
            return True, "Kullanıcı başarıyla eklendi."
            
        except sqlite3.Error as e:
            print(f"Kullanıcı ekleme hatası: {e}")
            return False, f"Veritabanı hatası: {e}"
    
    # ----- Parfüm İşlemleri -----
    
    def get_all_parfumler(self, kullanici_id=None):
        """Tüm parfümleri getirir, kullanıcı ID'si belirtilirse sadece o kullanıcının parfümlerini getirir"""
        try:
            if kullanici_id:
                self.cursor.execute('''
                SELECT p.parfum_id, p.ad, p.marka_id, p.tur_id, p.boyut_ml, p.kalan_miktar_ml, 
                       p.edinme_tarihi, p.fiyat, p.koku_notalari, p.sezon_onerisi, 
                       p.durum_onerisi, p.aciklama, p.sise_foto_yolu
                FROM Parfümler p
                WHERE p.kullanici_id = ?
                ORDER BY p.ad
                ''', (kullanici_id,))
            else:
                self.cursor.execute('''
                SELECT p.parfum_id, p.ad, p.marka_id, p.tur_id, p.boyut_ml, p.kalan_miktar_ml, 
                       p.edinme_tarihi, p.fiyat, p.koku_notalari, p.sezon_onerisi, 
                       p.durum_onerisi, p.aciklama, p.sise_foto_yolu
                FROM Parfümler p
                ORDER BY p.ad
                ''')
            
            return [Parfum.from_db_row(row) for row in self.cursor.fetchall()]
            
        except sqlite3.Error as e:
            print(f"Parfüm verisi alma hatası: {e}")
            return []
    
    def get_parfumler_with_details(self, kullanici_id=None):
        """Marka ve tür adlarıyla birlikte tüm parfümleri getirir"""
        try:
            if kullanici_id:
                # Kullanıcıya özel filtreleme
                self.cursor.execute('''
                SELECT p.parfum_id, p.ad, p.marka_id, p.tur_id, p.boyut_ml, p.kalan_miktar_ml, 
                       p.edinme_tarihi, p.fiyat, p.koku_notalari, p.sezon_onerisi, 
                       p.durum_onerisi, p.aciklama, p.sise_foto_yolu,
                       m.ad as marka_adi, t.ad as tur_adi
                FROM Parfümler p
                LEFT JOIN Markalar m ON p.marka_id = m.marka_id
                LEFT JOIN "Parfüm Türleri" t ON p.tur_id = t.tur_id
                WHERE p.kullanici_id = ?
                ORDER BY p.ad
                ''', (kullanici_id,))
            else:
                # Tüm parfümleri getir
                self.cursor.execute('''
                SELECT p.parfum_id, p.ad, p.marka_id, p.tur_id, p.boyut_ml, p.kalan_miktar_ml, 
                       p.edinme_tarihi, p.fiyat, p.koku_notalari, p.sezon_onerisi, 
                       p.durum_onerisi, p.aciklama, p.sise_foto_yolu,
                       m.ad as marka_adi, t.ad as tur_adi
                FROM Parfümler p
                LEFT JOIN Markalar m ON p.marka_id = m.marka_id
                LEFT JOIN "Parfüm Türleri" t ON p.tur_id = t.tur_id
                ORDER BY p.ad
                ''')
            
            rows = self.cursor.fetchall()
            result = []
            
            for row in rows:
                parfum = Parfum.from_db_row(row)
                # Detay alanlarını ekle
                parfum.marka_adi = row[13] if row[13] else ""
                parfum.tur_adi = row[14] if row[14] else ""
                result.append(parfum)
                
            return result
            
        except sqlite3.Error as e:
            print(f"Parfüm detaylarını alma hatası: {e}")
            return []
    
    def get_parfum_by_id(self, parfum_id):
        """ID'ye göre parfüm getirir"""
        try:
            self.cursor.execute('''
            SELECT p.parfum_id, p.ad, p.marka_id, p.tur_id, p.boyut_ml, p.kalan_miktar_ml, 
                   p.edinme_tarihi, p.fiyat, p.koku_notalari, p.sezon_onerisi, 
                   p.durum_onerisi, p.aciklama, p.sise_foto_yolu
            FROM Parfümler p
            WHERE p.parfum_id = ?
            ''', (parfum_id,))
            
            row = self.cursor.fetchone()
            return Parfum.from_db_row(row) if row else None
            
        except sqlite3.Error as e:
            print(f"Parfüm detayı alma hatası: {e}")
            return None
    
    def add_parfum(self, parfum, kullanici_id=None):
        """Yeni parfüm ekler"""
        try:
            if kullanici_id:
                # Kullanıcı bilgisiyle ekle
                self.cursor.execute('''
                INSERT INTO Parfümler (ad, marka_id, tur_id, boyut_ml, kalan_miktar_ml,
                                      edinme_tarihi, fiyat, koku_notalari, sezon_onerisi,
                                      durum_onerisi, aciklama, sise_foto_yolu, kullanici_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', parfum.to_tuple() + (kullanici_id,))
            else:
                # Kullanıcı bilgisi olmadan ekle
                self.cursor.execute('''
                INSERT INTO Parfümler (ad, marka_id, tur_id, boyut_ml, kalan_miktar_ml,
                                      edinme_tarihi, fiyat, koku_notalari, sezon_onerisi,
                                      durum_onerisi, aciklama, sise_foto_yolu)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', parfum.to_tuple())
            
            self.conn.commit()
            return self.cursor.lastrowid
            
        except sqlite3.Error as e:
            print(f"Parfüm ekleme hatası: {e}")
            return None
    
    def update_parfum(self, parfum):
        """Mevcut parfümü günceller"""
        try:
            self.cursor.execute('''
            UPDATE Parfümler 
            SET ad = ?, marka_id = ?, tur_id = ?, boyut_ml = ?, kalan_miktar_ml = ?,
                edinme_tarihi = ?, fiyat = ?, koku_notalari = ?, sezon_onerisi = ?,
                durum_onerisi = ?, aciklama = ?, sise_foto_yolu = ?
            WHERE parfum_id = ?
            ''', parfum.to_update_tuple())
            
            self.conn.commit()
            return self.cursor.rowcount > 0
            
        except sqlite3.Error as e:
            print(f"Parfüm güncelleme hatası: {e}")
            return False
    
    def delete_parfum(self, parfum_id):
        """Parfümü siler"""
        try:
            self.cursor.execute("DELETE FROM Parfümler WHERE parfum_id = ?", (parfum_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
            
        except sqlite3.Error as e:
            print(f"Parfüm silme hatası: {e}")
            return False
    
    def search_parfumler(self, arama_metni, kullanici_id=None):
        """Parfümleri isim, marka veya koku notalarına göre arar"""
        try:
            arama_metni = f"%{arama_metni}%"
            
            if kullanici_id:
                # Kullanıcıya özel arama
                self.cursor.execute('''
                SELECT p.parfum_id, p.ad, p.marka_id, p.tur_id, p.boyut_ml, p.kalan_miktar_ml, 
                       p.edinme_tarihi, p.fiyat, p.koku_notalari, p.sezon_onerisi, 
                       p.durum_onerisi, p.aciklama, p.sise_foto_yolu,
                       m.ad as marka_adi, t.ad as tur_adi
                FROM Parfümler p
                LEFT JOIN Markalar m ON p.marka_id = m.marka_id
                LEFT JOIN "Parfüm Türleri" t ON p.tur_id = t.tur_id
                WHERE (p.ad LIKE ? OR p.koku_notalari LIKE ? OR m.ad LIKE ?) AND p.kullanici_id = ?
                ORDER BY p.ad
                ''', (arama_metni, arama_metni, arama_metni, kullanici_id))
            else:
                # Genel arama
                self.cursor.execute('''
                SELECT p.parfum_id, p.ad, p.marka_id, p.tur_id, p.boyut_ml, p.kalan_miktar_ml, 
                       p.edinme_tarihi, p.fiyat, p.koku_notalari, p.sezon_onerisi, 
                       p.durum_onerisi, p.aciklama, p.sise_foto_yolu,
                       m.ad as marka_adi, t.ad as tur_adi
                FROM Parfümler p
                LEFT JOIN Markalar m ON p.marka_id = m.marka_id
                LEFT JOIN "Parfüm Türleri" t ON p.tur_id = t.tur_id
                WHERE p.ad LIKE ? OR p.koku_notalari LIKE ? OR m.ad LIKE ?
                ORDER BY p.ad
                ''', (arama_metni, arama_metni, arama_metni))
            
            rows = self.cursor.fetchall()
            result = []
            
            for row in rows:
                parfum = Parfum.from_db_row(row)
                # Detay alanlarını ekle
                parfum.marka_adi = row[13] if row[13] else ""
                parfum.tur_adi = row[14] if row[14] else ""
                result.append(parfum)
                
            return result
            
        except sqlite3.Error as e:
            print(f"Parfüm arama hatası: {e}")
            return []
    
    # ----- Marka İşlemleri -----
    
    def get_all_markalar(self):
        """Tüm markaları getirir"""
        try:
            self.cursor.execute("SELECT marka_id, ad, kurulus_yili, ulke FROM Markalar ORDER BY ad")
            return [Marka.from_db_row(row) for row in self.cursor.fetchall()]
            
        except sqlite3.Error as e:
            print(f"Marka verisi alma hatası: {e}")
            return []
    
    def get_marka_by_id(self, marka_id):
        """ID'ye göre marka getirir"""
        try:
            self.cursor.execute("SELECT marka_id, ad, kurulus_yili, ulke FROM Markalar WHERE marka_id = ?", (marka_id,))
            row = self.cursor.fetchone()
            return Marka.from_db_row(row) if row else None
            
        except sqlite3.Error as e:
            print(f"Marka detayı alma hatası: {e}")
            return None
    
    def get_marka_id_by_name(self, marka_adi):
        """İsimden marka ID'sini bulur"""
        try:
            self.cursor.execute("SELECT marka_id FROM Markalar WHERE ad = ?", (marka_adi,))
            row = self.cursor.fetchone()
            return row[0] if row else None
            
        except sqlite3.Error as e:
            print(f"Marka ID'si alma hatası: {e}")
            return None
    
    # ----- Tür İşlemleri -----
    
    def get_all_turler(self):
        """Tüm parfüm türlerini getirir"""
        try:
            self.cursor.execute('SELECT tur_id, ad, konsantrasyon_araligi FROM "Parfüm Türleri" ORDER BY ad')
            return [ParfumTuru.from_db_row(row) for row in self.cursor.fetchall()]
            
        except sqlite3.Error as e:
            print(f"Tür verisi alma hatası: {e}")
            return []
    
    def get_tur_by_id(self, tur_id):
        """ID'ye göre tür getirir"""
        try:
            self.cursor.execute('SELECT tur_id, ad, konsantrasyon_araligi FROM "Parfüm Türleri" WHERE tur_id = ?', (tur_id,))
            row = self.cursor.fetchone()
            return ParfumTuru.from_db_row(row) if row else None
            
        except sqlite3.Error as e:
            print(f"Tür detayı alma hatası: {e}")
            return None
    
    def get_tur_id_by_name(self, tur_adi):
        """İsimden tür ID'sini bulur"""
        try:
            self.cursor.execute('SELECT tur_id FROM "Parfüm Türleri" WHERE ad = ?', (tur_adi,))
            row = self.cursor.fetchone()
            return row[0] if row else None
            
        except sqlite3.Error as e:
            print(f"Tür ID'si alma hatası: {e}")
            return None 