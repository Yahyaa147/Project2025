from PyQt5.QtWidgets import QMessageBox
from models.parfum_model import Parfum
from datetime import date

class ParfumController:
    """Parfüm işlemleri için kontrolcü sınıfı"""
    
    def __init__(self, db_controller):
        """Veritabanı kontrolcüsünü alır"""
        self.db = db_controller
    
    def get_all_parfumler(self, kullanici_id=None):
        """Tüm parfümleri getirir, kullanıcı ID'si belirtilirse sadece o kullanıcının parfümlerini getirir"""
        return self.db.get_parfumler_with_details(kullanici_id)
    
    def get_parfum(self, parfum_id):
        """ID'ye göre parfüm getirir"""
        return self.db.get_parfum_by_id(parfum_id)
    
    def search_parfumler(self, arama_metni, kullanici_id=None):
        """Parfümleri arar, kullanıcı ID'si belirtilirse sadece o kullanıcının parfümlerini getirir"""
        if not arama_metni.strip():
            return self.get_all_parfumler(kullanici_id)
        return self.db.search_parfumler(arama_metni, kullanici_id)
    
    def add_parfum(self, parent_view, formdan_parfum_getiren_fonksiyon, kullanici_id=None):
        """Parfüm ekler, kullanıcı ID'si belirtilirse o kullanıcıya ait olarak ekler"""
        try:
            # Form verilerini al
            parfum = formdan_parfum_getiren_fonksiyon()
            
            # Validasyon
            if not parfum.ad:
                QMessageBox.warning(parent_view, "Hata", "Parfüm adı boş olamaz!")
                return False
            
            # Veritabanına ekle
            parfum_id = self.db.add_parfum(parfum, kullanici_id)
            
            if parfum_id:
                QMessageBox.information(parent_view, "Başarılı", "Parfüm başarıyla eklendi!")
                return True
            else:
                QMessageBox.warning(parent_view, "Hata", "Parfüm eklenemedi!")
                return False
                
        except Exception as e:
            QMessageBox.critical(parent_view, "Hata", f"Parfüm eklenirken bir hata oluştu: {str(e)}")
            return False
    
    def update_parfum(self, parent_view, parfum_id, formdan_parfum_getiren_fonksiyon):
        """Parfüm günceller"""
        try:
            # Parfümü kontrol et
            mevcut_parfum = self.db.get_parfum_by_id(parfum_id)
            if not mevcut_parfum:
                QMessageBox.warning(parent_view, "Hata", "Güncellenecek parfüm bulunamadı!")
                return False
            
            # Form verilerini al
            parfum = formdan_parfum_getiren_fonksiyon()
            parfum.parfum_id = parfum_id  # ID'yi ayarla
            
            # Validasyon
            if not parfum.ad:
                QMessageBox.warning(parent_view, "Hata", "Parfüm adı boş olamaz!")
                return False
            
            # Veritabanında güncelle
            if self.db.update_parfum(parfum):
                QMessageBox.information(parent_view, "Başarılı", "Parfüm başarıyla güncellendi!")
                return True
            else:
                QMessageBox.warning(parent_view, "Hata", "Parfüm güncellenemedi!")
                return False
                
        except Exception as e:
            QMessageBox.critical(parent_view, "Hata", f"Parfüm güncellenirken bir hata oluştu: {str(e)}")
            return False
    
    def delete_parfum(self, parent_view, parfum_id, parfum_adi):
        """Parfüm siler"""
        try:
            # Kullanıcı onayı al
            onay = QMessageBox.question(
                parent_view, 
                "Onay", 
                f"{parfum_adi} parfümünü silmek istediğinize emin misiniz?", 
                QMessageBox.Yes | QMessageBox.No
            )
            
            if onay != QMessageBox.Yes:
                return False
            
            # Parfümü sil
            if self.db.delete_parfum(parfum_id):
                QMessageBox.information(parent_view, "Başarılı", "Parfüm başarıyla silindi!")
                return True
            else:
                QMessageBox.warning(parent_view, "Hata", "Parfüm silinemedi!")
                return False
                
        except Exception as e:
            QMessageBox.critical(parent_view, "Hata", f"Parfüm silinirken bir hata oluştu: {str(e)}")
            return False
    
    def get_all_markalar(self):
        """Tüm markaları getirir"""
        return self.db.get_all_markalar()
    
    def get_all_turler(self):
        """Tüm türleri getirir"""
        return self.db.get_all_turler()
    
    def get_marka_id(self, marka_adi):
        """Marka adından ID getirir"""
        return self.db.get_marka_id_by_name(marka_adi)
    
    def get_tur_id(self, tur_adi):
        """Tür adından ID getirir"""
        return self.db.get_tur_id_by_name(tur_adi) 