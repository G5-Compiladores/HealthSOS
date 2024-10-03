# db.py
import sqlite3

def initialize_database():
    # Conectar a la base de datos (se crea si no existe)
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    # Crear tabla para usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        hashed_password TEXT NOT NULL
    )
    ''')

    # Crear tabla para formularios de salud
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS health_forms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        alergias BOOLEAN,
        alergias_medicamentos BOOLEAN,
        medicamentos_actuales TEXT,
        diabetes BOOLEAN,
        marcapasos BOOLEAN,
        epilepsia BOOLEAN,
        grupo_sanguineo TEXT,
        enfermedades_cardiacas BOOLEAN,
        enfermedades_respiratorias BOOLEAN,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')

    # Guardar (commit) los cambios y cerrar la conexión
    conn.commit()
    conn.close()
