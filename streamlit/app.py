import streamlit as st
import requests
import os

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

st.title("HealthSOS - Health Form and Medical Chatbot")

# Sidebar for login/register
sidebar_option = st.sidebar.radio("Choose an option", ["Login", "Register"])

if sidebar_option == "Login":
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        response = login(email, password)
        if "access_token" in response:
            st.session_state.token = response["access_token"]
            st.success("Logged in successfully!")
        else:
            st.error("Login failed. Please check your credentials.")

elif sidebar_option == "Register":
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Register"):
        response = register(email, password)
        if "email" in response:
            st.success("Registered successfully! Please login.")
        else:
            st.error("Registration failed. " + response.get("detail", ""))

# Main content
if "token" in st.session_state:
    tab1, tab2 = st.tabs(["Health Form", "Medical Chatbot"])
    
    with tab1:
        st.header("Health Form")
        with st.form("health_form"):
            alergias = st.checkbox("Do you have any allergies?")
            alergias_medicamentos = st.checkbox("Do you have any medication allergies?")
            medicamentos_actuales = st.text_input("Current medications")
            diabetes = st.checkbox("Do you have diabetes?")
            marcapasos = st.checkbox("Do you have a pacemaker?")
            epilepsia = st.checkbox("Do you have epilepsy?")
            grupo_sanguineo = st.selectbox("Blood type", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
            enfermedades_cardiacas = st.checkbox("Do you have any heart diseases?")
            enfermedades_respiratorias = st.checkbox("Do you have any respiratory diseases?")

            if st.form_submit_button("Submit"):
                form_data = {
                    "alergias": alergias,
                    "alergias_medicamentos": alergias_medicamentos,
                    "medicamentos_actuales": medicamentos_actuales,
                    "diabetes": diabetes,
                    "marcapasos": marcapasos,
                    "epilepsia": epilepsia,
                    "grupo_sanguineo": grupo_sanguineo,
                    "enfermedades_cardiacas": enfermedades_cardiacas,
                    "enfermedades_respiratorias": enfermedades_respiratorias
                }
                response = submit_health_form(form_data, st.session_state.token)
                if "message" in response:
                    st.success(response["message"])
                else:
                    st.error("Failed to submit health form. " + response.get("detail", ""))

    with tab2:
        st.header("Medical Chatbot")
        user_input = st.text_input("Ask a medical question:")
        if st.button("Send"):
            response = get_chatbot_response(user_input)
            if "response" in response:
                st.write("Chatbot: " + response["response"])
            else:
                st.error("Failed to get response from chatbot.")

else:
    st.warning("Please login or register to access the health form and medical chatbot.")