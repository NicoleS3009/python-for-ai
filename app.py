import os
import streamlit as st
from google import genai
from dotenv import load_dotenv

# 1. Configurar la página web
st.set_page_config(page_title="Mi Asistente de IA", page_icon="🤖")
st.title("🤖 Mi Asistente de IA Personal")
st.write("Pregúntame lo que quieras basado en el documento de datos locales.")

# 2. Cargar credenciales
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 3. Leer el archivo local
def leer_contexto_local():
    try:
        with open("datos.txt", "r", encoding="utf-8") as archivo:
            return archivo.read()
    except FileNotFoundError:
        return "No se encontró el archivo datos.txt"

contexto = leer_contexto_local()

# 4. Historial de chat en la interfaz
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Entrada del usuario
if prompt := st.chat_input("Escribe tu pregunta aquí..."):
    # Mostrar el mensaje del usuario en la pantalla
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Enviar a Gemini con el contexto oculto
    prompt_completo = f"Responde basándote únicamente en este contexto:\n\n{contexto}\n\nUser: {prompt}"
    
    with st.chat_message("assistant"):
        try:
            respuesta = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt_completo,
            )
            response_text = respuesta.text
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        except Exception as e:
            st.error(f"Error con la API: {e}")