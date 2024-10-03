import sqlite3
import bcrypt
import pandas as pd
import streamlit as st
from db import initialize_database  # Asegúrate de que este nombre coincide con tu función de inicialización
from password_utils import get_password_hash  # Importa tu función para hash de contraseñas

# Inicializa la base de datos
initialize_database()

# Función para hashear la contraseña
def get_password_hash(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# Función para crear un usuario
def create_user(email, password):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (email, hashed_password) VALUES (?, ?)", (email, get_password_hash(password)))
    conn.commit()
    conn.close()

# Función para crear un formulario de salud
def create_health_form(user_id, health_form_data):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute(""" 
    INSERT INTO health_forms (user_id, alergias, alergias_medicamentos, medicamentos_actuales,
                               diabetes, marcapasos, epilepsia, grupo_sanguineo,
                               enfermedades_cardiacas, enfermedades_respiratorias)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                   (user_id,
                    'Sí' if health_form_data['alergias'] else 'No',
                    health_form_data['alergias_medicamentos'] if health_form_data['alergias'] else None,
                    health_form_data['medicamentos_actuales'], 
                    'Sí' if health_form_data['diabetes'] else 'No',
                    'Sí' if health_form_data['marcapasos'] else 'No',
                    'Sí' if health_form_data['epilepsia'] else 'No',
                    health_form_data['grupo_sanguineo'],
                    health_form_data['enfermedades_cardiacas'] if health_form_data['enfermedades_cardiacas'] else None,
                    health_form_data['enfermedades_respiratorias'] if health_form_data['enfermedades_respiratorias'] else None))
    conn.commit()
    conn.close()

# Función para mostrar datos de usuarios y formularios de salud
def show_data():
    conn = sqlite3.connect('my_database.db')
    users_df = pd.read_sql_query("SELECT * FROM users", conn)
    health_forms_df = pd.read_sql_query("SELECT * FROM health_forms", conn)
    conn.close()

    st.subheader("Registros de Usuarios")
    st.dataframe(users_df)

    st.subheader("Formularios de Salud")
    st.dataframe(health_forms_df)

# Interfaz de usuario para registro
st.title("Registro de Usuario")
email = st.text_input("Email")
password = st.text_input("Contraseña", type="password")

if st.button("Registrar"):
    create_user(email, password)
    st.success("Usuario registrado exitosamente!")

# Interfaz de usuario para el formulario de salud
st.title("Formulario de Salud")

# Pregunta sobre alergias
alergias = st.checkbox("¿Tienes alergias a medicamentos?")
alergias_medicamentos = ""
if alergias:
    alergias_medicamentos = st.text_input("Especifica a qué medicamentos eres alérgico:")

# Pregunta sobre medicamentos actuales
medicamentos_actuales = st.text_input("Medicamentos actuales")

# Pregunta sobre diabetes
diabetes = st.checkbox("¿Tienes diabetes?")

# Pregunta sobre marcapasos
marcapasos = st.checkbox("¿Tienes marcapasos?")

# Pregunta sobre epilepsia
epilepsia = st.checkbox("¿Tienes epilepsia?")

# Pregunta sobre tipo sanguíneo
grupo_sanguineo = st.selectbox("Grupo sanguíneo", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])

# Preguntas sobre enfermedades
enfermedades_cardiacas = ""
if st.checkbox("¿Tienes enfermedades cardíacas?"):
    enfermedades_cardiacas = st.text_input("Especifica las enfermedades cardíacas que tienes:")

enfermedades_respiratorias = ""
if st.checkbox("¿Tienes enfermedades respiratorias?"):
    enfermedades_respiratorias = st.text_input("Especifica las enfermedades respiratorias que tienes:")

if st.button("Enviar Formulario"):
    # Aquí necesitarías el user_id que has creado en el registro
    user_id = 1  # Este debería ser el id del usuario registrado
    health_form_data = {
        'alergias': alergias,
        'alergias_medicamentos': alergias_medicamentos,
        'medicamentos_actuales': medicamentos_actuales,
        'diabetes': diabetes,
        'marcapasos': marcapasos,
        'epilepsia': epilepsia,
        'grupo_sanguineo': grupo_sanguineo,
        'enfermedades_cardiacas': enfermedades_cardiacas,
        'enfermedades_respiratorias': enfermedades_respiratorias
    }
    create_health_form(user_id, health_form_data)
    st.success("Formulario de salud enviado exitosamente!")

# Mostrar datos
if st.button("Mostrar Datos"):
    show_data()



