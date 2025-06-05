from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QWidget, QSplitter, QScrollArea, 
                            QFrame, QTableView, QHeaderView)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5 import uic

from views.parfum_form import ParfumForm
from controllers.parfum_controller import ParfumController
from utils.style_utils import (apply_stylesheet, create_custom_button, 
                              create_title_label, setup_table_view)

class MainWindow(QMainWindow):
    """Ana uygulama penceresi"""
    
    def __init__(self, db_controller, user_info=None):
        super(MainWindow, self).__init__()
        
        # Kullanıcı bilgilerini sakla
        self.user_info = user_info or {}
        # Kullanıcı ID'sini al
        self.kullanici_id = self.user_info.get('kullanici_id') if self.user_info else None
        
        # Kontrolcüleri oluştur
        self.parfum_controller = ParfumController(db_controller)
        
        # UI dosyasını yükle
        uic.loadUi('views/main_window.ui', self)
        
        # Form oluştur ve scroll area içine yerleştir
        self.parfum_form = ParfumForm(self.parfum_controller)
        self.formScrollArea.setWidget(self.parfum_form)
        
        # Butonlara işlevsellik ekle
        self.ekleButton.clicked.connect(self.parfum_ekle)
        self.guncelleButton.clicked.connect(self.parfum_guncelle)
        self.silButton.clicked.connect(self.parfum_sil)
        self.temizleButton.clicked.connect(self.parfum_form.clear_form)
        self.yenileButton.clicked.connect(self.load_parfumler)
        self.aramaLineEdit.textChanged.connect(self.parfumleri_filtrele)
        
        # Tabloyu ayarla
        self.parfumTableView = setup_table_view(self.parfumTableView)
        self.parfumTableView.doubleClicked.connect(self.parfum_sec)
        
        # Kullanıcı adını pencere başlığına ekle
        if self.user_info and 'kullanici_adi' in self.user_info:
            self.setWindowTitle(f"Parfüm Koleksiyonu - {self.user_info['kullanici_adi']}")
        
        # Parfüm verisini yükle
        self.load_parfumler()
    
    def load_parfumler(self):
        """Parfümleri tabloya yükler"""
        try:
            # Parfümleri al (kullanıcıya özel)
            parfumler = self.parfum_controller.get_all_parfumler(self.kullanici_id)
            
            # Tablo modelini oluştur
            model = QStandardItemModel()
            
            # Tablo başlıklarını ayarla
            headers = ["ID", "Parfüm Adı", "Marka", "Tür", "Boyut (ml)", "Kalan (ml)", 
                      "Edinme Tarihi", "Fiyat", "Koku Notları", "Sezon", "Durum", "Açıklama"]
            model.setHorizontalHeaderLabels(headers)
            
            # Verileri modele ekle
            for parfum in parfumler:
                row = []
                # ID
                row.append(QStandardItem(str(parfum.parfum_id)))
                # Ad
                row.append(QStandardItem(parfum.ad))
                # Marka
                row.append(QStandardItem(parfum.marka_adi if hasattr(parfum, 'marka_adi') else ""))
                # Tür
                row.append(QStandardItem(parfum.tur_adi if hasattr(parfum, 'tur_adi') else ""))
                # Boyut
                row.append(QStandardItem(str(parfum.boyut_ml) if parfum.boyut_ml else ""))
                # Kalan Miktar
                row.append(QStandardItem(str(parfum.kalan_miktar_ml) if parfum.kalan_miktar_ml else ""))
                # Edinme Tarihi
                row.append(QStandardItem(parfum.edinme_tarihi if parfum.edinme_tarihi else ""))
                # Fiyat
                row.append(QStandardItem(str(parfum.fiyat) if parfum.fiyat else ""))
                # Koku Notaları
                row.append(QStandardItem(parfum.koku_notalari if parfum.koku_notalari else ""))
                # Sezon Önerisi
                row.append(QStandardItem(parfum.sezon_onerisi if parfum.sezon_onerisi else ""))
                # Durum Önerisi
                row.append(QStandardItem(parfum.durum_onerisi if parfum.durum_onerisi else ""))
                # Açıklama
                row.append(QStandardItem(parfum.aciklama if parfum.aciklama else ""))
                
                model.appendRow(row)
            
            # Tabloyu modele bağla
            self.parfumTableView.setModel(model)
            
            # ID kolonunu gizle
            self.parfumTableView.hideColumn(0)
            
            # Sütun genişliklerini ayarla
            self.parfumTableView.resizeColumnsToContents()
            
        except Exception as e:
            print(f"Parfüm tablosu yükleme hatası: {e}")
    
    def parfumleri_filtrele(self):
        """Arama kutusuna yazılan metne göre parfümleri filtreler"""
        try:
            arama_metni = self.aramaLineEdit.text().strip()
            
            # Parfümleri ara (kullanıcıya özel)
            parfumler = self.parfum_controller.search_parfumler(arama_metni, self.kullanici_id)
            
            # Tablo modelini oluştur
            model = QStandardItemModel()
            
            # Tablo başlıklarını ayarla
            headers = ["ID", "Parfüm Adı", "Marka", "Tür", "Boyut (ml)", "Kalan (ml)", 
                      "Edinme Tarihi", "Fiyat", "Koku Notları", "Sezon", "Durum", "Açıklama"]
            model.setHorizontalHeaderLabels(headers)
            
            # Verileri modele ekle
            for parfum in parfumler:
                row = []
                # ID
                row.append(QStandardItem(str(parfum.parfum_id)))
                # Ad
                row.append(QStandardItem(parfum.ad))
                # Marka
                row.append(QStandardItem(parfum.marka_adi if hasattr(parfum, 'marka_adi') else ""))
                # Tür
                row.append(QStandardItem(parfum.tur_adi if hasattr(parfum, 'tur_adi') else ""))
                # Boyut
                row.append(QStandardItem(str(parfum.boyut_ml) if parfum.boyut_ml else ""))
                # Kalan Miktar
                row.append(QStandardItem(str(parfum.kalan_miktar_ml) if parfum.kalan_miktar_ml else ""))
                # Edinme Tarihi
                row.append(QStandardItem(parfum.edinme_tarihi if parfum.edinme_tarihi else ""))
                # Fiyat
                row.append(QStandardItem(str(parfum.fiyat) if parfum.fiyat else ""))
                # Koku Notaları
                row.append(QStandardItem(parfum.koku_notalari if parfum.koku_notalari else ""))
                # Sezon Önerisi
                row.append(QStandardItem(parfum.sezon_onerisi if parfum.sezon_onerisi else ""))
                # Durum Önerisi
                row.append(QStandardItem(parfum.durum_onerisi if parfum.durum_onerisi else ""))
                # Açıklama
                row.append(QStandardItem(parfum.aciklama if parfum.aciklama else ""))
                
                model.appendRow(row)
            
            # Tabloyu modele bağla
            self.parfumTableView.setModel(model)
            
            # ID kolonunu gizle
            self.parfumTableView.hideColumn(0)
            
            # Sütun genişliklerini ayarla
            self.parfumTableView.resizeColumnsToContents()
            
        except Exception as e:
            print(f"Parfüm filtreleme hatası: {e}")
    
    def parfum_sec(self):
        """Tabloda seçilen parfümün bilgilerini form alanlarına yükler"""
        try:
            # Seçili satırı kontrol et
            selected_row = self.parfumTableView.currentIndex().row()
            if selected_row < 0:
                return
            
            # Seçili parfümün ID'sini al
            model = self.parfumTableView.model()
            parfum_id = int(model.index(selected_row, 0).data())
            
            # Parfümü al ve forma yükle
            parfum = self.parfum_controller.get_parfum(parfum_id)
            self.parfum_form.load_parfum(parfum)
            
        except Exception as e:
            print(f"Parfüm seçme hatası: {e}")
    
    def parfum_ekle(self):
        """Formdaki bilgilerle yeni bir parfüm ekler"""
        # Kontrolcüye parfüm ekleme işlemini gerçekleştirmesini söyle
        self.parfum_controller.add_parfum(self, self.parfum_form.get_parfum_from_form, self.kullanici_id)
        
        # Formu temizle ve tabloyu yenile
        self.parfum_form.clear_form()
        self.load_parfumler()
    
    def parfum_guncelle(self):
        """Formdaki bilgilerle seçili parfümü günceller"""
        # Seçili parfüm ID'sini kontrol et
        if not self.parfum_form.current_parfum_id:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Hata", "Lütfen güncellenecek bir parfüm seçin!")
            return
        
        # Kontrolcüye parfüm güncelleme işlemini gerçekleştirmesini söyle
        if self.parfum_controller.update_parfum(self, self.parfum_form.current_parfum_id, 
                                              self.parfum_form.get_parfum_from_form):
            # Tabloyu yenile
            self.load_parfumler()
    
    def parfum_sil(self):
        """Seçili parfümü siler"""
        # Seçili parfüm ID'sini kontrol et
        if not self.parfum_form.current_parfum_id:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Hata", "Lütfen silinecek bir parfüm seçin!")
            return
        
        # Parfüm adını al
        parfum_adi = self.parfum_form.parfumAdiEdit.text()
        
        # Kontrolcüye parfüm silme işlemini gerçekleştirmesini söyle
        if self.parfum_controller.delete_parfum(self, self.parfum_form.current_parfum_id, parfum_adi):
            # Formu temizle ve tabloyu yenile
            self.parfum_form.clear_form()
            self.load_parfumler() 