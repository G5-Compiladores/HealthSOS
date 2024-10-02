# Usa una imagen base de Python  
FROM python:3.9-slim  

# Establece el directorio de trabajo dentro del contenedor  
WORKDIR /app  

# Copia el archivo requirements.txt y el script de Streamlit al contenedor  
COPY requirements.txt ./  
COPY app.py ./  

# Instala las dependencias  
RUN pip install --no-cache-dir -r requirements.txt  

# Expone el puerto que usará Streamlit  
EXPOSE 8501  

# Comando para ejecutar la aplicación de Streamlit  
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]