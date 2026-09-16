import streamlit as st
import yt_dlp
import pandas as pd
import re
import time
import requests
import json
import datetime
import math
import os
import traceback
import urllib.parse
import random
import google.generativeai as genai
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup

# ==============================================================================
# 1. CONFIGURACIÓN ESTRUCTURAL Y NÚCLEO IA DE ALTO RENDIMIENTO
# ==============================================================================

# Credenciales de Acceso - Protocolo BS LATAM
DRIVE_API_KEY = "AIzaSyBjETNqerBHpqCBQBH7B1bZl55eYWrtMQk" 
GEMINI_API_KEY = "AIzaSyA8HsM0vSCopd1s05nOryhbNIGU26dvxG4"

# Configuración Inicial del Dashboard
st.set_page_config(
    page_title="BS LATAM - AUDIT ELITE SUPREMACÍA V32.9.1",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicialización de Inteligencia Artificial Gemini
try:
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Marcador de tiempo
    fecha_actual_global = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Configuración de generación
    generation_config = {
        "temperature": 0.85,
        "top_p": 0.95,
        "top_k": 45,
        "max_output_tokens": 4096,
    }
    
    # Instrucción Maestra del Sistema - Identidad Corporativa
    system_instruction_core = (
        f"Eres el Consultor Senior y Partner Estratégico de BS LATAM. "
        f"HOY ES: {fecha_actual_global}. "
        "Tu misión es asistir al usuario en TODO: auditoría de métricas, programación, "
        "redacción de reportes, matemáticas complejas y análisis de mercado. "
        "Eres una IA de PROPÓSITO GENERAL. "
        "Mantén siempre un tono profesional, con autoridad técnica. "
        "Estilo visual: Cyberpunk Industrial / Corporativo de Élite. "
        "NUNCA uses frases robóticas ni disculpas innecesarias."
    )

    # Configuramos el modelo sin forzar rutas largas
    model_name_target = 'gemini-1.5-flash' 
    
    # Inicializamos el modelo vinculando la instrucción que acabamos de crear
    model_ia = genai.GenerativeModel(
        model_name=model_name_target,
        generation_config=generation_config,
        system_instruction=system_instruction_core
    )
    
    st.sidebar.success("Núcleo Neuronal: ONLINE")

except Exception as e_ia_init:
    st.error(f"FALLA CRÍTICA EN NÚCLEO NEURAL: {e_ia_init}")

# ==============================================================================
# 2. CAPA DE DISEÑO VISUAL "ELITE SUPREMACÍA" (CSS EXTENDIDO)
# ==============================================================================

st.markdown("""
    <style>
    /* Estética General Dark Industrial */
    .main { 
        background-color: #0b0d11; 
        color: #e6edf3; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
    }

    .stApp { 
        background-color: #0b0d11; 
    }
    
    /* BLOQUE DE TÍTULO PRINCIPAL EXTENDIDO */
    .title-box { 
        border-left: 20px solid #E30613; 
        padding: 50px 70px; 
        margin: 40px 0 70px 0; 
        background: linear-gradient(90deg, #161b22 0%, rgba(11,13,17,0) 100%);
        border-radius: 0 40px 40px 0;
        box-shadow: 20px 0 50px rgba(0,0,0,0.7);
    }

    .m-title { 
        font-size: 60px; 
        font-weight: 900; 
        color: #ffffff; 
        text-transform: uppercase; 
        letter-spacing: 12px; 
        margin: 0; 
        line-height: 1.1; 
        text-shadow: 5px 5px 10px rgba(0,0,0,1);
    }

    .s-title { 
        font-size: 26px; 
        color: #8b949e; 
        font-family: 'Courier New', monospace; 
        margin-top: 25px; 
        letter-spacing: 5px; 
        font-weight: bold;
    }

    /* ESTILO DE LOS ENCABEZADOS DE MÓDULO */
    .module-header {
        font-size: 32px; 
        font-weight: 700; 
        color: #ffffff;
        margin-top: 40px; 
        margin-bottom: 25px;
        display: flex; 
        align-items: center; 
        gap: 15px;
        border-bottom: 1px solid #30363d; 
        padding-bottom: 15px;
    }

    .sub-header {
        font-size: 20px; 
        font-weight: 600; 
        color: #E30613;
        margin-top: 20px; 
        text-transform: uppercase; 
        letter-spacing: 2px;
    }

    /* ESTILO BS LATAM SIDEBAR */
    .bs-latam-sidebar {
        color: #ffffff; 
        font-weight: 950; 
        font-size: 45px; 
        text-align: center;
        text-transform: uppercase; 
        letter-spacing: 7px;
        text-shadow: 0px 0px 30px #0055ff, 4px 4px 0px #000000;
        margin-bottom: 45px; 
        padding: 25px; 
        border-bottom: 4px solid #E30613;
    }

    /* BOTONERÍA ÉLITE */
    .stButton>button { 
        background: linear-gradient(135deg, #E30613 0%, #9e040d 100%) !important;
        color: #ffffff !important; 
        font-weight: 900 !important; 
        text-transform: uppercase; 
        border-radius: 30px; 
        height: 70px; 
        width: 100%; 
        font-size: 22px !important;
        border: none; 
        box-shadow: 0 10px 20px rgba(227,6,19,0.35);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    .stButton>button:hover {
        transform: scale(1.02) translateY(-4px);
        box-shadow: 0 15px 35px rgba(227,6,19,0.55);
        border: 2px solid #ffffff;
    }
    
    /* INPUTS Y TEXT AREAS MASIVAS */
    .stTextArea textarea, .stTextInput input, .stNumberInput input { 
        background-color: #161b22 !important; 
        color: #e6edf3 !important; 
        border: 2px solid #30363d !important; 
        border-radius: 15px;
        font-size: 16px; 
        padding: 15px;
    }

    .stTextArea textarea:focus, .stTextInput input:focus { 
        border-color: #E30613 !important; 
    }

    /* TABLAS Y DATAFRAMES */
    [data-testid="stDataFrame"] {
        border: 2px solid #30363d; 
        border-radius: 20px; 
        overflow: hidden;
        background-color: #161b22;
    }
    
    /* BLOQUES DE CÓDIGO (Optimización para copiado) */
    .stCodeBlock {
        border: 1px solid #E30613;
        border-radius: 10px;
    }

    /* CONTENEDORES DE ERROR PERSONALIZADOS */
    .error-card {
        background-color: #2d0000;
        border: 1px solid #ff4b4b;
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
    }

    /* MÉTRICAS FLOTANTES */
    .metric-value {
        color: #E30613; 
        font-size: 38px; 
        font-weight: 900;
    }

    /* ESTILO RESUMEN TÁCTICO V32.9 */
    .tactical-summary {
        background: linear-gradient(135deg, #161b22 0%, #0b0d11 100%);
        border: 1px solid #30363d;
        border-left: 5px solid #E30613;
        padding: 20px;
        border-radius: 10px;
        color: #e6edf3;
        font-family: 'Courier New', monospace;
    }

    .tactical-item { 
        margin-bottom: 8px; 
        display: flex; 
        justify-content: space-between; 
    }

    .tactical-label { 
        color: #8b949e; 
        text-transform: uppercase; 
        font-size: 14px; 
    }

    .tactical-value { 
        color: #ffffff; 
        font-weight: bold; 
        border-bottom: 1px solid #E30613; 
    }
    </style>
    
    <div class="title-box">
        <p class="m-title">AUDIT-ELITE SUPREMACÍA V32.9.1</p>
        <p class="s-title">SISTEMA INTEGRAL BS LATAM • FB / YT / TK / VISION-IA</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. GESTIÓN DE MEMORIA, VARIABLES DE ESTADO Y LOGS
# ==============================================================================

if 'db_final' not in st.session_state: 
    st.session_state.db_final = pd.DataFrame()

if 'db_fallidos' not in st.session_state: 
    st.session_state.db_fallidos = pd.DataFrame()

if 'db_drive_vision' not in st.session_state: 
    st.session_state.db_drive_vision = pd.DataFrame()

if 'chat_log' not in st.session_state:
    st.session_state.chat_log = [
        {"role": "assistant", "content": f"SISTEMA OPERATIVO V32.9.1 LISTO. Algoritmos de Facebook actualizados."}
    ]

# ==============================================================================
# 4. FUNCIONES CORE - LÓGICA DE PROCESAMIENTO MULTI-PLATAFORMA
# ==============================================================================

def limpiar_url_táctica(url):
    """Limpia parámetros de rastreo agresivos para evitar fallos de scraping en Facebook y TikTok."""
    url = url.strip().replace('"', '').replace("'", "")
    url_l = url.lower()
    
    if "web.facebook.com" in url_l:
        url = url.replace("web.facebook.com", "www.facebook.com")
    
    # Limpieza agresiva de parámetros basura que bloquean a yt_dlp
    parametros_basura = ['?si=', '&pp=', '?mibextid=', '&mibextid=', '?is_from_webapp=', '&is_from_webapp=']
    for param in parametros_basura:
        if param in url:
            url = url.split(param)[0]
        
    if 'facebook.com' in url or 'fb.watch' in url:
        # CORRECCIÓN FB: Si tiene "?v=", no cortarlo porque es el ID del video.
        if '?' in url and 'fb.watch' not in url and 'v=' not in url.split('?')[1]:
            url = url.split('?')[0]
            
    return url

def obtener_tipo_video(url, info_dict):
    """Determina la categoría exacta del contenido, incluyendo soporte para TikTok Photos/Carousels."""
    url_l = url.lower()
    if "facebook.com" in url_l or "fb.watch" in url_l or "fb.com" in url_l:
        return "Facebook Video"
    
    if "tiktok.com" in url_l:
        if "/photo/" in url_l:
            return "TikTok Photo Carousel"
        return "TikTok Video"
    
    if "youtube.com" in url_l or "youtu.be" in url_l:
        duration = info_dict.get('duration', 0)
        if "/shorts/" in url_l or (duration and duration <= 65):
            return "YouTube Shorts"
        return "YouTube Video"
    
    return "Contenido Externo"

def navegar_ia_en_enlace(url):
    """Permite que el sistema 'entre' en un enlace y extraiga texto para la IA."""
    try:
        header_request = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        r = requests.get(url, headers=header_request, timeout=12)
        if r.status_code == 200:
            s = BeautifulSoup(r.text, 'html.parser')
            for tag in s(["script", "style", "header", "footer", "nav"]):
                tag.decompose()
            return s.get_text(separator=' ')[:5000]
        return "Error: No se pudo acceder al sitio."
    except Exception as e:
        return f"Error de conexión: {str(e)}"

def analizar_imagen_con_ia(image_file):
    """Usa Gemini Vision para leer métricas, maneja Ks/Ms y muestra reportes en pantalla."""
    try:
        if 'model_ia' not in globals():
            st.error("🚨 NÚCLEO IA OFFLINE: El modelo no cargó.")
            return 0
            
        img = Image.open(image_file)
        prompt_vision = "Analiza esta imagen. Dime ÚNICAMENTE el número total de vistas (views). Si ves una 'K' o 'M', inclúyela (ejemplo: 5.9K, 1.2M). No agregues texto adicional, solo el número."
        
        response = model_ia.generate_content([prompt_vision, img])
        texto_ia = response.text.strip().lower()
        
        st.warning(f"👁️ Lectura Cruda de la IA: '{texto_ia}'") 
        
        texto_limpio = texto_ia.replace(',', '.') 
        numeros = re.findall(r'[0-9.]+', texto_limpio)
        
        if not numeros:
            return 0
            
        valor_base = float(numeros[0])
        
        if 'k' in texto_limpio:
            return int(valor_base * 1000)
        elif 'm' in texto_limpio:
            return int(valor_base * 1000000)
        else:
            return int(valor_base)
            
    except Exception as e_vision:
        st.error(f"❌ FALLO EN LECTURA ÓPTICA (VISION): {str(e_vision)}")
        return 0

def analizar_imagen_drive_con_ia(url_drive):
    """Módulo Vision Avanzado: Descarga capturas desde Google Drive público y extrae vistas con IA."""
    try:
        file_id = re.findall(r'[-\w]{25,}', url_drive)
        if not file_id: 
            return 0, "ID de Drive no encontrado en la URL"
        
        url_download = f"https://drive.google.com/uc?export=download&id={file_id[0]}"
        response = requests.get(url_download, timeout=15)
        
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            prompt_vision = (
                "Actúa como un validador experto en auditoría visual de BS LATAM. "
                "Analiza esta captura de pantalla de métricas de redes sociales. "
                "Localiza y extrae únicamente el número total de VISTAS (Views o Reproducciones). "
                "Responde de forma estricta el número entero puro, sin letras, espacios, ni caracteres adicionales."
            )
            res = model_ia.generate_content([prompt_vision, img])
            texto_limpio = re.sub(r'[^0-9]', '', res.text)
            return int(texto_limpio) if texto_limpio else 0, "Éxito"
        else:
            return 0, f"Error de descarga: Código HTTP {response.status_code}. Asegúrate de que el enlace sea público."
    except Exception as e:
        return 0, str(e)

def convertir_k_m(valor_str):
    """Convierte strings de Facebook como '6.1K' o '1.2M' a enteros reales."""
    if not valor_str: return 0
    valor_str = str(valor_str).upper().strip()
    multiplicador = 1
    if 'K' in valor_str:
        multiplicador = 1000
        valor_str = valor_str.replace('K', '')
    elif 'M' in valor_str:
        multiplicador = 1000000
        valor_str = valor_str.replace('M', '')
    try:
        return int(float(valor_str) * multiplicador)
    except:
        return 0

def motor_auditor_universal_v32(urls):
    """Core de scraping masivo con parámetros de red optimizados para evitar cuelgues."""
    resultados = []
    fallidos = []
    
    p_bar = st.progress(0)
    status_text = st.empty()
    
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0'
    ]

    for i, raw_url in enumerate(urls):
        url = limpiar_url_táctica(raw_url)
        status_text.markdown(f"🔍 **AUDITANDO (#{i+1}):** `{url[:50]}...`")
        
        ydl_opts = {
            'quiet': True,
            'ignoreerrors': True,
            'skip_download': True,
            'no_warnings': True,
            'extract_flat': False,
            'socket_timeout': 15,    
            'retries': 3,            
            'nocheckcertificate': True, 
            'http_headers': {
                'User-Agent': random.choice(user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7',
            }
        }

        # Inyección dinámica de cookies si el archivo existe (Parche Anti-Bot de TikTok)
        if os.path.exists('cookies.txt'):
            ydl_opts['cookiefile'] = 'cookies.txt'
            ydl_opts['sleep_interval_requests'] = 2
            ydl_opts['max_sleep_interval'] = 4
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if info:
                    titulo_raw = info.get('title', 'N/A')
                    vistas = int(info.get('view_count') or 0)
                    likes = int(info.get('like_count') or 0)
                    comments_val = int(info.get('comment_count') or 0)
                    saves_val = int(info.get('repost_count') or 0)
                    
                    tipo = obtener_tipo_video(url, info)
                    plataforma = tipo.split(' ')[0].upper()

                    # =========================================================
                    # 🛠️ PARCHE FACEBOOK V32.9.1: EXTRACCIÓN AVANZADA METADATA
                    # =========================================================
                    if plataforma == 'FACEBOOK':
                        # yt-dlp devuelve a veces: "1.2K views, 34 likes, 10 comments, 2 shares, Facebook Reels | Título"
                        if '|' in titulo_raw:
                            partes = titulo_raw.split('|', 1)
                            metadata_str = partes[0]
                            titulo_raw = partes[1].strip()
                        else:
                            metadata_str = titulo_raw
                            # Limpieza agresiva por si no hay delimitador '|'
                            titulo_raw = re.sub(r"([\d\.]+[KMkm]?)\s*(views|likes|reactions|comments|shares)[,\s]*", "", titulo_raw, flags=re.IGNORECASE).strip()
                            titulo_raw = re.sub(r"Facebook (Reels|video|Post)", "", titulo_raw, flags=re.IGNORECASE).strip()

                        # Extraemos cada métrica independientemente
                        m_vistas = re.search(r"([\d\.]+[KMkm]?)\s*views", metadata_str, re.IGNORECASE)
                        if m_vistas: vistas = convertir_k_m(m_vistas.group(1))

                        m_likes = re.search(r"([\d\.]+[KMkm]?)\s*(likes|reactions)", metadata_str, re.IGNORECASE)
                        if m_likes: likes = convertir_k_m(m_likes.group(1))

                        m_comments = re.search(r"([\d\.]+[KMkm]?)\s*comments", metadata_str, re.IGNORECASE)
                        if m_comments: comments_val = convertir_k_m(m_comments.group(1))

                        m_shares = re.search(r"([\d\.]+[KMkm]?)\s*shares", metadata_str, re.IGNORECASE)
                        if m_shares: saves_val = convertir_k_m(m_shares.group(1))
                    # =========================================================

                    resultados.append({
                        "ID": i + 1,
                        "Fecha": info.get('upload_date', 'N/A'),
                        "Plataforma": plataforma,
                        "Tipo": tipo,
                        "Creador": info.get('uploader', 'N/A'),
                        "Título": titulo_raw[:65],
                        "Vistas": vistas,
                        "Likes": likes,
                        "Comments": comments_val,
                        "Saves": saves_val,
                        "Link": url
                    })
                else:
                    fallidos.append({"ID": i + 1, "Link": raw_url, "Error": "Sin respuesta / Privado / Bloqueo anti-bot"})
        
        except Exception as e_scrap:
            fallidos.append({"ID": i + 1, "Link": raw_url, "Error": str(e_scrap)[:50]})
        
        p_bar.progress((i + 1) / len(urls))
    
    p_bar.empty()
    status_text.empty()
    return pd.DataFrame(resultados), pd.DataFrame(fallidos)

def motor_busqueda_temporal(urls_canales, f_start, f_end, min_views):
    """
    MOTOR REPARADO: Se eliminan pausas innecesarias y se blindan las cabeceras para máxima velocidad.
    """
    resultados = []
    d_start = int(f_start.strftime('%Y%m%d'))
    d_end = int(f_end.strftime('%Y%m%d'))
    
    p_bar = st.progress(0)
    status = st.empty()
    
    ydl_opts_search = {
        'quiet': True,
        'ignoreerrors': True,
        'extract_flat': True,
        'playlistend': 50,
        'socket_timeout': 15,
        'retries': 3,
        'nocheckcertificate': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
        }
    }
    
    for i, url in enumerate(urls_canales):
        url = url.strip()
        if not url: continue
        
        url_lower = url.lower()
        if "facebook.com" in url_lower and "/videos" not in url_lower and "watch" not in url_lower:
            if not url.endswith("/"):
                url += "/"
            url += "videos/"
        elif "youtube.com" in url_lower and "@" in url_lower and "/videos" not in url_lower and "/shorts" not in url_lower:
            if not url.endswith("/"):
                url += "/"
            url += "videos"

        status.markdown(f"🛰️ **ESCANEO RADAR:** Analizando feed de `{url[:40]}...`")
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts_search) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if info and 'entries' in info:
                    videos = info['entries']
                    for vid in videos:
                        if not vid: continue
                        
                        v_date_str = vid.get('upload_date')
                        if not v_date_str and vid.get('timestamp'):
                            v_date_str = datetime.datetime.fromtimestamp(vid.get('timestamp')).strftime('%Y%m%d')
                        
                        v_views = vid.get('view_count')
                        
                        if v_date_str and v_views is not None:
                            v_date_int = int(v_date_str)
                            
                            if d_start <= v_date_int <= d_end:
                                if int(v_views) >= min_views:
                                    resultados.append({
                                        "Fecha": f"{v_date_str[:4]}-{v_date_str[4:6]}-{v_date_str[6:]}",
                                        "Canal/Fuente": info.get('title', 'N/A'),
                                        "Título Video": vid.get('title', 'N/A')[:60],
                                        "Vistas": int(v_views),
                                        "Likes": int(vid.get('like_count') or 0),
                                        "Comments": int(vid.get('comment_count') or 0),
                                        "Saves": int(vid.get('repost_count') or 0),
                                        "Link": vid.get('url') or vid.get('webpage_url') or url
                                    })
                else:
                    print(f"No se pudieron extraer entradas de: {url}")
        except Exception as e:
            print(f"Error en canal {url}: {e}")
            
        p_bar.progress((i + 1) / len(urls_canales))

    p_bar.empty()
    status.empty()
    return pd.DataFrame(resultados)

# ==============================================================================
# 5. SIDEBAR - CONTROL DE MISIONES
# ==============================================================================

with st.sidebar:
    st.markdown('<p class="bs-latam-sidebar">BS LATAM</p>', unsafe_allow_html=True)
    
    modulo = st.radio(
        "MÓDULOS OPERATIVOS", 
        ["🚀 EXTRACTOR ELITE", "📂 DRIVE AUDITOR (VISION)", "🤖 PARTNER IA", "🛰️ SEARCH PRO"],
        index=0
    )
    
    st.divider()
    
    if st.button("🚨 REINICIO DE CACHÉ"):
        st.session_state.clear()
        st.rerun()
    
    st.markdown("---")
    st.caption(f"VERSIÓN: 32.9.1-ELITE")
    st.caption(f"ÚLTIMO SYNC: {datetime.datetime.now().strftime('%H:%M:%S')}")

# ==============================================================================
# 6. MÓDULO 1: EXTRACTOR ELITE (MODO MULTI-PLATAFORMA)
# ==============================================================================

if modulo == "🚀 EXTRACTOR ELITE":
    st.markdown('<div class="module-header">📥 Extractor de Métricas Masivas</div>', unsafe_allow_html=True)
    
    texto_entrada = st.text_area(
        "Pega los enlaces (uno por línea o separados por espacios):", 
        height=250, 
        placeholder="www.tiktok.com/... \nhttps://web.facebook.com/reel/..."
    )
    
    c_btn1, c_btn2 = st.columns([1, 4])
    with c_btn1:
        ejecutar = st.button("🔥 EJECUTAR AUDITORÍA")
    
    if ejecutar:
        raw_words = texto_entrada.replace(',', ' ').replace('\n', ' ').split()
        urls_detectadas = []
        for word in raw_words:
            word = word.strip('"\'()[]')
            wl = word.lower()
            if any(domain in wl for domain in ['tiktok.com', 'facebook.com', 'fb.watch', 'fb.com', 'youtube.com', 'youtu.be', '/shorts/', '/photo/']):
                if not word.startswith('http'):
                    word = 'https://' + word
                urls_detectadas.append(word)
        
        if urls_detectadas:
            res, fails = motor_auditor_universal_v32(urls_detectadas)
            st.session_state.db_final = res
            st.session_state.db_fallidos = fails
            
            if not res.empty:
                st.success(f"PROCESO FINALIZADO: {len(res)} registros extraídos con éxito.")
            if not fails.empty:
                st.warning(f"AVISO: {len(fails)} enlaces presentaron anomalías.")
        else:
            st.error("ERROR: No se detectaron URLs válidas en el campo de texto. Asegúrate de pegar links de FB, TK o YT.")

    # --- ZONA DE VISUALIZACIÓN DE RESULTADOS ---
    
    if not st.session_state.db_fallidos.empty:
        with st.expander("⚠️ VER ENLACES NO PROCESADOS / ERRORES"):
            st.markdown('<div class="error-card">', unsafe_allow_html=True)
            st.dataframe(st.session_state.db_fallidos, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)

    if not st.session_state.db_final.empty:
        df = st.session_state.db_final.copy()
        
        # --- NÚCLEO MATEMÁTICO: APLICACIÓN DEL FACTOR X3 A YT LARGOS ---
        df['Vistas_Calc'] = df.apply(
            lambda row: int(row['Vistas'] * 3) if row['Tipo'] == 'YouTube Video' else int(row['Vistas']), 
            axis=1
        )
        
        st.divider()
        st.markdown('<div class="sub-header">📊 DATOS EXTRAÍDOS (MULTI-PLATAFORMA)</div>', unsafe_allow_html=True)
        st.dataframe(df.drop(columns=['Vistas_Calc']), use_container_width=True, hide_index=True)

        st.markdown('<div class="module-header">📋 CENTRO DE COPIADO Y FÓRMULAS</div>', unsafe_allow_html=True)
        
        df_yt_v = df[df['Tipo'] == 'YouTube Video']
        df_shorts = df[df['Tipo'] == 'YouTube Shorts']
        df_fb = df[df['Plataforma'] == 'FACEBOOK']
        df_tk = df[df['Plataforma'] == 'TIKTOK']

        # Grid de métricas rápidas
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"**TOTAL VISTAS (PONDERADO)**\n## {df['Vistas_Calc'].sum():,}")
        with m2:
            st.markdown(f"**YT LARGOS (x3 APLICADO)**\n## {df_yt_v['Vistas_Calc'].sum():,}")
        with m3:
            st.markdown(f"**FACEBOOK**\n## {df_fb['Vistas'].sum():,}")
        with m4:
            st.markdown(f"**TIKTOK**\n## {df_tk['Vistas'].sum():,}")

        # BLOQUES DE CÓDIGO PARA COPIADO DIRECTO
        st.divider()
        st.markdown("### 📥 Bloques de Texto para Copiar")
        
        col_copy1, col_copy2 = st.columns(2)
        
        with col_copy1:
            st.markdown("**1. FÓRMULA YT LARGOS (X+Y+Z) [YA MULTIPLICADO X3]**")
            f_yt_largos = "+".join(df_yt_v['Vistas_Calc'].astype(str).tolist())
            st.code(f_yt_largos if f_yt_largos else "0", language="text")
            
            st.markdown("**2. FÓRMULA FACEBOOK (X+Y+Z)**")
            f_fb_str = "+".join(df_fb['Vistas'].astype(str).tolist())
            st.code(f_fb_str if f_fb_str else "0", language="text")
            
            st.markdown("**3. FÓRMULA YT SHORTS (X+Y+Z)**")
            f_shorts_str = "+".join(df_shorts['Vistas'].astype(str).tolist())
            st.code(f_shorts_str if f_shorts_str else "0", language="text")

            st.markdown("**4. VISTAS TOTALES DE TODO (SUMA GLOBAL PONDERADA)**")
            f_total_todo = "+".join(df['Vistas_Calc'].astype(str).tolist())
            st.code(f_total_todo if f_total_todo else "0", language="text")

        with col_copy2:
            st.markdown("**5. FÓRMULA TIKTOK (X+Y+Z)**")
            f_tk_str = "+".join(df_tk['Vistas'].astype(str).tolist())
            st.code(f_tk_str if f_tk_str else "0", language="text")

            st.markdown("**6. FÓRMULA TOTAL GENERAL**")
            st.code(f_total_todo if f_total_todo else "0", language="text")
            
            # --- CÁLCULO ESTELAR CORREGIDO ---
            st.divider()
            st.markdown("### 🚀 CÁLCULO ESTELAR (YT + RESTO)")
            
            val_yt_long_x3 = df_yt_v['Vistas_Calc'].sum()
            val_resto = df[df['Tipo'] != 'YouTube Video']['Vistas_Calc'].sum()
            val_booster = val_yt_long_x3 + val_resto
            
            st.markdown(f"""
            <div style="background:#161b22; padding:15px; border-radius:10px; border:1px solid #E30613;">
                <span style="color:#8b949e;">LÓGICA:</span> (YT Largos x3: <b>{val_yt_long_x3:,}</b>) + Resto Global: <b>{val_resto:,}</b>
                <br>
                <span style="color:#ffffff; font-size:24px; font-weight:bold;">RESULTADO FINAL: {val_booster:,}</span>
            </div>
            """, unsafe_allow_html=True)
            st.code(f"{val_booster}", language="text")

            # --- RESUMEN TÁCTICO CORREGIDO ---
            st.markdown("**7. RESUMEN TÁCTICO DE OPERACIÓN**")
            st.markdown(f"""
                <div class="tactical-summary">
                    <div class="tactical-item"><span class="tactical-label">Protocolo:</span><span class="tactical-value">BS LATAM AUDIT ELITE</span></div>
                    <div class="tactical-item"><span class="tactical-label">Exitosos:</span><span class="tactical-value">{len(df)}</span></div>
                    <div class="tactical-item"><span class="tactical-label">YouTube Largos (x3):</span><span class="tactical-value">{val_yt_long_x3:,}</span></div>
                    <div class="tactical-item"><span class="tactical-label">YouTube Shorts (x1):</span><span class="tactical-value">{df_shorts['Vistas'].sum():,}</span></div>
                    <div class="tactical-item"><span class="tactical-label">Facebook:</span><span class="tactical-value">{df_fb['Vistas'].sum():,}</span></div>
                    <div class="tactical-item"><span class="tactical-label">TikTok:</span><span class="tactical-value">{df_tk['Vistas'].sum():,}</span></div>
                    <div style="border-top: 1px dashed #E30613; margin-top: 10px; padding-top: 10px;" class="tactical-item">
                        <span class="tactical-label" style="color:#E30613;">Acumulado Ponderado:</span>
                        <span class="tactical-value" style="font-size: 18px;">{df['Vistas_Calc'].sum():,}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# 7. MÓDULO 2: DRIVE AUDITOR (VISION IA + NAVEGACIÓN INTEGRADAS)
# ==============================================================================

elif modulo == "📂 DRIVE AUDITOR (VISION)":
    st.markdown('<div class="module-header">👁️ Auditor Visual y de Enlaces</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sub-header">🔗 Auditoría Automatizada de Capturas por Enlace de Google Drive</div>', unsafe_allow_html=True)
    entrada_enlaces_drive = st.text_area(
        "Pega aquí los enlaces de Google Drive (La IA descargará el contenido y procesará la métrica mediante visión artificial):", 
        height=150, 
        placeholder="Pega múltiples enlaces de Drive públicos aquí (uno por línea)..."
    )
    
    st.divider()
    
    st.markdown('<div class="sub-header">📸 Auditoría por Evidencia Visual Local (OCR)</div>', unsafe_allow_html=True)
    up_files = st.file_uploader("Arrastra las evidencias locales aquí:", type=['png', 'jpg', 'jpeg', 'webp'], accept_multiple_files=True)
    
    if st.button("🧠 INICIAR AUDITORÍA PROFUNDA"):
        v_results_final = []
        
        urls_drive = re.findall(r"(https?://[^\s\"\'\)\],]+)", entrada_enlaces_drive)
        if urls_drive:
            for u in urls_drive:
                if "drive.google.com" in u.lower():
                    with st.spinner(f"IA Descargando y escaneando captura de Drive..."):
                        vistas_drive, status_drive = analizar_imagen_drive_con_ia(u)
                        v_results_final.append({
                            "Fecha": "Drive Vision IA", 
                            "Plataforma": "DRIVE", 
                            "Tipo": "Captura Automática", 
                            "Creador": "N/A", 
                            "Título": f"Asset Drive Visual", 
                            "Vistas": vistas_drive, 
                            "Link": u
                        })
                else:
                    with st.spinner(f"IA Navegando en {u[:30]}..."):
                        texto_web = navegar_ia_en_enlace(u)
                        prompt_ia_link = f"Analiza este texto extraído de una web y busca el número de VISTAS o REPRODUCCIONES. Solo responde el número: {texto_web}"
                        res_ia_link = model_ia.generate_content(prompt_ia_link)
                        vistas_final = re.sub(r'[^0-9]', '', res_ia_link.text)
                        
                        v_results_final.append({
                            "Fecha": "Enlace IA", "Plataforma": "LINK", "Tipo": "Scraping IA", 
                            "Creador": "N/A", "Título": u[:50], 
                            "Vistas": int(vistas_final) if vistas_final else 0, "Link": u
                        })

        if up_files:
            v_bar = st.progress(0)
            for idx, f in enumerate(up_files):
                v_img = analizar_imagen_con_ia(f)
                v_results_final.append({
                    "Fecha": "OCR IA", "Plataforma": "VISION", "Tipo": "Captura Local", 
                    "Creador": "N/A", "Título": f.name, "Vistas": v_img, "Link": "Archivo Local"
                })
                v_bar.progress((idx + 1) / len(up_files))
        
        st.session_state.db_drive_vision = pd.DataFrame(v_results_final)
        st.success("Análisis Profundo Completado.")

    if not st.session_state.db_drive_vision.empty:
        st.markdown('<div class="sub-header">📊 DATA CONSOLIDADA DRIVE/VISION</div>', unsafe_allow_html=True)
        st.dataframe(st.session_state.db_drive_vision, use_container_width=True, hide_index=True)
        f_ia = "+".join(st.session_state.db_drive_vision['Vistas'].astype(str).tolist())
        st.markdown("**FÓRMULA DE SUMA DRIVE/VISION**")
        st.code(f_ia, language="text")

# ==============================================================================
# 8. MÓDULO 3: PARTNER IA (CON VALIDACIÓN DE CONEXIÓN)
# ==============================================================================

elif modulo == "🤖 PARTNER IA":
    st.markdown('<div class="module-header">🤖 Partner IA - Consultor Estratégico</div>', unsafe_allow_html=True)
    
    for msg in st.session_state.chat_log:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if p_user := st.chat_input("Instrucción técnica..."):
        st.session_state.chat_log.append({"role": "user", "content": p_user})
        with st.chat_message("user"): 
            st.markdown(p_user)
        
        with st.chat_message("assistant"):
            try:
                if not GEMINI_API_KEY or GEMINI_API_KEY == "TU_LLAVE_AQUI":
                    st.error("ERROR: API KEY no configurada. Verifica tus Secretos.")
                else:
                    ventana = st.session_state.chat_log[-6:] 
                    gemini_history = []
                    for msg in ventana[:-1]: 
                        if "SISTEMA OPERATIVO" in msg["content"]: continue
                        rol = "user" if msg["role"] == "user" else "model"
                        gemini_history.append({"role": rol, "parts": [msg["content"]]})
                    
                    chat = model_ia.start_chat(history=gemini_history)
                    response = chat.send_message(p_user)
                    
                    if response and response.text:
                        texto_ia = response.text
                        st.markdown(texto_ia)
                        st.session_state.chat_log.append({"role": "assistant", "content": texto_ia})
                    else:
                        st.warning("La IA respondió vacío. Reintenta.")
            
            except Exception as e_chat:
                st.error(f"FALLO DE CONEXIÓN CON GEMINI: {str(e_chat)}")
                st.info("💡 Tip: Verifica que tu API Key sea válida en los 'Secrets' de Streamlit.")

# ==============================================================================
# 9. MÓDULO 4: SEARCH PRO (SISTEMA RADAR TEMPORAL)
# ==============================================================================

elif modulo == "🛰️ SEARCH PRO":
    st.markdown('<div class="module-header">🚀 Radar de Canales (Motor Temporal)</div>', unsafe_allow_html=True)
    st.markdown("Pega los enlaces de canales o perfiles de **TikTok, YouTube o Facebook**. El sistema buscará videos dentro de las fechas indicadas.")
    
    area_search = st.text_area("Canales a rastrear (uno por línea):", height=150, placeholder="https://youtube.com/@CanalX\nhttps://facebook.com/PaginaY\nhttps://tiktok.com/@UserZ")
    
    col_s1, col_s2, col_s3 = st.columns(3)
    f_inicio = col_s1.date_input("Desde:", value=datetime.date(2026, 2, 1))
    f_fin = col_s2.date_input("Hasta:", value=datetime.date(2026, 2, 28))
    v_umbral = col_s3.number_input("Vistas Mínimas (Filtro):", value=1000)

    if st.button("🚀 ACTIVAR BARRIDO TEMPORAL"):
        perfiles = [p.strip() for p in area_search.split('\n') if p.strip()]
        
        if perfiles:
            with st.status("📡 Escaneando feeds de contenido...", expanded=True) as status:
                st.write(f"Iniciando extracción profunda en {len(perfiles)} canales...")
                st.write("Aplicando protocolos multiplataforma (FB / YT / TK)...")
                
                res_search = motor_busqueda_temporal(perfiles, f_inicio, f_fin, v_umbral)
                
                status.update(label="✅ Escaneo Completado", state="complete", expanded=False)
            
            if not res_search.empty:
                st.markdown('<div class="sub-header">📊 VIDEOS DETECTADOS (FILTRADOS)</div>', unsafe_allow_html=True)
                st.dataframe(res_search, use_container_width=True, hide_index=True)
                
                st.markdown('<div class="tactical-summary">', unsafe_allow_html=True)
                total_radar = res_search['Vistas'].sum()
                st.markdown(f"**VISTAS TOTALES ENCONTRADAS:** {total_radar:,}")
                st.markdown(f"**TOTAL VIDEOS:** {len(res_search)}")
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("**FÓRMULA TOTAL COPIABLE:**")
                f_search_total = "+".join(res_search['Vistas'].astype(str).tolist())
                st.code(f_search_total if f_search_total else "0", language="text")
            else:
                st.warning("No se encontraron videos que cumplan con los filtros. Si el perfil tiene videos, prueba bajando el umbral de vistas a 0 o revisa que el link sea público.")
        else:
            st.error("Error: Debe ingresar al menos un canal para el radar.")

# ==============================================================================
# PIE DE PÁGINA Y METADATOS
# ==============================================================================

st.markdown("---")
st.caption(f"BS LATAM Tools • {fecha_actual_global} • Blood Strike")
