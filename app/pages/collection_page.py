import sqlite3
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                            QPushButton, QTableView, QHeaderView, QAbstractItemView,
                            QSplitter, QFrame, QMessageBox)
from PyQt5.QtCore import Qt, QSortFilterProxyModel, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont, QIcon, QPixmap
import os

class CollectionPage(QWidget):
    perfume_edit_requested = pyqtSignal(int)

    def __init__(self, conn, cursor, kullanici_id=None):
        super(CollectionPage, self).__init__()
        self.conn = conn
        self.cursor = cursor
        self.kullanici_id = kullanici_id
        
        # Ana layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 25, 20, 20)
        self.main_layout.setSpacing(20)
        
        # Sayfa başlığı
        self.page_header = QLabel("PARFÜM KOLEKSİYONU")
        self.page_header.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #3b82f6;
            margin-bottom: 10px;
            padding: 20px;
        """)
        self.page_header.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.page_header)
        
        # Arama bölümü
        self.search_layout = QHBoxLayout()
        self.search_layout.setSpacing(15)
        
        self.search_label = QLabel("Parfüm Ara:")
        self.search_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.search_layout.addWidget(self.search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Parfüm adı, markası veya koku notaları...")
        self.search_input.setStyleSheet("""
            font-size: 16px; 
            padding: 10px;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            min-height: 35px;
        """)
        self.search_layout.addWidget(self.search_input, 1)
        
        self.refresh_button = QPushButton("Yenile")
        self.refresh_button.setStyleSheet("""
            background-color: #3b82f6;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border-radius: 6px;
            padding: 10px 15px;
            min-width: 100px;
        """)
        self.refresh_button.setCursor(Qt.PointingHandCursor)
        self.search_layout.addWidget(self.refresh_button)
        
        self.main_layout.addLayout(self.search_layout)
        
        # Tablo
        self.table_view = QTableView()
        self.table_view.setMinimumWidth(700)
        self.table_view.setStyleSheet("""
            QTableView {
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                background-color: white;
                alternate-background-color: #f8fafc;
                gridline-color: #e2e8f0;
                font-size: 16px;
            }
            QTableView::item {
                padding: 12px;
                border-bottom: 1px solid #e2e8f0;
            }
            QHeaderView::section {
                background-color: #f1f5f9;
                color: #0f172a;
                padding: 20px;
                border: none;
                border-right: 1px solid #cbd5e1;
                font-weight: bold;
                font-size: 16px;
            }
            QTableView:item:selected {
                background-color: #93c5fd;
                color: #0f172a;
            }
        """)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_view.setAlternatingRowColors(True)
        
        # Remove Detail Frame and related components
        # self.detail_frame = QFrame()
        # self.detail_frame.setFrameShape(QFrame.StyledPanel)
        # ... (rest of detail_frame setup)
        
        # Remove Splitter and directly add table_view to main_layout
        self.main_layout.addWidget(self.table_view, 1) # 1 ağırlık ile genişlesin
        
        # Model oluştur
        self.setup_model()
        
        # Bağlantıları kur
        self.setup_connections()
        
        # Verileri yükle
        self.load_parfumler()
        
        # Removed: self.detail_frame.hide()
    
    def setup_model(self):
        """Tablo modelini oluşturur"""
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([
            "ID", "Ad", "Marka", "Tür", "Boyut (ml)", 
            "Kalan Miktar (ml)", "Edinme Tarihi", "Fiyat (₺)"
        ])
        
        # Proxy model oluştur - arama için
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy_model.setFilterKeyColumn(-1)  # Tüm sütunlarda ara
        
        # Modeli tabloyla ilişkilendir
        self.table_view.setModel(self.proxy_model)
        
        # ID kolonunu gizle
        self.table_view.hideColumn(0)
    
    def setup_connections(self):
        """Sinyal bağlantılarını kurar"""
        self.refresh_button.clicked.connect(self.load_parfumler)
        self.search_input.textChanged.connect(self.filter_perfumes)
        self.table_view.selectionModel().selectionChanged.connect(self.show_selected_perfume)
        # Removed: self.edit_button.clicked.connect(self.edit_perfume)
        # Removed: self.delete_button.clicked.connect(self.delete_perfume)
        # Removed: self.close_detail_button.clicked.connect(self.hide_detail_frame)
    
    def load_parfumler(self):
        """Parfümleri veritabanından yükler ve tabloya ekler"""
        try:
            self.model.removeRows(0, self.model.rowCount())  # Tabloyu temizle
            
            # Sadece giriş yapan kullanıcının parfümlerini getir
            self.cursor.execute("""
                SELECT p.*, m.marka, t.tur_adi
                FROM parfumler p
                LEFT JOIN markalar m ON p.marka_id = m.id
                LEFT JOIN turler t ON p.tur_id = t.id
                WHERE p.kullanici_id = ?
                ORDER BY p.ad
            """, (self.kullanici_id,))
            
            parfumler = self.cursor.fetchall()
            
            for row, parfum in enumerate(parfumler):
                self.model.insertRow(row)
                
                # Parfüm adı
                self.model.setData(self.model.index(row, 0), parfum['id'])
                self.model.setData(self.model.index(row, 1), parfum['ad'])
                
                # Marka
                self.model.setData(self.model.index(row, 2), parfum['marka'])
                
                # Tür
                self.model.setData(self.model.index(row, 3), parfum['tur_adi'])
                
                # Boyut
                boyut = f"{parfum['boyut']:.1f} ml" if parfum['boyut'] is not None else ''
                self.model.setData(self.model.index(row, 4), boyut)
                
                # Kalan Miktar
                kalan = f"{parfum['kalan_miktar']:.1f} ml" if parfum['kalan_miktar'] is not None else ''
                self.model.setData(self.model.index(row, 5), kalan)
                
                # Edinme Tarihi
                self.model.setData(self.model.index(row, 6), parfum['edinme_tarihi'])
                
                # Fiyat
                fiyat = f"{parfum['fiyat']:.2f} ₺" if parfum['fiyat'] is not None else ''
                self.model.setData(self.model.index(row, 7), fiyat)
                
                # Sezon
                self.model.setData(self.model.index(row, 8), parfum['sezon'])
                
                # Durum
                self.model.setData(self.model.index(row, 9), parfum['durum'])
                
                # İşlem butonları
                actions_widget = QWidget()
                actions_layout = QHBoxLayout(actions_widget)
                actions_layout.setContentsMargins(4, 4, 4, 4)
                actions_layout.setSpacing(4)
                
                # Detay butonu
                detail_btn = QPushButton("Detay")
                detail_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #3b82f6;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 4px 8px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #2563eb;
                    }
                """)
                detail_btn.setCursor(Qt.PointingHandCursor)
                detail_btn.clicked.connect(lambda checked, pid=parfum['id']: self.show_perfume_detail(pid))
                actions_layout.addWidget(detail_btn)
                
                # Düzenle butonu
                edit_btn = QPushButton("Düzenle")
                edit_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #10b981;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 4px 8px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #059669;
                    }
                """)
                edit_btn.setCursor(Qt.PointingHandCursor)
                edit_btn.clicked.connect(lambda checked, pid=parfum['id']: self.edit_perfume(pid))
                actions_layout.addWidget(edit_btn)
                
                # Sil butonu
                delete_btn = QPushButton("Sil")
                delete_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #ef4444;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 4px 8px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #dc2626;
                    }
                """)
                delete_btn.setCursor(Qt.PointingHandCursor)
                delete_btn.clicked.connect(lambda checked, pid=parfum['id']: self.delete_perfume(pid))
                actions_layout.addWidget(delete_btn)
                
                actions_layout.addStretch()
            
            # Sütun genişliklerini ayarla
            self.table_view.horizontalHeader().resizeSections(QHeaderView.ResizeToContents)
            for i in range(self.model.columnCount()):
                self.table_view.horizontalHeader().setSectionResizeMode(i, QHeaderView.Interactive)
            self.table_view.horizontalHeader().setStretchLastSection(True)
        
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Veritabanı Hatası", f"Parfümler yüklenirken hata oluştu: {e}")
    
    def filter_perfumes(self, text):
        """Parfümleri filtreler"""
        self.proxy_model.setFilterFixedString(text)
    
    def show_selected_perfume(self, selected, deselected):
        """Seçilen parfümün detaylarını gösterir"""
        indexes = selected.indexes()
        if len(indexes) > 0:
            proxy_index = indexes[0]
            source_index = self.proxy_model.mapToSource(proxy_index)
            row = source_index.row()
            
            perfume_id = int(self.model.data(self.model.index(row, 0)))
            # print(f"CollectionPage: Selected perfume ID: {perfume_id}") # Debug print removed
            
            # Emit signal to MainWindow to show detail page
            self.perfume_edit_requested.emit(perfume_id)

        else:
            # If no selection, ensure any detail page is hidden or reset
            # This might be handled by MainWindow when switching pages
            pass # No longer hiding local detail frame
    
    def edit_perfume(self, perfume_id):
        """Seçilen parfümü düzenlemek için sinyal gönderir (şimdi PerfumeDetailPage tarafından işleniyor)"""
        # This method might become redundant if editing is handled directly by PerfumeDetailPage
        # For now, it will emit the same signal as selection
        self.perfume_edit_requested.emit(perfume_id)

    def delete_perfume(self, perfume_id):
        """Seçilen parfümü siler"""
        reply = QMessageBox.question(self, 'Parfüm Sil', 
                                    f'"{self.model.data(self.model.index(perfume_id, 1))}" parfümünü silmek istediğinize emin misiniz?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                # Parfümü sil
                self.cursor.execute("DELETE FROM parfumler WHERE id = ?", (perfume_id,))
                self.conn.commit()
                
                # Tabloyu yenile
                self.load_parfumler()
                
                QMessageBox.information(self, "Başarılı", f'"{self.model.data(self.model.index(perfume_id, 1))}" parfümü başarıyla silindi.')
            
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Veritabanı Hatası", f"Parfüm silinirken hata oluştu: {e}") 