from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap

class AboutPage(QWidget):
    def __init__(self):
        super(AboutPage, self).__init__()
        
        # Ana layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(30)
        self.main_layout.setAlignment(Qt.AlignCenter)
        
        # Başlık
        self.title_label = QLabel("PARFÜM KOLEKSİYONU YÖNETİMİ")
        self.title_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #3b82f6;
        """)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label)
        
        # Logo ve açıklama
        logo_container = QHBoxLayout()
        logo_container.setAlignment(Qt.AlignCenter)
        
        # Logo (isteğe bağlı)
        self.logo_label = QLabel()
        # self.logo_label.setPixmap(QPixmap("resources/icons/perfume.png").scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo_label.setAlignment(Qt.AlignCenter)
        logo_container.addWidget(self.logo_label)
        
        self.main_layout.addLayout(logo_container)
        
        # Sürüm bilgisi
        self.version_label = QLabel("Sürüm 1.0")
        self.version_label.setStyleSheet("""
            font-size: 16px;
            color: #64748b;
        """)
        self.version_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.version_label)
        
        # Açıklama
        self.description_label = QLabel(
            """
            <p>Bu uygulama, parfüm koleksiyonunuzu yönetmek için geliştirilmiş bir masaüstü uygulamasıdır.</p>
            <p>Aşağıdaki özelliklere sahiptir:</p>
            <ul>
                <li>Koleksiyonunuzdaki parfümleri listeleme ve arama</li>
                <li>Yeni parfüm ekleme ve mevcut parfümleri düzenleme</li>
                <li>Parfüm bilgilerini detaylı görüntüleme</li>
                <li>Marka ve tür yönetimi</li>
                <li>Fotoğraflarla parfüm şişelerini görüntüleme</li>
            </ul>
            <p>Uygulama Python ve PyQt5 kullanılarak geliştirilmiştir.</p>
            """
        )
        self.description_label.setStyleSheet("""
            font-size: 16px;
            color: #334155;
            line-height: 1.6;
        """)
        self.description_label.setWordWrap(True)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.description_label)
        
        # Telif hakkı
        self.copyright_label = QLabel("© 2025 Programlamaya Giriş 2")
        self.copyright_label.setStyleSheet("""
            font-size: 14px;
            color: #94a3b8;
        """)
        self.copyright_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.copyright_label) 