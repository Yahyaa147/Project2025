class Parfum:
    """Parfüm modeli - parfüm verilerini temsil eder"""
    
    def __init__(self, parfum_id=None, ad="", marka_id=None, tur_id=None, 
                 boyut_ml=0, kalan_miktar_ml=0, edinme_tarihi=None, fiyat=0,
                 koku_notalari="", sezon_onerisi="", durum_onerisi="", 
                 aciklama="", sise_foto_yolu=""):
        self.parfum_id = parfum_id
        self.ad = ad
        self.marka_id = marka_id
        self.tur_id = tur_id
        self.boyut_ml = boyut_ml
        self.kalan_miktar_ml = kalan_miktar_ml
        self.edinme_tarihi = edinme_tarihi
        self.fiyat = fiyat
        self.koku_notalari = koku_notalari
        self.sezon_onerisi = sezon_onerisi
        self.durum_onerisi = durum_onerisi
        self.aciklama = aciklama
        self.sise_foto_yolu = sise_foto_yolu
    
    @classmethod
    def from_db_row(cls, row):
        """Veritabanı satırından Parfüm nesnesi oluşturur"""
        if not row:
            return None
            
        return cls(
            parfum_id=row[0],
            ad=row[1],
            marka_id=row[2],
            tur_id=row[3],
            boyut_ml=row[4],
            kalan_miktar_ml=row[5],
            edinme_tarihi=row[6],
            fiyat=row[7],
            koku_notalari=row[8],
            sezon_onerisi=row[9],
            durum_onerisi=row[10],
            aciklama=row[11],
            sise_foto_yolu=row[12] if len(row) > 12 else ""
        )
    
    def to_tuple(self):
        """INSERT sorgusu için tuple formatına dönüştürür"""
        return (
            self.ad, self.marka_id, self.tur_id, self.boyut_ml,
            self.kalan_miktar_ml, self.edinme_tarihi, self.fiyat,
            self.koku_notalari, self.sezon_onerisi, self.durum_onerisi,
            self.aciklama, self.sise_foto_yolu
        )
    
    def to_update_tuple(self):
        """UPDATE sorgusu için tuple formatına dönüştürür"""
        return (
            self.ad, self.marka_id, self.tur_id, self.boyut_ml,
            self.kalan_miktar_ml, self.edinme_tarihi, self.fiyat,
            self.koku_notalari, self.sezon_onerisi, self.durum_onerisi,
            self.aciklama, self.sise_foto_yolu, self.parfum_id
        ) 