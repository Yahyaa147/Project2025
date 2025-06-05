class ParfumTuru:
    """Parfüm Türü modeli - parfüm türlerini temsil eder"""
    
    def __init__(self, tur_id=None, ad="", konsantrasyon_araligi=""):
        self.tur_id = tur_id
        self.ad = ad
        self.konsantrasyon_araligi = konsantrasyon_araligi
    
    @classmethod
    def from_db_row(cls, row):
        """Veritabanı satırından ParfumTuru nesnesi oluşturur"""
        if not row:
            return None
            
        return cls(
            tur_id=row[0],
            ad=row[1],
            konsantrasyon_araligi=row[2] if len(row) > 2 else ""
        )
    
    def to_tuple(self):
        """INSERT sorgusu için tuple formatına dönüştürür"""
        return (self.ad, self.konsantrasyon_araligi)
    
    def to_update_tuple(self):
        """UPDATE sorgusu için tuple formatına dönüştürür"""
        return (self.ad, self.konsantrasyon_araligi, self.tur_id)
    
    def __str__(self):
        return self.ad 