import streamlit as st
import requests

# ==========================================
# CONFIGURACIÓN DE TU ANYTHINGLLM LOCAL
# ==========================================
# Reemplaza 'tutor-solar' por el slug de tu Workspace (lo ves en la URL de AnythingLLM)
WORKSPACE_SLUG = "Asistente-solar" 
API_URL = f"http://localhost:3001/api/v1/workspace/{WORKSPACE_SLUG}/chat"

# Lógica para la API KEY:
# Intenta leerla desde los 'Secrets' de GitHub/Streamlit, 
# si no existe, usa la que pegues aquí manualmente para pruebas locales.
try:
    API_KEY = st.secrets["MY_API_KEY"]
except:
    API_KEY = "K4M6XR5-ZTB4S0E-M7KX1SV-EEQYN0D"

# ==========================================
# DISEÑO DE LA PÁGINA WEB (STREAMLIT)
# ==========================================
st.set_page_config(page_title="Tutor Solar ZNI", page_icon="☀️", layout="centered")

st.title("☀️ Tutor Comunitario de Energía Solar")
st.subheader("Asistente técnico para Zonas No Interconectadas")
st.markdown("---")

# Inicializar el historial de chat en la memoria de la página
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Mostrar los mensajes anteriores guardados en la sesión
for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["rol"]):
        st.markdown(mensaje["contenido"])

# Caja de entrada de texto del usuario
pregunta = st.chat_input("Ej: ¿Cómo se limpian los paneles solares?")

if pregunta:
    # 1. Mostrar y guardar la pregunta del usuario
    with st.chat_message("user"):
        st.markdown(pregunta)
    st.session_state.mensajes.append({"rol": "user", "contenido": pregunta})

    # 2. Configuración de la llamada a la API de AnythingLLM
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    datos = {
        "message": pregunta,
        "mode": "chat" # 'chat' mantiene el contexto de la conversación
    }

    # 3. Petición al servidor local
    with st.spinner("Buscando en la base de conocimientos..."):
        try:
            respuesta = requests.post(API_URL, headers=headers, json=datos)
            respuesta_json = respuesta.json()
            respuesta_bot = respuesta_json.get("textResponse", "Lo siento, no pude procesar esa respuesta.")
        except Exception as e:
            respuesta_bot = f"⚠️ Error de conexión local: Verifica que AnythingLLM esté abierto en el puerto 3001."

    # 4. Mostrar y guardar la respuesta del asistente
    with st.chat_message("assistant"):
        st.markdown(respuesta_bot)
    st.session_state.mensajes.append({"rol": "assistant", "contenido": respuesta_bot})