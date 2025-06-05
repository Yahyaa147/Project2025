import os
from PyQt5.QtWidgets import QDialog, QMessageBox, QInputDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFrame
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QCursor
from PyQt5 import uic

class LoginForm(QDialog):
    """
    Kullanıcı giriş ekranı
    
    Kullanıcı bilgilerini alarak giriş işlemini gerçekleştirir
    """
    
    login_success = pyqtSignal(dict)  # Başarılı giriş için sinyal, kullanıcı bilgilerini taşır
    
    def __init__(self, db_controller, parent=None):
        super().__init__(parent)
        
        # UI dosyasını yükle
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(current_dir, 'login_form.ui')
        uic.loadUi(ui_file, self)
        
        # Veritabanı bağlantısı
        self.db_controller = db_controller
        
        # Pencere özellikleri
        self.setWindowTitle("Parfüm Koleksiyonu - Giriş")
        self.setFixedSize(450, 650)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        # Hata mesajını gizle
        self.lbl_hata.setVisible(False)
        
        # Sinyalleri bağla
        self.btn_giris.clicked.connect(self.giris_yap)
        self.btn_kayit.clicked.connect(self.yeni_kayit_ac)
        
        # Enter tuşu davranışını ayarla
        self.txt_sifre.returnPressed.connect(self.giris_yap)
        
        # İlk odaklanmayı kullanıcı adı kutusuna yap
        self.txt_kullanici_adi.setFocus()
    
    def giris_yap(self):
        """Giriş işlemini gerçekleştirir"""
        kullanici_adi = self.txt_kullanici_adi.text().strip()
        sifre = self.txt_sifre.text().strip()
        
        # Boş kontrol
        if not kullanici_adi or not sifre:
            self.lbl_hata.setText("Kullanıcı adı ve şifre gereklidir!")
            self.lbl_hata.setVisible(True)
            return
        
        # Kullanıcı bilgilerini doğrula
        kullanici = self.db_controller.kullanici_kontrol(kullanici_adi, sifre)
        
        if kullanici:
            # Başarılı giriş
            self.lbl_hata.setVisible(False)
            self.login_success.emit(kullanici)  # Kullanıcı bilgilerini sinyal ile ilet
            self.accept()  # Dialog'u kabul et ve kapat
        else:
            # Başarısız giriş
            self.lbl_hata.setText("Kullanıcı adı veya şifre hatalı!")
            self.lbl_hata.setVisible(True)
            self.txt_sifre.clear()
            self.txt_sifre.setFocus()
    
    def yeni_kayit_ac(self):
        """Yeni kullanıcı kayıt ekranını açar"""
        # Yeni kayıt formunu aç
        kayit_form = KayitForm(self.db_controller, self)
        sonuc = kayit_form.exec_()
        
        if sonuc == QDialog.Accepted:
            # Kayıt başarılı
            # Kullanıcı adı ve şifreyi giriş formuna kopyala
            self.txt_kullanici_adi.setText(kayit_form.kullanici_adi)
            self.txt_sifre.setText(kayit_form.sifre)
            self.giris_yap()  # Otomatik giriş yap


class KayitForm(QDialog):
    """Yeni kullanıcı kayıt formu"""
    
    def __init__(self, db_controller, parent=None):
        super().__init__(parent)
        
        self.db_controller = db_controller
        self.kullanici_adi = ""
        self.sifre = ""
        
        # Pencere özellikleri
        self.setWindowTitle("Yeni Kullanıcı Kaydı")
        self.setFixedSize(450, 720)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        # Stil ayarla
        self.setStyleSheet("""
            QDialog {
                background-color: #1e293b;
            }
            QLabel {
                color: #cbd5e1;
                font-size: 14px;
                font-weight: bold;
            }
            QLabel#lbl_baslik {
                color: #f3f4f6;
                font-size: 22px;
                font-weight: bold;
            }
            QLabel#lbl_aciklama {
                color: #cbd5e1;
                font-size: 14px;
                font-weight: normal;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #475569;
                border-radius: 8px;
                background-color: #334155;
                color: #f3f4f6;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #3b82f6;
            }
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton#btn_kaydet {
                background-color: #10b981;
            }
            QPushButton#btn_kaydet:hover {
                background-color: #059669;
            }
            QLabel#lbl_hata {
                color: #ef4444;
                font-weight: bold;
                min-height: 35px;
                background-color: rgba(239, 68, 68, 0.1);
                border-radius: 5px;
                padding: 5px;
                margin-top: 5px;
                margin-bottom: 5px;
                line-height: 25px;
            }
            QFrame#main_frame {
                background-color: #273549;
                border-radius: 12px;
                border: 1px solid #475569;
            }
            #icon_container {
                background-color: #10b981;
                border-radius: 10px;
            }
            #icon_label {
                font-size: 36px;
            }
        """)
        
        # Ana layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)
        
        # Üst bölüm - icon ve başlık
        header_layout = QHBoxLayout()
        
        # İkon container
        icon_container = QFrame()
        icon_container.setObjectName("icon_container")
        icon_container.setMinimumSize(70, 70)
        icon_container.setMaximumSize(70, 70)
        
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_label = QLabel("👤")  # Kullanıcı ikonu
        icon_label.setObjectName("icon_label")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_layout.addWidget(icon_label, 0, Qt.AlignCenter)
        
        # Başlık ve açıklama
        title_layout = QVBoxLayout()
        title_layout.setContentsMargins(20, 0, 0, 0)
        title_layout.setSpacing(8)
        
        lbl_baslik = QLabel("Yeni Hesap Oluştur")
        lbl_baslik.setObjectName("lbl_baslik")
        
        lbl_aciklama = QLabel("Kişisel koleksiyon uygulamanız için hesap oluşturun")
        lbl_aciklama.setObjectName("lbl_aciklama")
        lbl_aciklama.setWordWrap(True)
        
        title_layout.addWidget(lbl_baslik)
        title_layout.addWidget(lbl_aciklama)
        
        header_layout.addWidget(icon_container)
        header_layout.addLayout(title_layout)
        
        # Form içeriği için ana çerçeve
        main_frame = QFrame()
        main_frame.setObjectName("main_frame")
        form_layout = QVBoxLayout(main_frame)
        form_layout.setContentsMargins(25, 30, 25, 30)
        form_layout.setSpacing(20)
        
        # Karşılama etiketi
        welcome_label = QLabel("Kullanıcı Bilgileri")
        welcome_label.setStyleSheet("color: #f3f4f6; font-size: 20px; font-weight: bold;")
        welcome_label.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(welcome_label, 0, Qt.AlignCenter)
        form_layout.addSpacing(20)
        
        # Hata mesajı - Üst kısımda konumlandır
        self.lbl_hata = QLabel()
        self.lbl_hata.setObjectName("lbl_hata")
        self.lbl_hata.setAlignment(Qt.AlignCenter)
        self.lbl_hata.setMinimumHeight(35)
        self.lbl_hata.setWordWrap(True)
        self.lbl_hata.setVisible(False)  # Başlangıçta gizli
        form_layout.addWidget(self.lbl_hata)
        
        # Kullanıcı adı
        username_layout = QVBoxLayout()
        username_layout.setSpacing(10)
        
        lbl_kullanici = QLabel("Kullanıcı Adı")
        self.txt_kullanici_adi = QLineEdit()
        self.txt_kullanici_adi.setMinimumHeight(48)
        self.txt_kullanici_adi.setPlaceholderText("Kullanıcı adınızı girin")
        
        username_layout.addWidget(lbl_kullanici)
        username_layout.addWidget(self.txt_kullanici_adi)
        form_layout.addLayout(username_layout)
        form_layout.addSpacing(20)
        
        # Şifre
        password_layout = QVBoxLayout()
        password_layout.setSpacing(10)
        
        lbl_sifre = QLabel("Şifre")
        self.txt_sifre = QLineEdit()
        self.txt_sifre.setMinimumHeight(48)
        self.txt_sifre.setEchoMode(QLineEdit.Password)
        self.txt_sifre.setPlaceholderText("Şifrenizi girin")
        
        password_layout.addWidget(lbl_sifre)
        password_layout.addWidget(self.txt_sifre)
        form_layout.addLayout(password_layout)
        form_layout.addSpacing(20)
        
        # Ad Soyad
        fullname_layout = QVBoxLayout()
        fullname_layout.setSpacing(10)
        
        lbl_ad_soyad = QLabel("Ad Soyad (İsteğe bağlı)")
        self.txt_ad_soyad = QLineEdit()
        self.txt_ad_soyad.setMinimumHeight(48)
        self.txt_ad_soyad.setPlaceholderText("Adınızı ve soyadınızı girin")
        
        fullname_layout.addWidget(lbl_ad_soyad)
        fullname_layout.addWidget(self.txt_ad_soyad)
        form_layout.addLayout(fullname_layout)
        form_layout.addSpacing(20)
        
        # Email
        email_layout = QVBoxLayout()
        email_layout.setSpacing(10)
        
        lbl_email = QLabel("E-posta (İsteğe bağlı)")
        self.txt_email = QLineEdit()
        self.txt_email.setMinimumHeight(48)
        self.txt_email.setPlaceholderText("E-posta adresinizi girin")
        
        email_layout.addWidget(lbl_email)
        email_layout.addWidget(self.txt_email)
        form_layout.addLayout(email_layout)
        form_layout.addSpacing(20)
        
        # Butonlar
        self.btn_iptal = QPushButton("Vazgeç")
        self.btn_iptal.setObjectName("btn_iptal")
        self.btn_iptal.setMinimumHeight(50)
        self.btn_iptal.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_iptal.clicked.connect(self.reject)
        form_layout.addWidget(self.btn_iptal)
        form_layout.addSpacing(15)
        
        self.btn_kaydet = QPushButton("Hesap Oluştur")
        self.btn_kaydet.setObjectName("btn_kaydet")
        self.btn_kaydet.setMinimumHeight(50)
        self.btn_kaydet.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_kaydet.clicked.connect(self.kullanici_kaydet)
        form_layout.addWidget(self.btn_kaydet)
        
        # Ana düzen
        main_layout.addLayout(header_layout)
        main_layout.addWidget(main_frame)
        
        # İlk odaklanma
        self.txt_kullanici_adi.setFocus()
    
    def kullanici_kaydet(self):
        """Kullanıcı bilgilerini validasyon sonrası kaydeder"""
        kullanici_adi = self.txt_kullanici_adi.text().strip()
        sifre = self.txt_sifre.text().strip()
        ad_soyad = self.txt_ad_soyad.text().strip()
        email = self.txt_email.text().strip()
        
        # Validasyon
        if not kullanici_adi:
            self.lbl_hata.setText("Kullanıcı adı gereklidir!")
            self.lbl_hata.setVisible(True)
            return
        
        if not sifre:
            self.lbl_hata.setText("Şifre gereklidir!")
            self.lbl_hata.setVisible(True)
            return
        
        if len(sifre) < 6:
            self.lbl_hata.setText("Şifre en az 6 karakter olmalıdır!")
            self.lbl_hata.setVisible(True)
            return
        
        # Kullanıcı ekle
        basarili, mesaj = self.db_controller.kullanici_ekle(kullanici_adi, sifre, ad_soyad, email)
        
        if basarili:
            # Bilgileri kaydet ve forma döndür
            self.kullanici_adi = kullanici_adi
            self.sifre = sifre
            self.accept()
        else:
            self.lbl_hata.setText(mesaj)
            self.lbl_hata.setVisible(True) 