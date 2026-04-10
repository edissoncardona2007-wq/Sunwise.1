"""
=============================================================================
 app.py — Interfaz Streamlit para chatbot offline con AnythingLLM + Ollama
 Diseñada para Zonas No Interconectadas (ZNI) de Colombia
 Funciona 100% offline — no requiere conexión a internet
=============================================================================
"""

import streamlit as st
import requests
import json
from datetime import datetime

# =============================================================================
# ⚙️  CONFIGURACIÓN — Edita estas variables según tu entorno
# =============================================================================

API_URL = "http://localhost:3001/api|brx-J1YBVGN-8Q94CN2-MPH7XK4-DJN7ENZ"
API_KEY = "F8EVNE3-6M841BJ-NXW2Y9P-EQTFQMX"

TIMEOUT = 60
NOMBRE_ASISTENTE = "Asistente Solar ZNI"
CHAT_MODE = "chat"

# =============================================================================
# 🎨  CONFIGURACIÓN DE PÁGINA
# =============================================================================

st.set_page_config(
    page_title="Claridad Solar — ZNI Colombia",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =============================================================================
# 💅  CSS EMBEBIDO
# =============================================================================

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --sol:        #F5A623;
    --sol-claro:  #FFD580;
    --sol-deep:   #C97D10;
    --tierra:     #1A1A2E;
    --tierra-mid: #16213E;
    --tierra-card:#0F3460;
    --blanco:     #F9F6F0;
    --gris-suave: #E8E4DC;
    --texto-muted:#A09E99;
    --verde-zni:  #2ECC71;
    --radio:      12px;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--tierra) !important;
    color: var(--blanco);
}

.stApp { background-color: var(--tierra) !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

.hero {
    background: linear-gradient(135deg, var(--tierra) 0%, var(--tierra-mid) 60%, #0D2137 100%);
    padding: 60px 60px 40px 60px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 360px; height: 360px;
    background: radial-gradient(circle, rgba(245,166,35,0.18) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-eyebrow {
    font-size: 0.8rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--sol);
    margin-bottom: 16px;
}
.hero-titulo {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.4rem, 5vw, 4rem);
    font-weight: 800;
    line-height: 1.05;
    color: var(--blanco);
    margin: 0 0 8px 0;
}
.hero-titulo span { color: var(--sol); }
.hero-subtitulo {
    font-size: 1.05rem;
    font-weight: 300;
    color: var(--gris-suave);
    max-width: 540px;
    line-height: 1.7;
    margin-bottom: 36px;
}
.metricas-row {
    display: flex;
    gap: 32px;
    flex-wrap: wrap;
    margin-bottom: 8px;
}
.metrica { display: flex; flex-direction: column; gap: 2px; }
.metrica-valor {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--sol);
    line-height: 1;
}
.metrica-label {
    font-size: 0.75rem;
    color: var(--texto-muted);
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.badge-offline {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(46, 204, 113, 0.12);
    border: 1px solid rgba(46, 204, 113, 0.35);
    color: var(--verde-zni);
    font-size: 0.75rem;
    font-weight: 500;
    padding: 5px 12px;
    border-radius: 100px;
    margin-bottom: 28px;
}
.badge-dot {
    width: 7px; height: 7px;
    background: var(--verde-zni);
    border-radius: 50%;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(1.3); }
}
.tarjeta-logo {
    background: linear-gradient(145deg, var(--tierra-mid), var(--tierra-card));
    border: 1px solid rgba(245,166,35,0.2);
    border-radius: var(--radio);
    padding: 28px 24px;
    text-align: center;
}
.logo-sol { font-size: 4rem; line-height: 1; margin-bottom: 12px; }
.logo-nombre {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: var(--sol);
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.logo-desc { font-size: 0.78rem; color: var(--texto-muted); margin-top: 6px; line-height: 1.5; }
.status-row { margin-top: 20px; display: flex; flex-direction: column; gap: 8px; }
.status-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.78rem;
    background: rgba(255,255,255,0.04);
    border-radius: 8px;
    padding: 7px 12px;
}
.status-label { color: var(--texto-muted); }
.status-val   { color: var(--sol-claro); font-weight: 500; }
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(245,166,35,0.3), transparent);
    margin: 0 60px;
}
.chat-titulo {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--blanco);
    margin-bottom: 4px;
}
.chat-desc { font-size: 0.85rem; color: var(--texto-muted); margin-bottom: 24px; }
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-bottom: 24px;
    max-height: 420px;
    overflow-y: auto;
    padding-right: 6px;
}
.chat-container::-webkit-scrollbar { width: 4px; }
.chat-container::-webkit-scrollbar-thumb { background: rgba(245,166,35,0.3); border-radius: 2px; }
.mensaje { display: flex; gap: 12px; align-items: flex-start; }
.mensaje-usuario { flex-direction: row-reverse; }
.avatar {
    width: 34px; height: 34px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}
.avatar-usuario { background: var(--sol); }
.avatar-asistente { background: var(--tierra-card); border: 1px solid rgba(245,166,35,0.3); }
.burbuja {
    max-width: 75%;
    padding: 12px 16px;
    border-radius: 16px;
    font-size: 0.9rem;
    line-height: 1.6;
}
.burbuja-usuario {
    background: linear-gradient(135deg, var(--sol), var(--sol-deep));
    color: var(--tierra);
    font-weight: 500;
    border-bottom-right-radius: 4px;
}
.burbuja-asistente {
    background: var(--tierra-mid);
    border: 1px solid rgba(255,255,255,0.07);
    color: var(--blanco);
    border-bottom-left-radius: 4px;
}
.msg-tiempo { font-size: 0.68rem; color: var(--texto-muted); margin-top: 4px; text-align: right; }
.msg-tiempo-usuario { text-align: left; }
.chat-bienvenida { text-align: center; padding: 40px 20px; color: var(--texto-muted); }
.bienvenida-icon { font-size: 2.5rem; margin-bottom: 12px; }
.bienvenida-texto { font-size: 0.88rem; line-height: 1.7; max-width: 380px; margin: 0 auto; }
.stTextInput > div > div > input {
    background: var(--tierra-mid) !important;
    border: 1.5px solid rgba(245,166,35,0.25) !important;
    color: var(--blanco) !important;
    border-radius: var(--radio) !important;
    font-size: 0.92rem !important;
    padding: 12px 16px !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--sol) !important;
    box-shadow: 0 0 0 3px rgba(245,166,35,0.12) !important;
}
.stTextInput > div > div > input::placeholder { color: var(--texto-muted) !important; }
.stButton > button {
    background: linear-gradient(135deg, var(--sol), var(--sol-deep)) !important;
    color: var(--tierra) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: var(--radio) !important;
    padding: 12px 28px !important;
    width: 100% !important;
}
.error-box {
    background: rgba(231, 76, 60, 0.12);
    border: 1px solid rgba(231,76,60,0.35);
    border-radius: var(--radio);
    padding: 12px 16px;
    font-size: 0.85rem;
    color: #E74C3C;
    margin-bottom: 16px;
}
.footer {
    text-align: center;
    padding: 20px 60px;
    font-size: 0.72rem;
    color: var(--texto-muted);
    border-top: 1px solid rgba(255,255,255,0.05);
    line-height: 1.8;
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# =============================================================================
# 🤖  FUNCIÓN PRINCIPAL — Consulta a AnythingLLM
# =============================================================================

def consultar_anythingllm(pregunta: str) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "message": pregunta,
        "mode": CHAT_MODE,
        "sessionId": "streamlit-session",
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=TIMEOUT)
        response.raise_for_status()
        datos = response.json()
        respuesta = datos.get("textResponse", "").strip()
        if not respuesta:
            return "⚠️ El modelo respondió pero el mensaje está vacío. Intenta reformular la pregunta."
        return respuesta
    except requests.exceptions.ConnectionError:
        return (
            "❌ **Sin conexión con AnythingLLM.**\n\n"
            "Verifica que:\n"
            "- AnythingLLM esté corriendo en `localhost:3001`\n"
            "- Ollama esté activo con el modelo cargado\n"
            "- El nombre del workspace en `API_URL` sea correcto"
        )
    except requests.exceptions.Timeout:
        return f"⏱️ **Tiempo de espera agotado.** El modelo tardó más de {TIMEOUT}s. Intenta de nuevo."
    except requests.exceptions.HTTPError as e:
        codigo = e.response.status_code if e.response else "?"
        if codigo == 401:
            return "🔑 **Error de autenticación (401).** Verifica que `API_KEY` sea correcta."
        elif codigo == 404:
            return "🔍 **Workspace no encontrado (404).** Revisa el nombre del workspace en `API_URL`."
        else:
            return f"🚨 **Error HTTP {codigo}:** {str(e)}"
    except (json.JSONDecodeError, KeyError) as e:
        return f"📋 **Error al procesar la respuesta:** {str(e)}"
    except Exception as e:
        return f"❗ **Error inesperado:** {str(e)}"


# =============================================================================
# 🗃️  ESTADO DE SESIÓN
# =============================================================================

if "historial" not in st.session_state:
    st.session_state.historial = []

def hora_actual() -> str:
    return datetime.now().strftime("%H:%M")

def agregar_mensaje(rol: str, texto: str):
    st.session_state.historial.append({"rol": rol, "texto": texto, "hora": hora_actual()})

def limpiar_historial():
    st.session_state.historial = []


# =============================================================================
# 🖼️  INTERFAZ
# =============================================================================

col_main, col_lateral = st.columns([3, 1], gap="large")

with col_main:
    st.markdown("""
    <div class="hero">
        <div class="badge-offline">
            <div class="badge-dot"></div>
            Sistema activo · 100% Offline
        </div>
        <p class="hero-eyebrow">☀️ Energía Solar · Zonas No Interconectadas · Colombia</p>
        <h1 class="hero-titulo">Claridad solar,<br><span>Impacto real</span></h1>
        <p class="hero-subtitulo">
            Plataforma de conocimiento sobre energía solar fotovoltaica para comunidades
            en Zonas No Interconectadas de Colombia. Consulta, aprende y toma decisiones
            con información confiable, disponible sin internet.
        </p>
        <div class="metricas-row">
            <div class="metrica">
                <span class="metrica-valor">1,710<span style="color:#C97D10;font-size:1.2rem">+</span></span>
                <span class="metrica-label">Localidades ZNI</span>
            </div>
            <div class="metrica">
                <span class="metrica-valor">52<span style="color:#C97D10;font-size:1.2rem">%</span></span>
                <span class="metrica-label">Sin acceso estable a energía</span>
            </div>
            <div class="metrica">
                <span class="metrica-valor">2M<span style="color:#C97D10;font-size:1.2rem">+</span></span>
                <span class="metrica-label">Personas en ZNI</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_lateral:
    st.markdown("""
    <div style="padding: 40px 20px 20px 0;">
        <div class="tarjeta-logo">
            <div class="logo-sol">☀️</div>
            <div class="logo-nombre">ZNI Solar</div>
            <div class="logo-desc">Asistente inteligente para<br>energía solar en zonas rurales</div>
            <div class="status-row">
                <div class="status-item">
                    <span class="status-label">Modelo</span>
                    <span class="status-val">Ollama / Mistral</span>
                </div>
                <div class="status-item">
                    <span class="status-label">Motor</span>
                    <span class="status-val">AnythingLLM</span>
                </div>
                <div class="status-item">
                    <span class="status-label">Modo</span>
                    <span class="status-val">100% Offline</span>
                </div>
                <div class="status-item">
                    <span class="status-label">Base de datos</span>
                    <span class="status-val">Archivos .md</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

with col_main:
    st.markdown("""
    <div style="padding: 32px 60px 0 60px;">
        <div class="chat-titulo">💬 Consulta al asistente solar</div>
        <div class="chat-desc">
            Haz preguntas sobre energía solar, instalación de paneles, mantenimiento,
            normativas ZNI o cualquier tema de la base de conocimiento.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.historial:
        st.markdown("""
        <div class="chat-bienvenida">
            <div class="bienvenida-icon">🌞</div>
            <div class="bienvenida-texto">
                Bienvenido al asistente solar para ZNI.<br>
                Escribe tu pregunta abajo para comenzar.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        burbujas_html = '<div class="chat-container">'
        for msg in st.session_state.historial:
            if msg["rol"] == "usuario":
                burbujas_html += f"""
                <div class="mensaje mensaje-usuario">
                    <div class="avatar avatar-usuario">👤</div>
                    <div>
                        <div class="burbuja burbuja-usuario">{msg["texto"]}</div>
                        <div class="msg-tiempo">{msg["hora"]}</div>
                    </div>
                </div>"""
            else:
                texto_html = msg["texto"].replace("\n", "<br>")
                burbujas_html += f"""
                <div class="mensaje">
                    <div class="avatar avatar-asistente">☀️</div>
                    <div>
                        <div class="burbuja burbuja-asistente">{texto_html}</div>
                        <div class="msg-tiempo msg-tiempo-usuario">{msg["hora"]}</div>
                    </div>
                </div>"""
        burbujas_html += '</div>'
        st.markdown(burbujas_html, unsafe_allow_html=True)

    col_input, col_btn = st.columns([4, 1])
    with col_input:
        pregunta = st.text_input(
            label="Pregunta",
            placeholder="Ej: ¿Cuántos paneles necesito para una casa en ZNI?",
            label_visibility="collapsed",
            key="input_pregunta",
        )
    with col_btn:
        enviar = st.button("Enviar ➤", use_container_width=True)

    col_limpiar, _ = st.columns([1, 3])
    with col_limpiar:
        if st.button("🗑️ Limpiar chat", use_container_width=True):
            limpiar_historial()
            st.rerun()

    if enviar and pregunta.strip():
        agregar_mensaje("usuario", pregunta.strip())
        with st.spinner("☀️ Consultando al asistente solar..."):
            respuesta = consultar_anythingllm(pregunta.strip())
        agregar_mensaje("asistente", respuesta)
        st.rerun()
    elif enviar and not pregunta.strip():
        st.markdown('<div class="error-box">⚠️ Escribe una pregunta antes de enviar.</div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    ☀️ <strong>ZNI Solar Assistant</strong> · Funcionando 100% offline con AnythingLLM + Ollama<br>
    Desarrollado para comunidades en Zonas No Interconectadas de Colombia
</div>
""", unsafe_allow_html=True)
