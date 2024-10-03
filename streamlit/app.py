import streamlit as st
import requests
import os
import sqlite3
import bcrypt
import pandas as pd

API_URL = os.getenv("API_URL", "http://localhost:8000")

def register(email, password):
    response = requests.post(f"{API_URL}/register", json={"email": email, "password": password})
    return response.json()

def login(email, password):
    response = requests.post(f"{API_URL}/token", data={"username": email, "password": password})
    return response.json()

def submit_health_form(form_data, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_URL}/health-form", json=form_data, headers=headers)
    return response.json()

def get_chatbot_response(question):
    response = requests.post(f"{API_URL}/chatbot", json={"question": question})
    return response.json()

def initialize_database():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        hashed_password TEXT NOT NULL
    )
    ''')
    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS health_forms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        alergias BOOLEAN,
        alergias_medicamentos TEXT,
        medicamentos_actuales TEXT,
        diabetes BOOLEAN,
        marcapasos BOOLEAN,
        epilepsia BOOLEAN,
        grupo_sanguineo TEXT,
        enfermedades_cardiacas TEXT,
        enfermedades_respiratorias TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    conn.commit()
    conn.close()

def get_password_hash(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_user(email, password):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (email, hashed_password) VALUES (?, ?)", (email, get_password_hash(password)))
    conn.commit()
    conn.close()

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

def show_data():
    conn = sqlite3.connect('my_database.db')
    users_df = pd.read_sql_query("SELECT * FROM users", conn)
    health_forms_df = pd.read_sql_query("SELECT * FROM health_forms", conn)
    conn.close()
    st.subheader("Registros de Usuarios")
    st.dataframe(users_df)
    st.subheader("Formularios de Salud")
    st.dataframe(health_forms_df)

initialize_database()

st.title("HealthSOS - Health Form and Medical Chatbot")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    def login_admin():
        st.title("Inicio de Sesión")
        username_input = st.text_input("Usuario", type="default")
        password_input = st.text_input("Contraseña", type="password")

        if st.button("Iniciar Sesión"):
            if username_input == "admin" and password_input == "admin":
                st.session_state.authenticated = True
                st.success("Inicio de sesión exitoso.")
            else:
                st.error("Usuario o contraseña incorrectos.")

    login_admin()
else:
    st.header("Opciones del Administrador")
    new_email = st.text_input("Email del Nuevo Usuario")
    new_password = st.text_input("Contraseña del Nuevo Usuario", type="password")

    if st.button("Registrar Nuevo Usuario"):
        if new_email and new_password:
            create_user(new_email, new_password)
            st.success("Nuevo usuario registrado exitosamente!")
        else:
            st.error("Por favor, complete todos los campos.")

    sidebar_option = st.sidebar.radio("Elige una opción", ["Formulario de Salud", "Chatbot Médico", "Mostrar Datos"])
    
    if sidebar_option == "Formulario de Salud":
        st.subheader("Formulario de Salud")
        with st.form("health_form"):
            alergias = st.checkbox("¿Tienes alergias a medicamentos?")
            alergias_medicamentos = st.text_input("Especifica a qué medicamentos eres alérgico:", disabled=not alergias)

            medicamentos_actuales = st.selectbox("Medicamentos actuales", 
                ["Anticoagulantes", "Antiagregantes plaquetarios", "Betabloqueantes", 
                 "Diuréticos", "Antiarrítmicos", "Nitratos", 
                 "Insulina y otros antidiabéticos", "Corticosteroides", "Otro"],
                index=0)

            if medicamentos_actuales == "Otro":
                medicamentos_actuales = st.text_input("Especifica el medicamento:")

            diabetes = st.checkbox("¿Tienes diabetes?")
            marcapasos = st.checkbox("¿Tienes marcapasos?")
            epilepsia = st.checkbox("¿Tienes epilepsia?")
            grupo_sanguineo = st.selectbox("Grupo sanguíneo", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])

            enfermedades_cardiacas = st.checkbox("¿Tienes enfermedades cardíacas?")
            enfermedades_cardiacas_tipo = None
            if enfermedades_cardiacas:
                enfermedades_cardiacas_tipo = st.selectbox("Especifica la enfermedad cardíaca:",
                    ["Arritmias Cardiacas", "Insuficiencia Cardíaca", "Enfermedad de las Arterias Coronarias", 
                     "Disección Aórtica", "Otro"],
                    index=0)
                if enfermedades_cardiacas_tipo == "Otro":
                    enfermedades_cardiacas_tipo = st.text_input("Especifica la enfermedad cardíaca:")

            enfermedades_respiratorias = st.checkbox("¿Tienes enfermedades respiratorias?")
            enfermedades_respiratorias_tipo = None
            if enfermedades_respiratorias:
                enfermedades_respiratorias_tipo = st.selectbox("Especifica la enfermedad respiratoria:",
                    ["EPOC", "Asma", "Edema Pulmonar", "Neumonias", "Bronquiolitis", "Otro"],
                    index=0)
                if enfermedades_respiratorias_tipo == "Otro":
                    enfermedades_respiratorias_tipo = st.text_input("Especifica la enfermedad respiratoria:")

            submitted = st.form_submit_button("Enviar")
            
            if submitted:
                form_data = {
                    "alergias": alergias,
                    "alergias_medicamentos": alergias_medicamentos if alergias else None,
                    "medicamentos_actuales": medicamentos_actuales,
                    "diabetes": diabetes,
                    "marcapasos": marcapasos,
                    "epilepsia": epilepsia,
                    "grupo_sanguineo": grupo_sanguineo,
                    "enfermedades_cardiacas": enfermedades_cardiacas_tipo if enfermedades_cardiacas else None,
                    "enfermedades_respiratorias": enfermedades_respiratorias_tipo if enfermedades_respiratorias else None
                }
                user_id = 1
                create_health_form(user_id, form_data)
                st.success("Formulario de salud enviado exitosamente!")

    elif sidebar_option == "Chatbot Médico":
        st.header("Chatbot Médico")
        user_input = st.text_input("Haga una pregunta médica:")
        if st.button("Enviar"):
            response = get_chatbot_response(user_input)
            st.write(response['answer'])
    
    elif sidebar_option == "Mostrar Datos":
        show_data()

