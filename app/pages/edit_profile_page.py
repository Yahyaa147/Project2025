from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class EditProfilePage(QWidget):
    def __init__(self, db_controller, user_info=None):
        super(EditProfilePage, self).__init__()
        self.db_controller = db_controller
        self.user_info = user_info if user_info is not None else {}
        self.kullanici_id = self.user_info.get('kullanici_id')

        self.setup_ui()
        self.load_user_data()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(20)
        self.main_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        title_label = QLabel("Profil Düzenle")
        title_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #3b82f6;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(title_label)

        # Kullanıcı Adı
        self.main_layout.addWidget(self.create_label("Kullanıcı Adı:"))
        self.username_input = self.create_line_edit("Kullanıcı adınızı girin")
        self.main_layout.addWidget(self.username_input)

        # Mevcut Şifre
        self.main_layout.addWidget(self.create_label("Mevcut Şifre (Değiştirmek için):"))
        self.current_password_input = self.create_line_edit("Mevcut şifrenizi girin", is_password=True)
        self.main_layout.addWidget(self.current_password_input)

        # Yeni Şifre
        self.main_layout.addWidget(self.create_label("Yeni Şifre (Boş bırakırsanız değişmez):"))
        self.new_password_input = self.create_line_edit("Yeni şifrenizi girin", is_password=True)
        self.main_layout.addWidget(self.new_password_input)

        # E-posta
        self.main_layout.addWidget(self.create_label("E-posta:"))
        self.email_input = self.create_line_edit("E-posta adresinizi girin")
        self.main_layout.addWidget(self.email_input)
        
        # Ad Soyad
        self.main_layout.addWidget(self.create_label("Ad Soyad:"))
        self.fullname_input = self.create_line_edit("Adınızı ve soyadınızı girin")
        self.main_layout.addWidget(self.fullname_input)

        # Butonlar
        self.save_button = self.create_button("Kaydet", "#10b981")
        self.save_button.clicked.connect(self.save_profile)
        self.main_layout.addWidget(self.save_button)

        self.cancel_button = self.create_button("İptal", "#ef4444")
        self.cancel_button.clicked.connect(self.cancel_edit)
        self.main_layout.addWidget(self.cancel_button)

        self.main_layout.addStretch()

    def create_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("font-size: 16px; font-weight: bold; color: #f8fafc;")
        return label

    def create_line_edit(self, placeholder, is_password=False):
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        line_edit.setMinimumHeight(40)
        line_edit.setStyleSheet("""
            border: 1px solid #475569;
            border-radius: 6px;
            padding: 8px;
            background-color: #334155;
            color: #f8fafc;
            font-size: 14px;
        """)
        if is_password:
            line_edit.setEchoMode(QLineEdit.Password)
        return line_edit

    def create_button(self, text, color):
        button = QPushButton(text)
        button.setStyleSheet(f"""
            background-color: {color};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 10px 18px;
            font-weight: bold;
            min-width: 120px;
            min-height: 36px;
            font-size: 14px;
        """)
        button.setCursor(Qt.PointingHandCursor)
        return button

    def load_user_data(self):
        if self.kullanici_id:
            user_data = self.db_controller.get_user_by_id(self.kullanici_id)
            if user_data:
                self.username_input.setText(user_data['kullanici_adi'])
                self.email_input.setText(user_data['email'])
                self.fullname_input.setText(user_data['ad_soyad'])
            else:
                QMessageBox.warning(self, "Hata", "Kullanıcı bilgileri yüklenemedi.")

    def save_profile(self):
        username = self.username_input.text().strip()
        current_password = self.current_password_input.text().strip()
        new_password = self.new_password_input.text().strip()
        email = self.email_input.text().strip()
        fullname = self.fullname_input.text().strip()

        if not username:
            QMessageBox.warning(self, "Hata", "Kullanıcı adı boş olamaz!")
            return

        if new_password and len(new_password) < 6:
            QMessageBox.warning(self, "Hata", "Yeni şifre en az 6 karakter olmalıdır!")
            return

        success, message = self.db_controller.update_user_profile(
            self.kullanici_id, username, current_password, new_password, email, fullname
        )

        if success:
            QMessageBox.information(self, "Başarılı", "Profiliniz başarıyla güncellendi!")
            # Update user_info in main window if needed
            self.user_info['kullanici_adi'] = username
            self.user_info['email'] = email
            self.user_info['ad_soyad'] = fullname
            # Clear password fields after successful update
            self.current_password_input.clear()
            self.new_password_input.clear()
        else:
            QMessageBox.warning(self, "Hata", message)

    def cancel_edit(self):
        # Simply re-load the data to discard changes
        self.load_user_data()
        self.current_password_input.clear()
        self.new_password_input.clear() 