class Marka:
    """Marka modeli - parfüm markalarını temsil eder"""
    
    def __init__(self, marka_id=None, ad="", kurulus_yili=None, ulke=""):
        self.marka_id = marka_id
        self.ad = ad
        self.kurulus_yili = kurulus_yili
        self.ulke = ulke
    
    @classmethod
    def from_db_row(cls, row):
        """Veritabanı satırından Marka nesnesi oluşturur"""
        if not row:
            return None
            
        return cls(
            marka_id=row[0],
            ad=row[1],
            kurulus_yili=row[2] if len(row) > 2 else None,
            ulke=row[3] if len(row) > 3 else ""
        )
    
    def to_tuple(self):
        """INSERT sorgusu için tuple formatına dönüştürür"""
        return (self.ad, self.kurulus_yili, self.ulke)
    
    def to_update_tuple(self):
        """UPDATE sorgusu için tuple formatına dönüştürür"""
        return (self.ad, self.kurulus_yili, self.ulke, self.marka_id)
    
    def __str__(self):
        return self.ad 