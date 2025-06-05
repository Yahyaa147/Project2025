import sqlite3
import bcrypt

class UserController:
    def __init__(self, db_conn):
        self.conn = db_conn
        self.cursor = self.conn.cursor()

    def get_user_by_id(self, user_id):
        self.cursor.execute("SELECT id, kullanici_adi, ad_soyad, email, parola_hash FROM kullanicilar WHERE id = ?", (user_id,))
        return self.cursor.fetchone()

    def update_user_profile(self, user_id, username, current_password, new_password, email, fullname):
        try:
            # Fetch current user data to verify current password
            user_data = self.get_user_by_id(user_id)
            if not user_data:
                return False, "Kullanıcı bulunamadı."

            # Verify current password if provided
            if current_password:
                if not bcrypt.checkpw(current_password.encode('utf-8'), user_data['parola_hash'].encode('utf-8')):
                    return False, "Mevcut şifre yanlış."
            elif new_password: # If new password is provided, current password must be entered
                return False, "Yeni şifre belirlemek için mevcut şifrenizi girmeniz gerekmektedir."

            # Prepare update query
            update_fields = ["kullanici_adi = ?", "ad_soyad = ?", "email = ?"]
            update_values = [username, fullname, email]

            if new_password:
                new_password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                update_fields.append("parola_hash = ?")
                update_values.append(new_password_hash.decode('utf-8'))

            query = f"UPDATE kullanicilar SET {', '.join(update_fields)} WHERE id = ?"
            update_values.append(user_id)

            self.cursor.execute(query, tuple(update_values))
            self.conn.commit()
            return True, "Profil başarıyla güncellendi."

        except Exception as e:
            print(f"Profil güncelleme hatası: {e}")
            return False, f"Profil güncellenirken bir hata oluştu: {str(e)}" 