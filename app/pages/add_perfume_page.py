import os
import sqlite3
from datetime import date
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, 
                            QLineEdit, QTextEdit, QComboBox, QDoubleSpinBox, QDateEdit,
                            QPushButton, QFileDialog, QMessageBox, QScrollArea, QFrame)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QPixmap, QFont

class AddPerfumePage(QWidget):
    def __init__(self, conn, cursor, kullanici_id=None):
        super(AddPerfumePage, self).__init__()
        self.conn = conn
        self.cursor = cursor
        self.kullanici_id = kullanici_id
        self.editing_id = None  # Düzenleme modu için ID
        
        # Ana layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        
        # Sayfa başlığı
        self.page_header = QLabel("YENİ PARFÜM EKLE")
        self.page_header.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #3b82f6;
            margin-bottom: 10px;
            padding: 10px;
        """)
        self.page_header.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.page_header)
        
        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
        """)
        
        # Form içeriği
        form_container = QWidget()
        self.form_layout = QFormLayout(form_container)
        self.form_layout.setContentsMargins(20, 20, 20, 20)
        self.form_layout.setSpacing(15)
        self.form_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        
        # Form alanları
        # Parfüm Adı
        self.adLineEdit = QLineEdit()
        self.adLineEdit.setStyleSheet("""
            font-size: 16px;
            padding: 12px;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            min-height: 25px;
        """)
        self.form_layout.addRow(self.create_label("Parfüm Adı:"), self.adLineEdit)
        
        # Marka
        self.markaComboBox = QComboBox()
        self.markaComboBox.setStyleSheet("""
            font-size: 16px;
            padding: 12px;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            min-height: 25px;
        """)
        self.form_layout.addRow(self.create_label("Marka:"), self.markaComboBox)
        
        # Tür
        self.turComboBox = QComboBox()
        self.turComboBox.setStyleSheet("""
            font-size: 16px;
            padding: 12px;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            min-height: 25px;
        """)
        self.form_layout.addRow(self.create_label("Tür:"), self.turComboBox)
        
        # Boyut
        self.boyutSpinBox = QDoubleSpinBox()
        self.boyutSpinBox.setStyleSheet("""
            font-size: 16px;
            padding: 12px;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            min-height: 25px;
        """)
        self.boyutSpinBox.setSuffix(" ml")
        self.boyutSpinBox.setMaximum(1000.0)
        self.form_layout.addRow(self.create_label("Boyut (ml):"), self.boyutSpinBox)
        
        # Kalan Miktar
        self.kalanMiktarSpinBox = QDoubleSpinBox()
        self.kalanMiktarSpinBox.setStyleSheet("""
            font-size: 16px;
            padding: 12px;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            min-height: 25px;
        """)
        self.kalanMiktarSpinBox.setSuffix(" ml")
        self.kalanMiktarSpinBox.setMaximum(1000.0)
        self.form_layout.addRow(self.create_label("Kalan Miktar (ml):"), self.kalanMiktarSpinBox)
        
        # Edinme Tarihi
        self.tarihDateEdit = QDateEdit()
        self.tarihDateEdit.setStyleSheet("""
            font-size: 16px;
            padding: 12px;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            min-height: 25px;
        """)
        self.tarihDateEdit.setCalendarPopup(True)
        self.tarihDateEdit.setDate(date.today())
        self.form_layout.addRow(self.create_label("Edinme Tarihi:"), self.tarihDateEdit)
        
        # Fiyat
        self.fiyatSpinBox = QDoubleSpinBox()
        self.fiyatSpinBox.setStyleSheet("""
            font-size: 16px;
            padding: 12px;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            min-height: 25px;
        """)
        self.fiyatSpinBox.setSuffix(" ₺")
        self.fiyatSpinBox.setMaximum(100000.0)
        self.form_layout.addRow(self.create_label("Fiyat:"), self.fiyatSpinBox)
        
        # Koku Notaları
        self.kokuNotlariTextEdit = QTextEdit()
        self.kokuNotlariTextEdit.setStyleSheet("""
            font-size: 16px;
            padding: 12px;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            min-height: 80px;
        """)
        self.form_layout.addRow(self.create_label("Koku Notaları:"), self.kokuNotlariTextEdit)
        
        # Sezon Önerisi
        self.sezonComboBox = QComboBox()
        self.sezonComboBox.setStyleSheet("""
            font-size: 16px;
            padding: 12px;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            min-height: 25px;
        """)
        self.sezonComboBox.addItems(["", "İlkbahar", "Yaz", "Sonbahar", "Kış", "Tüm Sezonlar"])
        self.form_layout.addRow(self.create_label("Sezon Önerisi:"), self.sezonComboBox)
        
        # Durum Önerisi
        self.durumComboBox = QComboBox()
        self.durumComboBox.setStyleSheet("""
            font-size: 16px;
            padding: 12px;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            min-height: 25px;
        """)
        self.durumComboBox.addItems(["", "Gündüz", "Gece", "İş", "Özel Günler", "Günlük"])
        self.form_layout.addRow(self.create_label("Durum Önerisi:"), self.durumComboBox)
        
        # Açıklama
        self.aciklamaTextEdit = QTextEdit()
        self.aciklamaTextEdit.setStyleSheet("""
            font-size: 16px;
            padding: 12px;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            min-height: 80px;
        """)
        self.form_layout.addRow(self.create_label("Açıklama:"), self.aciklamaTextEdit)
        
        # Fotoğraf
        foto_layout = QHBoxLayout()
        
        self.fotoPathLineEdit = QLineEdit()
        self.fotoPathLineEdit.setStyleSheet("""
            font-size: 16px;
            padding: 12px;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            min-height: 25px;
        """)
        self.fotoPathLineEdit.setReadOnly(True)
        foto_layout.addWidget(self.fotoPathLineEdit)
        
        self.fotoBrowseButton = QPushButton("Gözat")
        self.fotoBrowseButton.setStyleSheet("""
            background-color: #3b82f6;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border-radius: 6px;
            padding: 12px;
            min-width: 100px;
        """)
        self.fotoBrowseButton.setCursor(Qt.PointingHandCursor)
        foto_layout.addWidget(self.fotoBrowseButton)
        
        self.form_layout.addRow(self.create_label("Şişe Fotoğrafı:"), foto_layout)
        
        # Fotoğraf önizleme
        self.foto_preview = QLabel("Fotoğraf yok")
        self.foto_preview.setStyleSheet("""
            border: 1px dashed #cbd5e1;
            background-color: #f8fafc;
            border-radius: 6px;
            padding: 10px;
        """)
        self.foto_preview.setAlignment(Qt.AlignCenter)
        self.foto_preview.setMinimumHeight(200)
        self.form_layout.addRow(self.foto_preview)
        
        # Kaydet butonu
        self.saveButton = QPushButton("Parfüm Ekle")
        self.saveButton.setStyleSheet("""
            background-color: #3b82f6;
            color: white;
            font-size: 18px;
            font-weight: bold;
            border-radius: 8px;
            padding: 12px 20px;
            min-height: 40px;
        """)
        self.saveButton.setCursor(Qt.PointingHandCursor)
        self.form_layout.addRow(self.saveButton)
        
        # Scroll area'ya form ekle
        scroll_area.setWidget(form_container)
        
        # Ana layout'a scroll area ekle
        self.main_layout.addWidget(scroll_area)
        
        # Butonlar
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(20)
        
        self.temizleButton = QPushButton("TEMİZLE")
        self.temizleButton.setStyleSheet("""
            background-color: #9ca3af;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border-radius: 6px;
            padding: 15px 20px;
            min-width: 150px;
        """)
        self.temizleButton.setCursor(Qt.PointingHandCursor)
        
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.saveButton)
        self.button_layout.addWidget(self.temizleButton)
        self.button_layout.addStretch()
        
        self.main_layout.addLayout(self.button_layout)
        
        # Bağlantıları kur
        self.setup_connections()
        
        # Markaları ve türleri yükle
        self.load_markalar()
        self.load_turler()
    
    def create_label(self, text):
        """Form etiketleri için stil"""
        label = QLabel(text)
        label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            padding-right: 15px;
            color: #334155;
        """)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        return label
    
    def setup_connections(self):
        """Buton bağlantılarını ayarlar"""
        self.saveButton.clicked.connect(self.save_perfume)
        self.temizleButton.clicked.connect(self.clear_form)
        self.fotoBrowseButton.clicked.connect(self.browse_image)
        self.fotoPathLineEdit.textChanged.connect(self.update_foto_preview)
    
    def load_markalar(self):
        """Markaları veritabanından yükler"""
        try:
            self.markaComboBox.clear()
            self.markaComboBox.addItem("")  # Boş seçenek
            
            self.cursor.execute("SELECT marka FROM markalar ORDER BY marka")
            markalar = self.cursor.fetchall()
            
            for marka in markalar:
                self.markaComboBox.addItem(marka['marka'])
        
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Veritabanı Hatası", f"Markalar yüklenirken hata oluştu: {e}")
    
    def load_turler(self):
        """Türleri veritabanından yükler"""
        try:
            self.turComboBox.clear()
            self.turComboBox.addItem("")  # Boş seçenek
            
            self.cursor.execute("SELECT tur_adi FROM turler ORDER BY tur_adi")
            turler = self.cursor.fetchall()
            
            for tur in turler:
                self.turComboBox.addItem(tur['tur_adi'])
        
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Veritabanı Hatası", f"Türler yüklenirken hata oluştu: {e}")
    
    def browse_image(self):
        """Fotoğraf seçme diyalog penceresini açar"""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Fotoğraf Seç", "", "Resim Dosyaları (*.png *.jpg *.jpeg *.bmp *.gif)", options=options
        )
        
        if file_path:
            self.fotoPathLineEdit.setText(file_path)
    
    def update_foto_preview(self):
        """Seçilen fotoğrafı önizleme alanında gösterir"""
        path = self.fotoPathLineEdit.text()
        if path and os.path.exists(path):
            pixmap = QPixmap(path)
            self.foto_preview.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.foto_preview.setText("Fotoğraf yok")
            self.foto_preview.setPixmap(QPixmap())
    
    def get_marka_id(self, marka_adi):
        """Marka adına göre ID döndürür, yoksa yeni ekler"""
        if not marka_adi:
            return None
        
        try:
            # Marka ID'sini bul
            self.cursor.execute("SELECT id FROM markalar WHERE marka = ?", (marka_adi,))
            result = self.cursor.fetchone()
            
            if result:
                return result['id']
            else:
                # Yeni marka ekle
                self.cursor.execute("INSERT INTO markalar (marka) VALUES (?)", (marka_adi,))
                self.conn.commit()
                return self.cursor.lastrowid
        
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Veritabanı Hatası", f"Marka işlenirken hata oluştu: {e}")
            return None
    
    def get_tur_id(self, tur_adi):
        """Tür adına göre ID döndürür, yoksa yeni ekler"""
        if not tur_adi:
            return None
        
        try:
            # Tür ID'sini bul
            self.cursor.execute("SELECT id FROM turler WHERE tur_adi = ?", (tur_adi,))
            result = self.cursor.fetchone()
            
            if result:
                return result['id']
            else:
                # Yeni tür ekle
                self.cursor.execute("INSERT INTO turler (tur_adi) VALUES (?)", (tur_adi,))
                self.conn.commit()
                return self.cursor.lastrowid
        
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Veritabanı Hatası", f"Tür işlenirken hata oluştu: {e}")
            return None
    
    def save_perfume(self):
        """Yeni parfüm ekler veya mevcut parfümü günceller"""
        if self.kullanici_id is None:
            QMessageBox.critical(self, "Kullanıcı Hatası", "Kullanıcı bilgisi bulunamadı. Lütfen tekrar giriş yapın.")
            return
        
        ad = self.adLineEdit.text().strip()
        marka_id = self.get_marka_id(self.markaComboBox.currentText())
        tur_id = self.get_tur_id(self.turComboBox.currentText())
        boyut = self.boyutSpinBox.value()
        kalan_miktar = self.kalanMiktarSpinBox.value()
        edinme_tarihi = self.tarihDateEdit.date().toString("yyyy-MM-dd")
        fiyat = self.fiyatSpinBox.value()
        koku_notlari = self.kokuNotlariTextEdit.toPlainText().strip()
        sezon = self.sezonComboBox.currentText().strip()
        durum = self.durumComboBox.currentText().strip()
        aciklama = self.aciklamaTextEdit.toPlainText().strip()
        foto_path = self.fotoPathLineEdit.text().strip()

        # Strong input validation
        if not ad:
            QMessageBox.warning(self, "Hata", "Parfüm adı boş olamaz!")
            return
        if not marka_id:
            QMessageBox.warning(self, "Hata", "Lütfen bir marka seçin!")
            return
        if not tur_id:
            QMessageBox.warning(self, "Hata", "Lütfen bir tür seçin!")
            return
        if boyut <= 0:
            QMessageBox.warning(self, "Hata", "Boyut 0'dan büyük olmalıdır!")
            return
        if kalan_miktar < 0 or kalan_miktar > boyut:
            QMessageBox.warning(self, "Hata", "Kalan miktar 0 ile şişe boyutu arasında olmalıdır!")
            return
        if fiyat < 0:
            QMessageBox.warning(self, "Hata", "Fiyat negatif olamaz!")
            return
        # Optionally, validate file path, date, etc.

        try:
            if self.editing_id is None: # Yeni parfüm ekle
                self.cursor.execute("""
                    INSERT INTO parfumler (ad, marka_id, tur_id, boyut, kalan_miktar, 
                                        edinme_tarihi, fiyat, koku_notlari, sezon, durum, aciklama, foto_path, kullanici_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (ad, marka_id, tur_id, boyut, kalan_miktar, edinme_tarihi, 
                     fiyat, koku_notlari, sezon, durum, aciklama, foto_path, self.kullanici_id))
                self.conn.commit()
                QMessageBox.information(self, "Başarılı", "Yeni parfüm başarıyla eklendi!")
                self.clear_form()
            else: # Mevcut parfümü güncelle
                # Önce parfümün kullanıcıya ait olup olmadığını kontrol et
                self.cursor.execute("SELECT kullanici_id FROM parfumler WHERE id = ?", (self.editing_id,))
                result = self.cursor.fetchone()
                
                if not result or result['kullanici_id'] != self.kullanici_id:
                    QMessageBox.warning(self, "Hata", "Bu parfümü düzenleme yetkiniz yok!")
                    return
                
                self.cursor.execute("""
                    UPDATE parfumler
                    SET ad = ?, marka_id = ?, tur_id = ?, boyut = ?, kalan_miktar = ?, 
                        edinme_tarihi = ?, fiyat = ?, koku_notlari = ?, sezon = ?, durum = ?, 
                        aciklama = ?, foto_path = ?
                    WHERE id = ? AND kullanici_id = ?
                """, (ad, marka_id, tur_id, boyut, kalan_miktar, edinme_tarihi, 
                     fiyat, koku_notlari, sezon, durum, aciklama, foto_path, self.editing_id, self.kullanici_id))
                self.conn.commit()
                QMessageBox.information(self, "Başarılı", "Parfüm başarıyla güncellendi!")
                self.clear_form()
                self.editing_id = None # Reset editing mode
                self.page_header.setText("YENİ PARFÜM EKLE")
                self.saveButton.setText("Parfüm Ekle")

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Veritabanı Hatası", f"Parfüm kaydedilirken hata oluştu: {e}")
    
    def load_perfume_for_edit(self, perfume_id):
        """Düzenleme için parfüm verilerini yükler ve formu doldurur"""
        self.editing_id = perfume_id
        self.page_header.setText("PARFÜM DÜZENLE")
        self.saveButton.setText("Güncelle")

        try:
            self.cursor.execute("""
                SELECT p.*, m.marka, t.tur_adi
                FROM parfumler p
                LEFT JOIN markalar m ON p.marka_id = m.id
                LEFT JOIN turler t ON p.tur_id = t.id
                WHERE p.id = ?
            """, (perfume_id,))
            perfume = self.cursor.fetchone()

            if perfume:
                self.adLineEdit.setText(perfume['ad'] or '')
                # Set combo box by text, not ID
                marka_index = self.markaComboBox.findText(perfume['marka'] or '')
                if marka_index != -1:
                    self.markaComboBox.setCurrentIndex(marka_index)
                
                tur_index = self.turComboBox.findText(perfume['tur_adi'] or '')
                if tur_index != -1:
                    self.turComboBox.setCurrentIndex(tur_index)
                
                self.boyutSpinBox.setValue(float(perfume['boyut']) if perfume['boyut'] is not None else 0.0)
                self.kalanMiktarSpinBox.setValue(float(perfume['kalan_miktar']) if perfume['kalan_miktar'] is not None else 0.0)
                
                if perfume['edinme_tarihi']:
                    qdate = QDate.fromString(perfume['edinme_tarihi'], "yyyy-MM-dd")
                    self.tarihDateEdit.setDate(qdate)
                else:
                    self.tarihDateEdit.setDate(date.today())
                
                self.fiyatSpinBox.setValue(float(perfume['fiyat']) if perfume['fiyat'] is not None else 0.0)
                self.kokuNotlariTextEdit.setText(perfume['koku_notlari'] or '')
                
                sezon_index = self.sezonComboBox.findText(perfume['sezon'] or '')
                if sezon_index != -1:
                    self.sezonComboBox.setCurrentIndex(sezon_index)
                    
                durum_index = self.durumComboBox.findText(perfume['durum'] or '')
                if durum_index != -1:
                    self.durumComboBox.setCurrentIndex(durum_index)
                
                self.aciklamaTextEdit.setText(perfume['aciklama'] or '')
                self.fotoPathLineEdit.setText(perfume['foto_path'] or '')
                self.update_foto_preview()
            else:
                QMessageBox.warning(self, "Hata", "Parfüm bulunamadı!")
                self.clear_form()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Veritabanı Hatası", f"Parfüm bilgileri yüklenirken hata oluştu: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Form doldurulurken beklenmedik hata oluştu: {e}")
    
    def clear_form(self):
        """Formdaki tüm alanları temizler ve başlangıç durumuna getirir"""
        self.adLineEdit.clear()
        self.markaComboBox.setCurrentIndex(0)
        self.turComboBox.setCurrentIndex(0)
        self.boyutSpinBox.setValue(0.0)
        self.kalanMiktarSpinBox.setValue(0.0)
        self.tarihDateEdit.setDate(date.today())
        self.fiyatSpinBox.setValue(0.0)
        self.kokuNotlariTextEdit.clear()
        self.sezonComboBox.setCurrentIndex(0)
        self.durumComboBox.setCurrentIndex(0)
        self.aciklamaTextEdit.clear()
        self.fotoPathLineEdit.clear()
        self.foto_preview.setText("Fotoğraf yok")
        self.foto_preview.setPixmap(QPixmap())
        
        # Düzenleme modundan çık
        if self.editing_id is not None:
            self.editing_id = None
            self.page_header.setText("YENİ PARFÜM EKLE") 

    def set_kullanici_id(self, kullanici_id):
        self.kullanici_id = kullanici_id 