import sqlite3
import bcrypt
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                            QLabel, QLineEdit, QPushButton, QMessageBox, 
                            QFrame, QGraphicsDropShadowEffect, QSpacerItem,
                            QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QSize
from PyQt5.QtGui import QFont, QPixmap, QIcon, QColor
from app.database_manager import DatabaseManager

class LoginForm(QDialog):
    # Başarılı giriş için sinyal - kullanıcı bilgilerini gönderecek
    login_success = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super(LoginForm, self).__init__(parent)
        print("LoginForm.__init__ başladı")
        self.setup_ui()
        self.setup_connections()
        print("LoginForm.__init__ UI ve bağlantılar kuruldu")
        
        # AUTO_LOGIN devre dışı - otomatik giriş yapmayı engelle
        self.AUTO_LOGIN = False
        
        # DEBUG: Arayüz öğelerinin boş olduğunu kontrol et
        print(f"Giriş formu oluşturulduğunda username_input: '{self.username_input.text()}'")
        print(f"Giriş formu oluşturulduğunda password_input: '{self.password_input.text()}'")
        
        # QLineEdit değişikliklerini izle
        # self.username_input.textChanged.connect(self._username_changed)
        # self.password_input.textChanged.connect(self._password_changed)
        
        # Veritabanı bağlantısı oluştur
        try:
            print("Veritabanı bağlantısı kuruluyor...")
            self.db = DatabaseManager()
            self.conn = self.db.conn
            self.cursor = self.db.cursor
            print("Veritabanı bağlantısı kuruldu")
            
            # Kullanıcılar tablosunu kontrol et ve yoksa oluştur
            self.create_users_table()
            
            # Otomatik giriş devre dışı (debug için)
            if self.AUTO_LOGIN:
                print("OTOMATİK GİRİŞ YAPILIYOR! (DEBUG)")
                self.username_input.setText("yahya")
                self.password_input.setText("123456")
                self.login()
            
        except Exception as e:
            import traceback
            print(f"Veritabanı bağlantı hatası: {e}\n{traceback.format_exc()}")
            QMessageBox.critical(self, "Veritabanı Hatası", f"Veritabanı bağlantısı sırasında hata oluştu: {e}")
    
    def _username_changed(self, text):
        """Kullanıcı adı değiştiğinde izlemek için"""
        print(f"Username değişti: '{text}'")
    
    def _password_changed(self, text):
        """Şifre değiştiğinde izlemek için"""
        print(f"Password değişti: '{text}'")
    
    def setup_ui(self):
        """Kullanıcı arayüzünü oluşturur"""
        # Temel pencere ayarları
        self.setWindowTitle("Parfüm Koleksiyonu")
        self.setFixedSize(480, 650)  # Genişliği ve yüksekliği arttırdım
        
        # Genel stil tanımları - basit tutuldu
        self.setStyleSheet("""
            QDialog {
                background-color: #1a2234;
            }
        """)
        
        # Ana Layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)  # Kenar boşluklarını arttırdım
        main_layout.setSpacing(30)  # Aradaki boşluğu arttırdım
        
        # ---- BAŞLIK KISMI ----
        # Logo ve başlık yan yana
        header_layout = QHBoxLayout()
        
        # Logo
        logo_label = QLabel()
        logo_label.setFixedSize(55, 55)  # Logo boyutunu arttırdım
        logo_label.setStyleSheet("""
            background-color: #10b981;
            border-radius: 10px;
        """)
        
        # Logo içindeki ikon
        icon_label = QLabel("👤", logo_label)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("""
            color: #1a2234;
            font-size: 26px;  /* Font boyutunu arttırdım */
            background-color: transparent;
        """)
        icon_label.setGeometry(0, 0, 55, 55)
        
        header_layout.addWidget(logo_label)
        header_layout.addSpacing(20)  # Boşluğu arttırdım
        
        # Başlık ve alt başlık dikey olarak
        title_layout = QVBoxLayout()
        title_layout.setSpacing(5)  # Boşluğu arttırdım
        
        # Başlık içeriği
        title = QLabel("Parfüm Koleksiyonu")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))  # Font boyutunu küçülttüm
        title.setStyleSheet("color: white;")
        title.setWordWrap(True)
        title_layout.addWidget(title)
        
        # Alt başlık
        subtitle = QLabel("Kişisel koleksiyon uygulamanıza giriş yapın")
        subtitle.setFont(QFont("Segoe UI", 12))  # Font boyutunu arttırdım
        subtitle.setStyleSheet("color: #a0aec0;")
        subtitle.setWordWrap(True)
        subtitle.setMinimumWidth(260)  # Minimum genişlik ekledim
        subtitle.setMinimumHeight(25)  # Minimum yükseklik ekledim
        
        title_layout.addWidget(subtitle)
        
        header_layout.addLayout(title_layout)
        
        main_layout.addLayout(header_layout)
        main_layout.addSpacing(25)  # Boşluğu arttırdım
        
        # ---- GİRİŞ FORMU ----
        # İç kart bölgesi
        login_card = QFrame()
        login_card.setStyleSheet("""
            background-color: #1f2a45;
            border-radius: 12px;  /* Köşe yuvarlaklığını arttırdım */
            border: 1px solid #2d3748;  /* Kenar çizgisi ekledim */
        """)
        
        # Kart içeriği
        card_layout = QVBoxLayout(login_card)
        card_layout.setContentsMargins(25, 30, 25, 30)  # Kenar boşluklarını arttırdım
        card_layout.setSpacing(20)  # Boşluğu arttırdım
        
        # Hoş geldiniz başlığı
        welcome_label = QLabel("HOŞ GELDİNİZ")
        welcome_label.setFont(QFont("Segoe UI", 22, QFont.Bold))  # Font boyutunu arttırdım
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("color: white;")
        welcome_label.setMinimumHeight(45)  # Minimum yüksekliği arttırdım
        card_layout.addWidget(welcome_label)
        card_layout.addSpacing(20)  # Boşluğu arttırdım
        
        # Form alanları - kullanıcı adı
        username_label = QLabel("Kullanıcı Adı")
        username_label.setFont(QFont("Segoe UI", 13))  # Font boyutunu arttırdım
        username_label.setStyleSheet("color: white;")
        username_label.setMinimumHeight(25)  # Minimum yükseklik ekledim
        card_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Kullanıcı adınızı girin")
        self.username_input.setFont(QFont("Segoe UI", 14))  # Font boyutunu arttırdım
        self.username_input.setMinimumHeight(52)  # Yüksekliği arttırdım
        self.username_input.setStyleSheet("""
            background-color: #1f2a45;
            color: white;
            border: 2px solid #3d4659;  /* Kenarlık kalınlığını arttırdım */
            border-radius: 6px;  /* Köşe yuvarlaklığını arttırdım */
            padding: 10px 15px;  /* İç boşluğu arttırdım */
            selection-background-color: #4299e1;
            selection-color: white;
        """)
        # Placeholder rengi için CSS ayarı
        self.username_input.setStyleSheet(self.username_input.styleSheet() + """
            QLineEdit::placeholder {
                color: #8a94a8;
            }
        """)
        self.username_input.setProperty("cursorWidth", 2)
        card_layout.addWidget(self.username_input)
        card_layout.addSpacing(30)  # Kullanıcı adı ve şifre arası mesafe genişletildi
        
        # Form alanları - şifre
        password_label = QLabel("Şifre")
        password_label.setFont(QFont("Segoe UI", 13))  # Font boyutunu arttırdım
        password_label.setStyleSheet("color: white;")
        password_label.setMinimumHeight(25)  # Minimum yükseklik ekledim
        card_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Şifrenizi girin")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Segoe UI", 14))  # Font boyutunu arttırdım
        self.password_input.setMinimumHeight(52)  # Yüksekliği arttırdım
        self.password_input.setStyleSheet("""
            background-color: #1f2a45;
            color: white;
            border: 2px solid #3d4659;  /* Kenarlık kalınlığını arttırdım */
            border-radius: 6px;  /* Köşe yuvarlaklığını arttırdım */
            padding: 10px 15px;  /* İç boşluğu arttırdım */
            selection-background-color: #4299e1;
            selection-color: white;
        """)
        # Placeholder rengi için CSS ayarı
        self.password_input.setStyleSheet(self.password_input.styleSheet() + """
            QLineEdit::placeholder {
                color: #8a94a8;
            }
        """)
        self.password_input.setProperty("cursorWidth", 2)
        card_layout.addWidget(self.password_input)
        card_layout.addSpacing(20)  # Boşluğu arttırdım
        
        # Hata mesajı
        self.error_label = QLabel()
        self.error_label.setStyleSheet("""
            color: #fc8181; 
            font-size: 14px;
            background-color: rgba(252, 129, 129, 0.1);
            border-radius: 4px;
            padding: 8px;
        """)
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setText("Kullanıcı adı veya şifre hatalı!")
        self.error_label.setMinimumHeight(40)  # Daha yüksek
        self.error_label.setVisible(False)
        self.error_label.setWordWrap(True)
        card_layout.addWidget(self.error_label)
        
        # Butonlar
        self.login_button = QPushButton("Giriş Yap")
        self.login_button.setFont(QFont("Segoe UI", 15, QFont.Bold))  # Font boyutunu arttırdım
        self.login_button.setMinimumHeight(54)  # Yüksekliği arttırdım
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.setStyleSheet("""
            background-color: #4299e1;
            color: white;
            border: none;
            border-radius: 6px;  /* Köşe yuvarlaklığını arttırdım */
            padding: 12px;
            font-weight: bold;
        """)
        card_layout.addWidget(self.login_button)
        card_layout.addSpacing(15)  # Daha fazla boşluk ekledim
        
        self.register_button = QPushButton("Yeni Hesap Oluştur")
        self.register_button.setFont(QFont("Segoe UI", 15, QFont.Bold))  # Font boyutunu arttırdım
        self.register_button.setMinimumHeight(54)  # Yüksekliği arttırdım
        self.register_button.setCursor(Qt.PointingHandCursor)
        self.register_button.setStyleSheet("""
            background-color: #10b981;
            color: white;
            border: none;
            border-radius: 6px;  /* Köşe yuvarlaklığını arttırdım */
            padding: 12px;
            font-weight: bold;
        """)
        card_layout.addWidget(self.register_button)
        
        main_layout.addWidget(login_card)
    
    def setup_connections(self):
        """Buton ve diğer bağlantıları kurar"""
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.show_register_form)
        self.password_input.returnPressed.connect(self.login)
        self.username_input.returnPressed.connect(self.login)
    
    def create_users_table(self):
        """Kullanıcılar tablosunu oluşturur"""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS kullanicilar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kullanici_adi TEXT NOT NULL UNIQUE,
            parola_hash TEXT NOT NULL,
            ad_soyad TEXT,
            email TEXT,
            kayit_tarihi DATE DEFAULT CURRENT_DATE,
            son_giris_tarihi DATE
        )
        ''')
        self.conn.commit()
        
        # Mevcut kullanıcıları kontrol etmek için debug çıktısı
        print("Kullanıcılar tablosu kontrol ediliyor...")
        
        try:
            # Tüm kullanıcıları listele
            self.cursor.execute("SELECT kullanici_adi, parola_hash FROM kullanicilar")
            users = self.cursor.fetchall()
            
            if users:
                print(f"Toplam {len(users)} kullanıcı bulundu.")
                for user in users:
                    print(f"Kullanıcı: {user['kullanici_adi']}, Şifre: {user['parola_hash']}")
            else:
                print("Hiç kullanıcı bulunamadı.")
        
        except sqlite3.Error as e:
            print(f"Veritabanı hatası: {e}")
            QMessageBox.critical(self, "Veritabanı Hatası", f"Veritabanı bağlantısı sırasında hata oluştu: {e}")
    
    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        if not username or not password:
            QMessageBox.warning(self, "Hata", "Lütfen kullanıcı adı ve şifre girin!")
            return
        try:
            self.cursor.execute(
                "SELECT id, kullanici_adi, parola_hash, ad_soyad, email FROM kullanicilar WHERE kullanici_adi = ?",
                (username,)
            )
            user = self.cursor.fetchone()
            if user:
                parola_hash = user['parola_hash']
                # Try bcrypt check first
                try:
                    if bcrypt.checkpw(password.encode('utf-8'), parola_hash.encode('utf-8')):
                        valid = True
                    else:
                        valid = False
                except ValueError:
                    # Not a valid bcrypt hash, fallback to plain text check
                    if password == parola_hash:
                        # Re-hash and update
                        new_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                        self.cursor.execute("UPDATE kullanicilar SET parola_hash = ? WHERE id = ?", (new_hash, user['id']))
                        self.conn.commit()
                        valid = True
                    else:
                        valid = False
                if valid:
                    self.cursor.execute(
                        "UPDATE kullanicilar SET son_giris_tarihi = CURRENT_DATE WHERE id = ?",
                        (user['id'],)
                    )
                    self.conn.commit()
                    user_info = {
                        'kullanici_id': user['id'],
                        'kullanici_adi': user['kullanici_adi'],
                        'ad_soyad': user['ad_soyad'],
                        'email': user['email']
                    }
                    self.user_info = user_info
                    self.login_success.emit(user_info)
                    self.accept()
                else:
                    QMessageBox.warning(self, "Hata", "Kullanıcı adı veya şifre hatalı!")
            else:
                QMessageBox.warning(self, "Hata", "Kullanıcı adı veya şifre hatalı!")
        except Exception as e:
            import traceback
            print(f"Girişte hata: {e}\n{traceback.format_exc()}")
            QMessageBox.critical(self, "Veritabanı Hatası", f"Giriş sırasında bir hata oluştu. Lütfen tekrar deneyin.")
    
    def show_register_form(self):
        """Kayıt formunu gösterir"""
        register_dialog = RegisterForm(self)
        if register_dialog.exec_() == QDialog.Accepted:
            # Başarılı kayıt sonrası kullanıcı adını doldur
            self.username_input.setText(register_dialog.username)
            self.password_input.setText(register_dialog.password)
    
    def closeEvent(self, event):
        """Dialog kapatıldığında veritabanı bağlantısını kapatır"""
        if hasattr(self, 'conn'):
            self.conn.close()
        event.accept()


class RegisterForm(QDialog):
    def __init__(self, parent=None):
        super(RegisterForm, self).__init__(parent)
        self.conn = parent.conn
        self.cursor = parent.cursor
        self.username = ""
        self.password = ""
        self.setup_ui()
        self.setup_connections()
    
    def setup_ui(self):
        """Kullanıcı arayüzünü oluşturur"""
        # Temel pencere ayarları
        self.setWindowTitle("Yeni Hesap Oluştur")
        self.setFixedSize(450, 680)  # Genişliği arttırdım
        
        # Genel stil tanımları
        self.setStyleSheet("""
            QDialog {
                background-color: #1a2234;
            }
        """)
        
        # Ana Layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)
        
        # ---- BAŞLIK KISMI ----
        # Logo ve başlık yan yana
        header_layout = QHBoxLayout()
        
        # Logo
        logo_label = QLabel()
        logo_label.setFixedSize(45, 45)
        logo_label.setStyleSheet("""
            background-color: #10b981;
            border-radius: 8px;
        """)
        
        # Logo içindeki ikon
        icon_label = QLabel("👤", logo_label)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("""
            color: #1a2234;
            font-size: 22px;
            background-color: transparent;
        """)
        icon_label.setGeometry(0, 0, 45, 45)
        
        header_layout.addWidget(logo_label)
        header_layout.addSpacing(15)
        
        # Başlık ve alt başlık dikey olarak
        title_layout = QVBoxLayout()
        title_layout.setSpacing(5)  # Biraz arttırdım
        
        # Başlık içeriği
        title = QLabel("Yeni Hesap Oluştur")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: white;")
        title.setMinimumWidth(250)  # Minimum genişlik ekledim
        
        # Alt başlık
        subtitle = QLabel("Kişisel koleksiyon uygulamanız için hesap oluşturun")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet("color: #a0aec0;")
        subtitle.setWordWrap(True)
        subtitle.setMinimumWidth(250)  # Minimum genişlik ekledim
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        
        header_layout.addLayout(title_layout)
        
        main_layout.addLayout(header_layout)
        main_layout.addSpacing(15)
        
        # ---- KAYIT FORMU ----
        # İç kart bölgesi
        register_card = QFrame()
        register_card.setStyleSheet("""
            background-color: #1f2a45;
            border-radius: 8px;
        """)
        
        # Form içeriği - QFormLayout kullan
        form_layout = QVBoxLayout(register_card)
        form_layout.setContentsMargins(20, 25, 20, 25)
        form_layout.setSpacing(15)
        
        # Form başlığı
        form_title = QLabel("Kullanıcı Bilgileri")
        form_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        form_title.setAlignment(Qt.AlignCenter)
        form_title.setStyleSheet("color: white;")
        form_title.setMinimumHeight(40)  # Minimum yükseklik
        form_layout.addWidget(form_title)
        form_layout.addSpacing(20)
        
        # Kullanıcı adı
        username_label = QLabel("Kullanıcı Adı")
        username_label.setFont(QFont("Segoe UI", 12))
        username_label.setStyleSheet("color: white;")
        form_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Kullanıcı adınızı girin")
        self.username_input.setFont(QFont("Segoe UI", 13))
        self.username_input.setMinimumHeight(48)
        self.username_input.setStyleSheet("""
            background-color: #1f2a45;
            color: white;
            border: 1px solid #3d4659;
            border-radius: 4px;
            padding: 8px 12px;
            selection-background-color: #4299e1;
            selection-color: white;
        """)
        # Placeholder rengi için CSS ayarı
        self.username_input.setStyleSheet(self.username_input.styleSheet() + """
            QLineEdit::placeholder {
                color: #8a94a8;
            }
        """)
        self.username_input.setProperty("cursorWidth", 2)
        form_layout.addWidget(self.username_input)
        form_layout.addSpacing(15)
        
        # Şifre
        password_label = QLabel("Şifre")
        password_label.setFont(QFont("Segoe UI", 12))
        password_label.setStyleSheet("color: white;")
        form_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Şifrenizi girin")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Segoe UI", 13))
        self.password_input.setMinimumHeight(48)
        self.password_input.setStyleSheet("""
            background-color: #1f2a45;
            color: white;
            border: 1px solid #3d4659;
            border-radius: 4px;
            padding: 8px 12px;
            selection-background-color: #4299e1;
            selection-color: white;
        """)
        # Placeholder rengi için CSS ayarı
        self.password_input.setStyleSheet(self.password_input.styleSheet() + """
            QLineEdit::placeholder {
                color: #8a94a8;
            }
        """)
        self.password_input.setProperty("cursorWidth", 2)
        form_layout.addWidget(self.password_input)
        form_layout.addSpacing(15)
        
        # Ad Soyad
        fullname_label = QLabel("Ad Soyad (İsteğe bağlı)")
        fullname_label.setFont(QFont("Segoe UI", 12))
        fullname_label.setStyleSheet("color: white;")
        form_layout.addWidget(fullname_label)
        
        self.fullname_input = QLineEdit()
        self.fullname_input.setPlaceholderText("Adınızı ve soyadınızı girin")
        self.fullname_input.setFont(QFont("Segoe UI", 13))
        self.fullname_input.setMinimumHeight(48)  # Daha yüksek
        self.fullname_input.setStyleSheet("""
            background-color: #1f2a45;
            color: white;
            border: 1px solid #3d4659;
            border-radius: 4px;
            padding: 8px 12px;
            selection-background-color: #4299e1;
            selection-color: white;
        """)
        # Placeholder rengi için CSS ayarı
        self.fullname_input.setStyleSheet(self.fullname_input.styleSheet() + """
            QLineEdit::placeholder {
                color: #8a94a8;
            }
        """)
        self.fullname_input.setProperty("cursorWidth", 2)  # İmleç genişliği
        form_layout.addWidget(self.fullname_input)
        form_layout.addSpacing(15)
        
        # E-posta
        email_label = QLabel("E-posta (İsteğe bağlı)")
        email_label.setFont(QFont("Segoe UI", 12))
        email_label.setStyleSheet("color: white;")
        form_layout.addWidget(email_label)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-posta adresinizi girin")
        self.email_input.setFont(QFont("Segoe UI", 13))
        self.email_input.setMinimumHeight(48)  # Daha yüksek
        self.email_input.setStyleSheet("""
            background-color: #1f2a45;
            color: white;
            border: 1px solid #3d4659;
            border-radius: 4px;
            padding: 8px 12px;
            selection-background-color: #4299e1;
            selection-color: white;
        """)
        # Placeholder rengi için CSS ayarı
        self.email_input.setStyleSheet(self.email_input.styleSheet() + """
            QLineEdit::placeholder {
                color: #8a94a8;
            }
        """)
        self.email_input.setProperty("cursorWidth", 2)  # İmleç genişliği
        form_layout.addWidget(self.email_input)
        form_layout.addSpacing(20)
        
        # Hata mesajı
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: #fc8181; font-size: 13px;")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setMinimumHeight(30)  # Daha yüksek
        self.error_label.setVisible(False)
        self.error_label.setWordWrap(True)
        form_layout.addWidget(self.error_label)
        
        # Buton grupları için yatay layout - BU KISMI DEĞİŞTİRDİM
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)  # Yatay boşluk
        
        # Vazgeç butonu
        self.cancel_button = QPushButton("Vazgeç")
        self.cancel_button.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.cancel_button.setFixedHeight(50)  # Yüksekliği arttırdım
        self.cancel_button.setCursor(Qt.PointingHandCursor)
        self.cancel_button.setStyleSheet("""
            background-color: #4299e1;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 10px;
        """)
        buttons_layout.addWidget(self.cancel_button, 1)  # 1 ağırlık
        
        # Hesap oluştur butonu
        self.register_button = QPushButton("Hesap Oluştur")
        self.register_button.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.register_button.setFixedHeight(50)  # Yüksekliği arttırdım
        self.register_button.setCursor(Qt.PointingHandCursor)
        self.register_button.setStyleSheet("""
            background-color: #10b981;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 10px;
        """)
        buttons_layout.addWidget(self.register_button, 1)  # 1 ağırlık
        
        form_layout.addLayout(buttons_layout)
        
        # Ana layout'a form kartını ekle
        main_layout.addWidget(register_card)
    
    def setup_connections(self):
        """Buton bağlantılarını kurar"""
        self.register_button.clicked.connect(self.register)
        self.cancel_button.clicked.connect(self.reject)
    
    def register(self):
        """Yeni kullanıcı kaydeder"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        fullname = self.fullname_input.text().strip()
        email = self.email_input.text().strip()
        if not username or not password:
            self.error_label.setText("Kullanıcı adı ve şifre zorunludur!")
            self.error_label.setVisible(True)
            return
        try:
            self.cursor.execute("SELECT COUNT(*) as count FROM kullanicilar WHERE kullanici_adi = ?", (username,))
            result = self.cursor.fetchone()
            if result['count'] > 0:
                self.error_label.setText("Bu kullanıcı adı zaten kullanılıyor!")
                self.error_label.setVisible(True)
                return
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            self.cursor.execute(
                "INSERT INTO kullanicilar (kullanici_adi, parola_hash, ad_soyad, email) VALUES (?, ?, ?, ?)",
                (username, password_hash.decode('utf-8'), fullname, email)
            )
            self.conn.commit()
            self.username = username
            self.password = password
            QMessageBox.information(self, "Başarılı", "Hesabınız başarıyla oluşturuldu!")
            self.accept()
        except Exception as e:
            import traceback
            print(f"Kayıtta hata: {e}\n{traceback.format_exc()}")
            self.error_label.setText("Kayıt sırasında bir hata oluştu. Lütfen tekrar deneyin.")
            self.error_label.setVisible(True) 