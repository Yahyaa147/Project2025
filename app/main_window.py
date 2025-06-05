import sys
import sqlite3
import os
from PyQt5.QtWidgets import (QMainWindow, QMessageBox, QFileDialog, QTableView, 
                            QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, 
                            QStackedWidget, QListWidget, QListWidgetItem, QFrame,
                            QSplitter, QSizePolicy)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor
from app.pages.collection_page import CollectionPage
from app.pages.add_perfume_page import AddPerfumePage
from app.pages.edit_profile_page import EditProfilePage
from app.pages.perfume_detail_page import PerfumeDetailPage
from app.login_form import LoginForm
from controllers.user_controller import UserController
from app.database_manager import DatabaseManager

class MainWindow(QMainWindow):
    def __init__(self, user_info=None):
        super(MainWindow, self).__init__()
        
        # Kullanıcı bilgisi ve ID'sini sakla
        self.user_info = user_info or {}
        self.kullanici_id = self.user_info.get('kullanici_id') if self.user_info else None
        
        # Temel ayarlar
        self.setWindowTitle("Parfüm Koleksiyonu Yönetimi")
        self.setMinimumSize(1200, 800)
        
        # Veritabanı bağlantısı
        try:
            self.db_manager = DatabaseManager()
            self.conn = self.db_manager.conn
            self.cursor = self.db_manager.cursor
            print("Veritabanı bağlantısı başarılı")
            
        except sqlite3.Error as e:
            print(f"Veritabanı hatası: {e}")
        
        # Kontrolcüleri oluştur
        self.user_controller = UserController(self.conn)
        
        # Ana widget'ı oluştur
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Ana layout
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Sidebar oluştur
        self.setup_sidebar()
        
        # İçerik alanını oluştur
        self.setup_content_area()
        
        # Sayfa bağlantılarını kur
        self.setup_connections()

        # Varsayılan olarak koleksiyon sayfasını göster
        self.show_page(0)

        # Uygulamayı göster
        self.show()
    
    def setup_sidebar(self):
        """Sol taraftaki navigasyon sidebar'ını oluşturur"""
        # Sidebar Container
        self.sidebar_widget = QWidget()
        self.sidebar_widget.setObjectName("sidebar")
        self.sidebar_widget.setStyleSheet("""
            QWidget#sidebar {
                background-color: #1e293b;
                min-width: 250px;
                max-width: 250px;
            }
            QListWidget {
                background-color: transparent;
                border: none;
                color: #f8fafc;
                font-size: 16px;
                padding: 10px;
            }
            QListWidget::item {
                height: 50px;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 5px;
            }
            QListWidget::item:selected {
                background-color: #3b82f6;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #334155;
            }
            QLabel {
                color: #f8fafc;
            }
        """)
        
        self.sidebar_layout = QVBoxLayout(self.sidebar_widget)
        self.sidebar_layout.setContentsMargins(10, 20, 10, 20)
        self.sidebar_layout.setSpacing(20)
        
        # Logo ve başlık
        self.header_layout = QHBoxLayout()
        self.logo_label = QLabel()
        # self.logo_label.setPixmap(QPixmap("resources/icons/perfume.png").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.header_layout.addWidget(self.logo_label)
        
        self.title_label = QLabel("Parfüm Koleksiyonu")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #f8fafc;")
        self.header_layout.addWidget(self.title_label)
        self.header_layout.addStretch()
        self.sidebar_layout.addLayout(self.header_layout)
        
        # Ayırıcı çizgi
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #475569;")
        self.sidebar_layout.addWidget(separator)
        
        # Navigasyon Menüsü
        self.nav_list = QListWidget()
        self.nav_list.setIconSize(QSize(24, 24))
        
        # Koleksiyon Göster
        self.collection_item = QListWidgetItem("Koleksiyon Göster")
        # self.collection_item.setIcon(QIcon("resources/icons/collection.png"))
        self.nav_list.addItem(self.collection_item)
        
        # Parfüm Ekle
        self.add_item = QListWidgetItem("Parfüm Ekle")
        # self.add_item.setIcon(QIcon("resources/icons/add.png"))
        self.nav_list.addItem(self.add_item)
        
        # Profili Düzenle
        self.edit_profile_item = QListWidgetItem("Profili Düzenle")
        # self.edit_profile_item.setIcon(QIcon("resources/icons/edit_profile.png")) # Yeni ikon
        self.nav_list.addItem(self.edit_profile_item)
        
        self.sidebar_layout.addWidget(self.nav_list)
        self.sidebar_layout.addStretch()
        
        # Çıkış Yap butonu ekle
        self.logout_button = QPushButton("Çıkış Yap")
        self.logout_button.setStyleSheet("background-color: #ef4444; color: white; font-weight: bold; border-radius: 8px; padding: 12px; font-size: 16px;")
        self.logout_button.setCursor(Qt.PointingHandCursor)
        self.sidebar_layout.addWidget(self.logout_button)
        
        # Ana layout'a sidebar ekle
        self.main_layout.addWidget(self.sidebar_widget)
    
    def setup_content_area(self):
        """İçerik alanını oluşturur - çoklu sayfa yapısı"""
        # İçerik container
        self.content_widget = QWidget()
        self.content_widget.setObjectName("content")
        self.content_widget.setStyleSheet("""
            QWidget#content {
                background-color: #f8fafc;
            }
        """)
        
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Sayfaları tutacak StackedWidget
        self.page_stack = QStackedWidget()
        self.page_stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Koleksiyon Sayfası
        self.collection_page = CollectionPage(self.conn, self.cursor, self.kullanici_id)
        self.page_stack.addWidget(self.collection_page)
        
        # Ekleme Sayfası
        self.add_page = AddPerfumePage(self.conn, self.cursor, self.kullanici_id)
        self.page_stack.addWidget(self.add_page)
        
        # Profili Düzenle Sayfası
        self.edit_profile_page = EditProfilePage(self.user_controller, self.user_info)
        self.page_stack.addWidget(self.edit_profile_page)
        
        # Parfüm Detay Sayfası
        self.perfume_detail_page = PerfumeDetailPage(self.conn, self.cursor, self.kullanici_id)
        self.page_stack.addWidget(self.perfume_detail_page)
        
        self.content_layout.addWidget(self.page_stack)
        
        # Ana layout'a içerik ekle
        self.main_layout.addWidget(self.content_widget, 99)  # Increased stretch factor for content
    
    def setup_connections(self):
        """Sayfalara geçiş bağlantılarını oluşturur"""
        self.nav_list.currentRowChanged.connect(self.show_page)
        # Connect the signal from CollectionPage to show perfume detail
        self.collection_page.perfume_edit_requested.connect(self.show_perfume_detail)
        
        # Connect signals from PerfumeDetailPage
        self.perfume_detail_page.back_to_collection_requested.connect(lambda: self.show_page(0)) # Go back to collection page
        self.perfume_detail_page.edit_perfume_requested.connect(self.show_edit_perfume) # Re-use existing edit method
        self.perfume_detail_page.delete_perfume_requested.connect(self.delete_perfume_from_detail) # New method for delete from detail
        
        # Çıkış Yap butonuna bağlantı
        self.logout_button.clicked.connect(self.logout_and_return_to_login)
    
    def show_page(self, index):
        """Seçilen sayfayı gösterir"""
        self.page_stack.setCurrentIndex(index)
        # Her sayfa geçişinde ilgili sayfaya güncel kullanıcı bilgisini aktar (eğer gerekliyse)
        if index == self.page_stack.indexOf(self.add_page):
            self.add_page.set_kullanici_id(self.kullanici_id)
        elif index == self.page_stack.indexOf(self.edit_profile_page):
            self.edit_profile_page.load_user_data()
        # self.nav_list.setCurrentRow(index) # This would change sidebar selection when going to detail page

    def show_perfume_detail(self, perfume_id):
        """Parfüm detay sayfasını gösterir ve detayları yükler"""
        # Find the index of PerfumeDetailPage in the stack
        detail_page_index = self.page_stack.indexOf(self.perfume_detail_page)
        self.page_stack.setCurrentIndex(detail_page_index)
        self.perfume_detail_page.load_perfume(perfume_id)

    def show_edit_perfume(self, perfume_id):
        """Parfüm düzenleme sayfasını gösterir (şu an ekleme sayfası gibi davranır)"""
        # Assuming AddPerfumePage can also be used for editing
        self.add_page.load_perfume_for_edit(perfume_id) # Need to implement this in AddPerfumePage
        self.show_page(1) # Show the Add/Edit page

    def delete_perfume_from_detail(self, perfume_id):
        """Detay sayfasından parfüm siler"""
        # Re-use delete logic from CollectionPage if possible, or implement here
        # For simplicity, will implement a basic delete here
        reply = QMessageBox.question(self, 'Parfüm Sil', 
                                    f'Bu parfümü silmek istediğinize emin misiniz?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                self.cursor.execute("DELETE FROM parfumler WHERE id = ?", (perfume_id,))
                self.conn.commit()
                QMessageBox.information(self, "Başarılı", "Parfüm başarıyla silindi.")
                self.collection_page.load_parfumler() # Refresh collection page
                self.show_page(0) # Go back to collection page after deletion
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Veritabanı Hatası", f"Parfüm silinirken hata oluştu: {e}")

    def logout_and_return_to_login(self):
        self.close()  # Ana pencereyi kapat
        # Login ekranını tekrar aç
        login_dialog = LoginForm()
        if login_dialog.exec_() == login_dialog.Accepted:
            # Giriş başarılıysa kullanıcı bilgisini al
            user_info = getattr(login_dialog, 'user_info', None)
            if user_info is None and hasattr(login_dialog, 'get_user_info'):
                user_info = login_dialog.get_user_info()
            main_window = MainWindow(user_info=user_info)
            main_window.show()

    def update_user_info(self, user_info):
        self.user_info = user_info
        self.kullanici_id = self.user_info.get('kullanici_id')
        # Update user_info in relevant pages if necessary
        self.collection_page.kullanici_id = self.kullanici_id
        self.add_page.set_kullanici_id(self.kullanici_id)
        self.perfume_detail_page.kullanici_id = self.kullanici_id
        self.edit_profile_page.user_info = self.user_info
        self.edit_profile_page.kullanici_id = self.kullanici_id
        # Update window title with new username if exists
        if self.user_info and 'kullanici_adi' in self.user_info:
            self.setWindowTitle(f"Parfüm Koleksiyonu - {self.user_info['kullanici_adi']}") 