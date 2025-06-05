import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QFont
from app.login_form import LoginForm
from app.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set app font
    font = QFont("Segoe UI", 11)
    # app.setFont(font)
    
    print("Creating login window...")
    
    try:
        # Create and show login form as a modal dialog
        login_dialog = LoginForm()
        
        # Show the login form modally (blocks until user closes it)
        print("Running login dialog modally...")
        result = login_dialog.exec_()
        print(f"Login dialog result: {result}")
        
        # Check if login was successful
        if result == LoginForm.Accepted:
            print("Login accepted, opening main window...")
            user_info = getattr(login_dialog, 'user_info', None)
            if user_info is None and hasattr(login_dialog, 'get_user_info'):
                user_info = login_dialog.get_user_info()
            main_window = MainWindow(user_info=user_info)
            main_window.show()
            sys.exit(app.exec_())
        else:
            print("Login canceled or failed")
            sys.exit(0)
            
    except Exception as e:
        print(f"Error: {e}")
        QMessageBox.critical(None, "Error", f"An error occurred: {str(e)}")
        sys.exit(1) 