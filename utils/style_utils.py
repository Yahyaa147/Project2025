from PyQt5.QtWidgets import QLabel, QTableView
from PyQt5.QtGui import QFont, QIcon

def apply_stylesheet(window):
    """Modern stil sayfasını ana pencereye uygular"""
    # Ana pencere stili
    window.setStyleSheet("""
        QMainWindow {
            background-color: #f5f5f5;
        }
        QLabel {
            font-size: 12px;
            font-weight: bold;
            color: #333;
        }
        QLineEdit, QTextEdit, QComboBox, QDoubleSpinBox, QDateEdit {
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 6px;
            background-color: white;
            min-height: 25px;
        }
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
            border: 1px solid #4a90e2;
        }
        QPushButton {
            background-color: #4a90e2;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
            min-width: 120px;
            min-height: 30px;
        }
        QPushButton:hover {
            background-color: #357ab7;
        }
        QPushButton:pressed {
            background-color: #2a5885;
        }
        QTableView {
            border: 1px solid #ddd;
            border-radius: 4px;
            background-color: white;
            selection-background-color: #4a90e2;
            selection-color: white;
            alternate-background-color: #f9f9f9;
        }
        QTableView::item {
            padding: 4px;
        }
        QHeaderView::section {
            background-color: #e0e0e0;
            padding: 6px;
            border: none;
            border-right: 1px solid #ccc;
            font-weight: bold;
        }
        QSplitter::handle {
            background-color: #ddd;
        }
        QScrollBar:vertical {
            border: none;
            background: #f0f0f0;
            width: 10px;
            margin: 0px;
        }
        QScrollBar::handle:vertical {
            background: #c0c0c0;
            min-height: 20px;
            border-radius: 5px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            border: none;
            background: none;
            height: 0px;
        }
    """)

def create_custom_button(text, icon_name=None, color=None):
    """Özel stillendirilmiş buton oluşturur"""
    from PyQt5.QtWidgets import QPushButton
    
    button = QPushButton(text)
    
    # İkon ekle
    if icon_name:
        button.setIcon(QIcon.fromTheme(icon_name))
        
    # Özel renk tanımla
    if color:
        button.setStyleSheet(f"background-color: {color}; min-width: 140px;")
    
    # İmleci değiştir
    from PyQt5.QtCore import Qt
    button.setCursor(Qt.PointingHandCursor)
    
    return button

def create_title_label(text):
    """Başlık stili uygulanmış etiket oluşturur"""
    label = QLabel(text)
    
    # Stil uygula
    label.setStyleSheet("""
        font-size: 24px;
        font-weight: bold;
        color: #4a90e2;
        margin: 10px;
        padding: 5px;
    """)
    
    # Hizalama
    from PyQt5.QtCore import Qt
    label.setAlignment(Qt.AlignCenter)
    
    return label

def create_form_label(text):
    """Form etiketi oluşturur"""
    label = QLabel(text)
    
    # Stil ve hizalama
    from PyQt5.QtCore import Qt
    label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    label.setStyleSheet("font-weight: bold;")
    
    return label

def setup_table_view(table_view):
    """Tablo görünümünü düzenler"""
    # Tablo özellikleri
    table_view.setAlternatingRowColors(True)
    
    # Başlık özellikleri
    from PyQt5.QtWidgets import QHeaderView
    table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    table_view.verticalHeader().setVisible(False)
    
    # Seçim davranışı
    from PyQt5.QtWidgets import QAbstractItemView
    table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
    table_view.setSelectionMode(QAbstractItemView.SingleSelection)
    
    return table_view 