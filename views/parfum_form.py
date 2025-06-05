import os
from PyQt5.QtWidgets import (QWidget, QFormLayout, QLineEdit, QDateEdit, 
                            QDoubleSpinBox, QTextEdit, QComboBox, QPushButton,
                            QHBoxLayout, QLabel, QFileDialog)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from datetime import date
from models.parfum_model import Parfum
from utils.style_utils import create_form_label

class ParfumForm(QWidget):
    """Parfüm verilerini düzenleme formu"""
    
    form_cleared = pyqtSignal()  # Form temizlendiğinde sinyal gönder
    
    def __init__(self, parfum_controller):
        super(ParfumForm, self).__init__()
        
        self.parfum_controller = parfum_controller
        self.current_parfum_id = None
        
        # UI dosyasını yükle
        uic.loadUi('views/parfum_form.ui', self)
        
        # Fotoğraf seçme düğmesine işlevsellik ekle
        self.fotoBrowseButton.clicked.connect(self.browse_image)
        
        # Fotoğraf yolu değiştiğinde önizlemeyi güncelle
        self.fotoPathLineEdit.textChanged.connect(self.update_foto_preview)
        
        # Comboboxları doldur
        self.load_comboboxes()
    
    def load_comboboxes(self):
        """Comboboxları doldurur"""
        # Markaları yükle
        self.markaComboBox.clear()
        self.markaComboBox.addItem("")  # Boş seçenek
        
        for marka in self.parfum_controller.get_all_markalar():
            self.markaComboBox.addItem(marka.ad)
        
        # Türleri yükle
        self.turComboBox.clear()
        self.turComboBox.addItem("")  # Boş seçenek
        
        for tur in self.parfum_controller.get_all_turler():
            self.turComboBox.addItem(tur.ad)
            
        # Sezon ve durum combobox'larını doldur
        if self.sezonComboBox.count() == 0:
            self.sezonComboBox.addItems(["", "İlkbahar", "Yaz", "Sonbahar", "Kış", "Tüm Sezonlar"])
            
        if self.durumComboBox.count() == 0:
            self.durumComboBox.addItems(["", "Gündüz", "Gece", "İş", "Özel Günler", "Günlük"])
    
    def browse_image(self):
        """Şişe fotoğrafı için dosya seçme dialog'u açar"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Şişe Fotoğrafı Seç", "", "Resim Dosyaları (*.png *.jpg *.jpeg)"
        )
        
        if file_path:
            self.fotoPathLineEdit.setText(file_path)
    
    def update_foto_preview(self):
        """Seçilen fotoğrafı önizleme alanında gösterir"""
        foto_path = self.fotoPathLineEdit.text()
        
        if foto_path and os.path.exists(foto_path):
            pixmap = QPixmap(foto_path)
            if not pixmap.isNull():
                # Resmi orantılı olarak yeniden boyutlandır
                pixmap = pixmap.scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.foto_preview.setPixmap(pixmap)
            else:
                self.foto_preview.setText("Görsel yüklenemedi")
        else:
            self.foto_preview.setText("Fotoğraf yok")
            self.foto_preview.setPixmap(QPixmap())  # Pixmap'i temizle
    
    def load_parfum(self, parfum):
        """Parfüm nesnesinden form alanlarını doldurur"""
        if not parfum:
            self.clear_form()
            return
            
        self.current_parfum_id = parfum.parfum_id
        
        # Form alanlarını doldur
        self.adLineEdit.setText(parfum.ad)
        
        # Marka ayarla
        index = self.markaComboBox.findText(parfum.marka_adi if hasattr(parfum, 'marka_adi') else "")
        if index >= 0:
            self.markaComboBox.setCurrentIndex(index)
        
        # Tür ayarla
        index = self.turComboBox.findText(parfum.tur_adi if hasattr(parfum, 'tur_adi') else "")
        if index >= 0:
            self.turComboBox.setCurrentIndex(index)
        
        # Diğer alanları doldur
        self.boyutSpinBox.setValue(parfum.boyut_ml if parfum.boyut_ml else 0)
        self.kalanMiktarSpinBox.setValue(parfum.kalan_miktar_ml if parfum.kalan_miktar_ml else 0)
        
        # Tarih alanını doldur
        if parfum.edinme_tarihi:
            try:
                self.tarihDateEdit.setDate(date.fromisoformat(parfum.edinme_tarihi))
            except (ValueError, TypeError):
                self.tarihDateEdit.setDate(date.today())
        
        self.fiyatSpinBox.setValue(parfum.fiyat if parfum.fiyat else 0)
        self.kokuNotlariTextEdit.setPlainText(parfum.koku_notalari if parfum.koku_notalari else "")
        
        # Sezon ayarla
        index = self.sezonComboBox.findText(parfum.sezon_onerisi if parfum.sezon_onerisi else "")
        if index >= 0:
            self.sezonComboBox.setCurrentIndex(index)
        
        # Durum ayarla
        index = self.durumComboBox.findText(parfum.durum_onerisi if parfum.durum_onerisi else "")
        if index >= 0:
            self.durumComboBox.setCurrentIndex(index)
        
        self.aciklamaTextEdit.setPlainText(parfum.aciklama if parfum.aciklama else "")
        self.fotoPathLineEdit.setText(parfum.sise_foto_yolu if parfum.sise_foto_yolu else "")
        
        # Fotoğraf önizlemeyi güncelle
        self.update_foto_preview()
    
    def get_parfum_from_form(self):
        """Form alanlarından Parfüm nesnesi oluşturur"""
        parfum = Parfum()
        parfum.parfum_id = self.current_parfum_id
        parfum.ad = self.adLineEdit.text()
        
        # Marka ve tür ID'lerini ayarla
        marka_adi = self.markaComboBox.currentText()
        parfum.marka_id = self.parfum_controller.get_marka_id(marka_adi) if marka_adi else None
        
        tur_adi = self.turComboBox.currentText()
        parfum.tur_id = self.parfum_controller.get_tur_id(tur_adi) if tur_adi else None
        
        # Diğer alanları ayarla
        parfum.boyut_ml = self.boyutSpinBox.value()
        parfum.kalan_miktar_ml = self.kalanMiktarSpinBox.value()
        parfum.edinme_tarihi = self.tarihDateEdit.date().toString("yyyy-MM-dd")
        parfum.fiyat = self.fiyatSpinBox.value()
        parfum.koku_notalari = self.kokuNotlariTextEdit.toPlainText()
        parfum.sezon_onerisi = self.sezonComboBox.currentText()
        parfum.durum_onerisi = self.durumComboBox.currentText()
        parfum.aciklama = self.aciklamaTextEdit.toPlainText()
        parfum.sise_foto_yolu = self.fotoPathLineEdit.text()
        
        return parfum
    
    def clear_form(self):
        """Form alanlarını temizler"""
        self.current_parfum_id = None
        
        # Alanları temizle
        self.adLineEdit.clear()
        self.boyutSpinBox.setValue(0)
        self.kalanMiktarSpinBox.setValue(0)
        self.tarihDateEdit.setDate(date.today())
        self.fiyatSpinBox.setValue(0)
        self.kokuNotlariTextEdit.clear()
        self.aciklamaTextEdit.clear()
        self.fotoPathLineEdit.clear()
        
        # ComboBox'ları sıfırla
        if self.markaComboBox.count() > 0:
            self.markaComboBox.setCurrentIndex(0)
        if self.turComboBox.count() > 0:
            self.turComboBox.setCurrentIndex(0)
        if self.sezonComboBox.count() > 0:
            self.sezonComboBox.setCurrentIndex(0)
        if self.durumComboBox.count() > 0:
            self.durumComboBox.setCurrentIndex(0)
        
        # Fotoğraf önizlemeyi temizle
        self.foto_preview.setText("Fotoğraf yok")
        self.foto_preview.setPixmap(QPixmap())
        
        # Sinyal gönder
        self.form_cleared.emit() 