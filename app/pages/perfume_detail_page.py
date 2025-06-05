import os
import sqlite3
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QMessageBox, QSizePolicy, QTextBrowser, QGridLayout, QFormLayout)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QPixmap, QTextOption
from models.parfum_model import Parfum # Assuming Parfum model is available

class AutoExpandingTextBrowser(QTextBrowser):
    def sizeHint(self):
        # Return a size hint that prefers to expand horizontally as much as possible
        return QSize(10000, super().sizeHint().height())

class PerfumeDetailPage(QWidget):
    back_to_collection_requested = pyqtSignal() # Signal to go back to collection
    edit_perfume_requested = pyqtSignal(int) # Signal to request editing
    delete_perfume_requested = pyqtSignal(int) # Signal to request deletion

    def __init__(self, conn, cursor, kullanici_id=None):
        super(PerfumeDetailPage, self).__init__()
        self.conn = conn
        self.cursor = cursor
        self.kullanici_id = kullanici_id
        self.current_perfume_id = None

        self.setMinimumSize(800, 600) # Set a reasonable minimum size for the window
        self.setStyleSheet("""
            background-color: #f0f2f5; /* A very light gray/blue for the overall page background */
            font-family: 'Segoe UI', sans-serif; /* Modern font */
        """) # Set a light background for the page

        # --- Moved detail label creation and styles to the beginning of __init__ ---
        label_style = '''
            font-size: 16px; /* Font size slightly reduced */
            color: #1e293b;
            font-weight: bold;
            padding-right: 15px; /* Padding azaltıldı */
            min-width: 100px; /* Min width azaltıldı */
            padding-top: 1px; /* Padding azaltıldı */
            padding-bottom: 1px; /* Padding azaltıldı */
        '''
        value_style = '''
            font-size: 16px; /* Font size slightly reduced */
            color: #334155;
            padding: 4px 0; /* Padding azaltıldı */
            background: transparent;
            border-bottom: 1px solid #e2e8f0;
            padding-top: 1px; /* Padding azaltıldı */
            padding-bottom: 1px; /* Padding azaltıldı */
        '''

        self.marka_label = QLabel()
        self.tur_label = QLabel()
        self.boyut_label = QLabel()
        self.kalan_label = QLabel()
        self.tarih_label = QLabel()
        self.fiyat_label = QLabel()
        self.koku_notlari = QLabel()
        self.sezon_label = QLabel()
        self.durum_label = QLabel()
        self.aciklama = QLabel()

        for lbl in [self.marka_label, self.tur_label, self.boyut_label, self.kalan_label, self.tarih_label, self.fiyat_label, self.koku_notlari, self.sezon_label, self.durum_label, self.aciklama]:
             lbl.setStyleSheet(value_style)
             lbl.setWordWrap(True)
             lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
             lbl.setMinimumHeight(24) # Min height azaltıldı
             lbl.setMaximumHeight(16777215)

        def make_label(text):
             l = QLabel(text)
             l.setStyleSheet(label_style)
             l.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
             l.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
             l.setMinimumHeight(24) # Min height azaltıldı
             l.setMaximumHeight(16777215)
             return l
        # --- End: Moved detail label creation and styles ---

        # I. main_layout Yapılandırması:
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        self.main_layout.setAlignment(Qt.AlignTop)

        # II. Üst Bar (Geri Butonu):
        self.back_button = QPushButton("< Geri")
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #4a5568;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 8px 15px;
                font-weight: bold;
                font-size: 14px;
                min-width: 80px;
                box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
            }
            QPushButton:hover {
                background-color: #2d3748;
            }
        """)
        self.back_button.setCursor(Qt.PointingHandCursor)
        self.back_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        ust_bar_layout = QHBoxLayout()
        ust_bar_layout.addWidget(self.back_button)
        ust_bar_layout.addStretch()
        self.main_layout.addLayout(ust_bar_layout)

        # III. Ana İçerik Alanı (İki Sütunlu):
        ana_icerik_layout = QHBoxLayout()
        ana_icerik_layout.setSpacing(20)

        # Sol Sütun (Görsel):
        sol_sutun_layout = QVBoxLayout()
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("""
            border: 2px dashed #cbd5e1;
            background-color: #f8fafc;
            border-radius: 10px;
            padding: 10px; /* Padding biraz azaltılabilir */
            margin: 0;
            min-height: 180px;
            max-height: 250px;
            max-width: 250px;
        """)
        self.image_label.setScaledContents(True)
        self.image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.image_label.setFixedSize(220, 220)

        sol_sutun_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        ana_icerik_layout.addLayout(sol_sutun_layout, 1) # streç faktörü 1


        # Sağ Sütun (Detaylar):
        sag_sutun_layout = QVBoxLayout()
        sag_sutun_layout.setSpacing(10)

        self.perfume_name = QLabel("")
        self.perfume_name.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #1a202c;
            margin-bottom: 10px;
        """)
        self.perfume_name.setAlignment(Qt.AlignLeft)
        self.perfume_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sag_sutun_layout.addWidget(self.perfume_name)

        self.details_form = QFormLayout()
        self.details_form.setSpacing(10)
        self.details_form.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.details_form.setFormAlignment(Qt.AlignTop)

        self.details_form.addRow(make_label("Marka:"), self.marka_label)
        self.details_form.addRow(make_label("Tür:"), self.tur_label)
        self.details_form.addRow(make_label("Boyut:"), self.boyut_label)
        self.details_form.addRow(make_label("Kalan Miktar:"), self.kalan_label)
        self.details_form.addRow(make_label("Edinme Tarihi:"), self.tarih_label)
        self.details_form.addRow(make_label("Fiyat:"), self.fiyat_label)
        self.details_form.addRow(make_label("Koku Notaları:"), self.koku_notlari)
        self.details_form.addRow(make_label("Sezon:"), self.sezon_label)
        self.details_form.addRow(make_label("Durum:"), self.durum_label)
        self.details_form.addRow(make_label("Açıklama:"), self.aciklama)

        details_widget = QWidget()
        details_widget.setLayout(self.details_form)
        details_widget.setStyleSheet('background: #f8fafc; border-radius: 10px; padding: 15px 20px;')
        details_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        details_widget.setMinimumWidth(600)
        details_widget.setMinimumHeight(300)
        sag_sutun_layout.addWidget(details_widget)

        ana_icerik_layout.addLayout(sag_sutun_layout, 2)

        self.main_layout.addLayout(ana_icerik_layout)
        self.main_layout.addStretch(1)

        # IV. Alt Bar (Eylem Butonları):
        alt_buton_layout = QHBoxLayout()
        alt_buton_layout.setSpacing(15)
        alt_buton_layout.addStretch()

        self.edit_button = QPushButton("Düzenle")
        self.edit_button.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 10px;
                padding: 14px 30px;
                min-width: 120px;
                box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
                transition: background-color 0.3s ease, transform 0.2s ease;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background-color: #1e40af;
                transform: translateY(0);
            }
        """)
        self.edit_button.setCursor(Qt.PointingHandCursor)
        alt_buton_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Sil")
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #dc2626;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 10px;
                padding: 14px 30px;
                min-width: 120px;
                box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
                transition: background-color 0.3s ease, transform 0.2s ease;
            }
            QPushButton:hover {
                background-color: #b91c1c;
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background-color: #991b1b;
                transform: translateY(0);
            }
        """)
        self.delete_button.setCursor(Qt.PointingHandCursor)
        alt_buton_layout.addWidget(self.delete_button)

        alt_buton_layout.addStretch()
        self.main_layout.addLayout(alt_buton_layout)

        self.main_layout.addStretch() # Push everything to the top if needed

        self.setup_connections()

    def setup_connections(self):
        self.back_button.clicked.connect(self.back_to_collection_requested.emit)
        self.edit_button.clicked.connect(lambda: self.edit_perfume_requested.emit(self.current_perfume_id))
        self.delete_button.clicked.connect(lambda: self.delete_perfume_requested.emit(self.current_perfume_id))

    def load_perfume(self, perfume_id):
        self.current_perfume_id = perfume_id  # Always set the current perfume ID
        try:
            # Parfümü ve kullanıcı ID'sini kontrol et
            self.cursor.execute("""
                SELECT p.*, m.marka, t.tur_adi
                FROM parfumler p
                LEFT JOIN markalar m ON p.marka_id = m.id
                LEFT JOIN turler t ON p.tur_id = t.id
                WHERE p.id = ? AND p.kullanici_id = ?
            """, (perfume_id, self.kullanici_id))
            
            perfume = self.cursor.fetchone()
            
            if not perfume:
                QMessageBox.warning(self, "Hata", "Parfüm bulunamadı veya bu parfüme erişim izniniz yok!")
                self.back_to_collection_requested.emit()
                return
            
            # Parfüm bilgilerini göster
            self.perfume_name.setText(perfume['ad'])
            self.marka_label.setText(perfume['marka'] or 'Belirtilmemiş')
            self.tur_label.setText(perfume['tur_adi'] or 'Belirtilmemiş')
            
            # Boyut ve kalan miktar
            boyut = f"{perfume['boyut']:.1f} ml" if perfume['boyut'] is not None else 'Belirtilmemiş'
            kalan = f"{perfume['kalan_miktar']:.1f} ml" if perfume['kalan_miktar'] is not None else 'Belirtilmemiş'
            self.boyut_label.setText(boyut)
            self.kalan_label.setText(kalan)
            
            # Tarih ve fiyat
            self.tarih_label.setText(perfume['edinme_tarihi'] or 'Belirtilmemiş')
            fiyat = f"{perfume['fiyat']:.2f} ₺" if perfume['fiyat'] is not None else 'Belirtilmemiş'
            self.fiyat_label.setText(fiyat)
            
            # Koku notları
            self.koku_notlari.setText(perfume['koku_notlari'] or 'Belirtilmemiş')
            
            # Sezon ve durum
            self.sezon_label.setText(perfume['sezon'] or 'Belirtilmemiş')
            self.durum_label.setText(perfume['durum'] or 'Belirtilmemiş')
            
            # Açıklama
            self.aciklama.setText(perfume['aciklama'] or 'Belirtilmemiş')
            
            # Fotoğrafı yükle ve göster
            foto_path = perfume['foto_path']
            if foto_path and os.path.exists(foto_path):
                try:
                    pixmap = QPixmap(foto_path)
                    if not pixmap.isNull():
                        # Scale the pixmap to fit the fixed size image_label while maintaining aspect ratio
                        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                        self.image_label.setText('') # Clear text if image is loaded
                    else:
                        self.image_label.setText("Geçersiz fotoğraf dosyası")
                        self.image_label.setPixmap(QPixmap()) # Clear any previous pixmap
                except Exception as img_e:
                    self.image_label.setText("Fotoğraf yüklenirken hata oluştu")
                    self.image_label.setPixmap(QPixmap()) # Clear any previous pixmap
                    print(f"Fotoğraf yükleme hatası: {img_e}") # Log error for debugging
            else:
                self.image_label.setText("Fotoğraf yok")
                self.image_label.setPixmap(QPixmap()) # Clear any previous pixmap
            
            # Butonları aktif et
            self.edit_button.setEnabled(True)
            self.delete_button.setEnabled(True)
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Veritabanı Hatası", f"Parfüm bilgileri yüklenirken hata oluştu: {e}")
            self.back_to_collection_requested.emit()

    def clear_details(self):
        self.current_perfume_id = None
        self.perfume_name.setText("Parfüm Detayları")
        # Clear all detail labels
        self.marka_label.setText('')
        self.tur_label.setText('')
        self.boyut_label.setText('')
        self.kalan_label.setText('')
        self.tarih_label.setText('')
        self.fiyat_label.setText('')
        self.koku_notlari.setText('')
        self.sezon_label.setText('')
        self.durum_label.setText('')
        self.aciklama.setText('')

        # Clear image label
        self.image_label.setText("Fotoğraf yok")
        self.image_label.setPixmap(QPixmap()) # Clear any previous pixmap 