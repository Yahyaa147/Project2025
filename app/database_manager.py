import sqlite3
import threading
from contextlib import contextmanager

DB_FILE = 'parfum_koleksiyonu.db'
SCHEMA_VERSION = 2  # Increment this when schema changes

class DatabaseManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DatabaseManager, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self, db_path=DB_FILE):
        if self._initialized:
            return
        self._initialized = True
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
        self._ensure_meta_table()
        self._migrate_schema()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Enable dictionary-like access to rows
            self.cursor = self.conn.cursor()
            print(f"Database connection successful: {self.db_path}")
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise

    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

    def create_tables(self):
        if not self.cursor:
            print("Cursor not available. Cannot create tables.")
            return
        try:
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
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS markalar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                marka_adi TEXT NOT NULL UNIQUE
            )
            ''')
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS turler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tur_adi TEXT NOT NULL UNIQUE
            )
            ''')
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS parfumler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kullanici_id INTEGER NOT NULL,
                ad TEXT NOT NULL,
                marka_id INTEGER,
                tur_id INTEGER,
                boyut_ml REAL,
                kalan_miktar_ml REAL,
                edinme_tarihi TEXT,
                fiyat REAL,
                koku_notalari TEXT,
                sezon_onerisi TEXT,
                durum_onerisi TEXT,
                aciklama TEXT,
                foto_path TEXT,
                FOREIGN KEY (kullanici_id) REFERENCES kullanicilar (id),
                FOREIGN KEY (marka_id) REFERENCES markalar (id),
                FOREIGN KEY (tur_id) REFERENCES turler (id)
            )
            ''')
            self.conn.commit()
            print("Tables checked/created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
            raise

    def _ensure_meta_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS meta (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        self.conn.commit()
        # Set version if not present
        self.cursor.execute("SELECT value FROM meta WHERE key = 'schema_version'")
        row = self.cursor.fetchone()
        if not row:
            self.cursor.execute("INSERT INTO meta (key, value) VALUES (?, ?)", ('schema_version', '1'))
            self.conn.commit()

    def _get_schema_version(self):
        self.cursor.execute("SELECT value FROM meta WHERE key = 'schema_version'")
        row = self.cursor.fetchone()
        return int(row['value']) if row else 1

    def _set_schema_version(self, version):
        self.cursor.execute("UPDATE meta SET value = ? WHERE key = 'schema_version'", (str(version),))
        self.conn.commit()

    def _migrate_schema(self):
        version = self._get_schema_version()
        if version < 2:
            # Migration: Add parola_hash column if missing
            self.cursor.execute("PRAGMA table_info(kullanicilar)")
            columns = [row['name'] for row in self.cursor.fetchall()]
            if 'parola_hash' not in columns:
                self.cursor.execute("ALTER TABLE kullanicilar ADD COLUMN parola_hash TEXT")
                self.conn.commit()
            # This part below should only copy existing passwords if they were stored unhashed in 'parola'
            # If the original schema had 'parola' column which was text and contained plain passwords,
            # then this would be used to hash them.
            # Assuming 'parola' might not exist or passwords were already hashed,
            # this update might not be strictly necessary for a fresh run,
            # but is good for migration from an older schema.
            # self.cursor.execute("UPDATE kullanicilar SET parola_hash = parola WHERE parola_hash IS NULL OR parola_hash = ''")
            # self.conn.commit()
            self._set_schema_version(2)

    @contextmanager
    def get_cursor(self):
        try:
            yield self.cursor
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    # Removed duplicated close method 