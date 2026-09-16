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

# Claves de API (Asegúrate de mantenerlas seguras o usar st.secrets en producción)
DRIVE_API_KEY = "AIzaSyBjETNqerBHpqCBQBH7B1bZl55eYWrtMQk" 
GEMINI_API_KEY = "AIzaSyA8HsM0vSCopd1s05nOryhbNIGU26dvxG4"

st.set_page_config(
    page_title="BS LATAM - AUDIT ELITE SUPREMACÍA V34.0",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    genai.configure(api_key=GEMINI_API_KEY)
    fecha_actual_global = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    generation_config = {
        "temperature": 0.85,
        "top_p": 0.95,
        "top_k": 45,
        "max_output_tokens": 4096,
    }
    
    system_instruction_core = (
        f"Eres el Consultor Senior y Partner Estratégico de BS LATAM. "
        f"HOY ES: {fecha_actual_global}. "
        "Tu misión es asistir al usuario en TODO: auditoría de métricas, programación, "
        "redacción de reportes, matemáticas complejas y análisis de mercado. "
        "Eres una IA de PROPÓSITO GENERAL. "
        "Mantén siempre un tono profesional, con autoridad técnica. "
        "Estilo visual: Cyberpunk Industrial / Corporativo de Élite."
    )

    model_name_target = 'gemini-1.5-flash' 
    
    model_ia = genai.GenerativeModel(
        model_name=model_name_target,
        generation_config=generation_config,
        system_instruction=system_instruction_core
    )

except Exception as e_ia_init:
    st.error(f"FALLA CRÍTICA EN NÚCLEO NEURAL: {e_ia_init}")

# ==============================================================================
# 2. CAPA DE DISEÑO VISUAL "ELITE SUPREMACÍA" (CSS EXTENDIDO)
# ==============================================================================

st.markdown("""
    <style>
    /* Fondo Global y Tipografía */
    .main { background-color: #0b0d11; color: #e6edf3; font-family: 'Segoe UI', Tahoma, sans-serif; }
    .stApp { background-color: #0b0d11; }
    
    /* Títulos y Encabezados */
    .title-box { 
        border-left: 20px solid #E30613; 
        padding: 50px 70px; 
        margin: 40px 0 70px 0; 
        background: linear-gradient(90deg, #161b22 0%, rgba(11,13,17,0) 100%);
        border-radius: 0 40px 40px 0;
        box-shadow: 20px 0 50px rgba(0,0,0,0.7);
    }
    .m-title { font-size: 60px; font-weight: 900; color: #ffffff; text-transform: uppercase; letter-spacing: 12px; margin: 0; line-height: 1.1; text-shadow: 5px 5px 10px rgba(0,0,0,1);}
    .s-title { font-size: 26px; color: #8b949e; font-family: 'Courier New', monospace; margin-top: 25px; letter-spacing: 5px; font-weight: bold;}
    .module-header { font-size: 32px; font-weight: 700; color: #ffffff; margin-top: 40px; margin-bottom: 25px; display: flex; align-items: center; gap: 15px; border-bottom: 1px solid #30363d; padding-bottom: 15px;}
    .sub-header { font-size: 20px; font-weight: 600; color: #E30613; margin-top: 20px; text-transform: uppercase; letter-spacing: 2px;}
    
    /* Sidebar */
    .bs-latam-sidebar { color: #ffffff; font-weight: 950; font-size: 45px; text-align: center; text-transform: uppercase; letter-spacing: 7px; text-shadow: 0px 0px 30px #0055ff, 4px 4px 0px #000000; margin-bottom: 45px; padding: 25px; border-bottom: 4px solid #E30613;}
    
    /* Botones */
    .stButton>button { background: linear-gradient(135deg, #E30613 0%, #9e040d 100%) !important; color: #ffffff !important; font-weight: 900 !important; text-transform: uppercase; border-radius: 30px; height: 70px; width: 100%; font-size: 22px !important; border: none; box-shadow: 0 10px 20px rgba(227,6,19,0.35); transition: all 0.4s;}
    .stButton>button:hover { transform: scale(1.02) translateY(-4px); box-shadow: 0 15px 35px rgba(227,6,19,0.55); border: 2px solid #ffffff;}
    
    /* Inputs y Text Areas */
    .stTextArea textarea, .stTextInput input, .stNumberInput input { background-color: #161b22 !important; color: #e6edf3 !important; border: 2px solid #30363d !important; border-radius: 15px; font-size: 16px; padding: 15px;}
    .stTextArea textarea:focus, .stTextInput input:focus { border-color: #E30613 !important; box-shadow: 0 0 10px rgba(227,6,19,0.2) !important;}
    
    /* DataFrames y Elementos Visuales */
    [data-testid="stDataFrame"] { border: 2px solid #30363d; border-radius: 20px; overflow: hidden; background-color: #161b22;}
    .stCodeBlock { border: 1px solid #E30613; border-radius: 10px;}
    .error-card { background-color: #2d0000; border: 1px solid #ff4b4b; padding: 20px; border-radius: 15px; margin: 10px 0;}
    .metric-value { color: #E30613; font-size: 38px; font-weight: 900;}
    
    /* Chat IA */
    .chat-user { background-color: #161b22; border-left: 4px solid #0055ff; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    .chat-ia { background-color: #1c2128; border-left: 4px solid #E30613; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    </style>
    
    <div class="title-box">
        <p class="m-title">AUDIT-ELITE SUPREMACÍA V34.0</p>
        <p class="s-title">SISTEMA INTEGRAL BS LATAM • FB / YT / TK / VISION-IA</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. GESTIÓN DE MEMORIA Y ESTADO (SESSION STATE)
# ==============================================================================

if 'db_final' not in st.session_state: st.session_state.db_final = pd.DataFrame()
if 'db_fallidos' not in st.session_state: st.session_state.db_fallidos = pd.DataFrame()
if 'db_search' not in st.session_state: st.session_state.db_search = pd.DataFrame()
if 'chat_log' not in st.session_state: st.session_state.chat_log = []

# ==============================================================================
# 4. FUNCIONES CORE - PROCESAMIENTO Y LIMPIEZA
# ==============================================================================

def limpiar_url_táctica(url):
    """Limpia rastreadores y desenmascara acortadores (Especialmente Facebook)"""
    url = url.strip().replace('"', '').replace("'", "")
    
    # RESOLUTOR DE REDIRECCIONES PARA FACEBOOK (/share/ y fb.watch)
    # Esto es CRÍTICO para transformar facebook.com/share/r/ID a facebook.com/reel/ID
    if any(x in url.lower() for x in ['/share/', 'fb.watch']):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            r = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
            url = r.url
        except Exception:
            pass
            
    url_l = url.lower()
    
    # Normalización de subdominios FB
    if "web.facebook.com" in url_l or "m.facebook.com" in url_l:
        url = url.replace("web.facebook.com", "www.facebook.com").replace("m.facebook.com", "www.facebook.com")
    
    # Limpieza estricta de parámetros
    if "youtube.com/shorts/" in url_l or "youtu.be/" in url_l or "tiktok.com" in url_l:
        url = url.split('?')[0]
    else:
        parametros_basura = ['?si=', '&pp=', '?mibextid=', '&mibextid=', '?is_from_webapp=', '&is_from_webapp=']
        for param in parametros_basura:
            if param in url:
                url = url.split(param)[0]
                
        # Para FB general, quitamos el ? si no es watch?v=
        if 'facebook.com' in url and '/watch' not in url_l:
            url = url.split('?')[0]
            
    return url

def obtener_tipo_video(url, info_dict=None):
    if info_dict is None: info_dict = {}
    url_l = url.lower()
    
    if "facebook.com" in url_l or "fb.watch" in url_l or "fb.com" in url_l:
        if "/reel/" in url_l: return "Facebook Reel"
        return "Facebook Video"
    
    if "tiktok.com" in url_l or "tiktok" in url_l:
        if "/photo/" in url_l: return "TikTok Photo Carousel"
        return "TikTok Video"
    
    if "youtube.com" in url_l or "youtu.be" in url_l or "youtube" in url_l:
        duration = info_dict.get('duration', 0) if info_dict else 0
        if "/shorts/" in url_l or (duration and duration <= 65): return "YouTube Shorts"
        return "YouTube Video"
    
    return "Contenido Externo"

def convertir_k_m(valor_str):
    """Función de respaldo. Solo se usa si falla la extracción exacta."""
    if not valor_str: return 0
    valor_str = str(valor_str).upper().strip().replace(',', '.')
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

# ==============================================================================
# 5. MOTOR DE EXTRACCIÓN HTML DE EMERGENCIA (BÚSQUEDA DE CIFRAS EXACTAS)
# ==============================================================================

def extraccion_html_emergencia(url):
    """
    Rastrea el código fuente buscando el número EXACTO de reproducciones.
    Evita las aproximaciones ("1.5M views") buscando en los JSON internos.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept-Language': 'es-419,es;q=0.9,en;q=0.8',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    }
    try:
        res = requests.get(url, headers=headers, timeout=12)
        if res.status_code != 200:
            return None, f"HTTP Error {res.status_code}"
            
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extracción de Título
        t_tag = soup.find("meta", property="og:title")
        titulo = t_tag["content"] if t_tag else soup.title.string if soup.title else "Título Desconocido"
        
        vistas_exactas = 0
        likes_exactos = 0
        
        # BÚSQUEDA DE CIFRAS EXACTAS POR PLATAFORMA
        if "youtube" in url.lower() or "youtu.be" in url.lower():
            v_match = re.search(r'"viewCount":"(\d+)"', html)
            if v_match: vistas_exactas = int(v_match.group(1))
            
        elif "tiktok" in url.lower():
            v_match = re.search(r'"playCount":\s*(\d+)', html)
            if v_match: vistas_exactas = int(v_match.group(1))
            l_match = re.search(r'"diggCount":\s*(\d+)', html)
            if l_match: likes_exactos = int(l_match.group(1))
            
        elif "facebook" in url.lower() or "fb.watch" in url.lower():
            # Intentar buscar la métrica cruda exacta en los scripts JSON
            # Regex 1: "play_count":12345
            match_exact = re.search(r'"play_count":\s*(\d+)', html)
            if not match_exact:
                # Regex 2: "video_view_count":12345
                match_exact = re.search(r'"video_view_count":\s*(\d+)', html)
            if not match_exact:
                # Regex 3: i18n_play_count":"12,345"
                match_exact = re.search(r'"i18n_play_count":"([\d,]+)"', html)
                if match_exact:
                    vistas_exactas = int(match_exact.group(1).replace(',', ''))
            
            if match_exact and not vistas_exactas:
                vistas_exactas = int(match_exact.group(1))
                
            # Solo si TODO lo anterior falla, usamos la aproximación del texto meta
            if vistas_exactas == 0:
                t_desc = soup.find("meta", property="og:description")
                texto_meta = f"{titulo} {t_desc['content'] if t_desc else ''}"
                match_fb_aprox = re.search(r"([\d\.,]+[KMkm]?)\s*(?:views|reproducciones|vistas)", texto_meta, re.IGNORECASE)
                if match_fb_aprox: 
                    vistas_exactas = convertir_k_m(match_fb_aprox.group(1))
                    
            # Likes Facebook exactos
            match_likes = re.search(r'"reaction_count":\s*\{"count":(\d+)', html)
            if match_likes: likes_exactos = int(match_likes.group(1))
            
        tipo = obtener_tipo_video(url, {})
        plataforma = tipo.split(' ')[0].upper()
        
        return {
            "Fecha": "N/A", "Plataforma": plataforma, "Tipo": tipo,
            "Creador": "Extracción HTML", "Título": str(titulo)[:70],
            "Vistas": vistas_exactas, "Likes": likes_exactos, 
            "Comments": 0, "Saves": 0, "Link": url
        }, None
        
    except Exception as e:
        return None, str(e)

# ==============================================================================
# 6. MOTOR AUDITOR UNIVERSAL (YT-DLP PRIMARIO)
# ==============================================================================

def motor_auditor_universal_v32(urls):
    resultados = []
    fallidos = []
    
    p_bar = st.progress(0)
    status_text = st.empty()
    
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]

    for i, raw_url in enumerate(urls):
        url = limpiar_url_táctica(raw_url)
        status_text.markdown(f"🔍 **AUDITANDO (#{i+1}/{len(urls)}):** `{url[:60]}...`")
        
        ydl_opts = {
            'quiet': True,
            'ignoreerrors': True,
            'skip_download': True,
            'no_warnings': True,
            'extract_flat': False,
            'socket_timeout': 15,
            'retries': 3,
            'nocheckcertificate': True, 
            'geo_bypass': True,
            'http_headers': {
                'User-Agent': random.choice(user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8',
            }
        }
        
        exito_extraccion = False

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if info:
                    titulo_raw = str(info.get('title', 'N/A'))
                    vistas = info.get('view_count') # Extraemos crudo primero
                    
                    if vistas is not None:
                        vistas = int(vistas)
                    else:
                        vistas = 0
                        
                    likes = int(info.get('like_count') or 0)
                    tipo = obtener_tipo_video(url, info)
                    plataforma = tipo.split(' ')[0].upper()

                    # Validaciones extra para Facebook si yt-dlp saca 0 vistas
                    if plataforma == 'FACEBOOK' and vistas == 0:
                        raise ValueError("YT-DLP devolvió 0 vistas para Facebook, forzando rescate HTML.")

                    raw_date = info.get('upload_date', 'N/A')
                    if raw_date and raw_date != 'N/A' and len(raw_date) == 8:
                        fecha_formateada = f"{raw_date[6:8]}/{raw_date[4:6]}/{raw_date[2:4]}"
                    else:
                        fecha_formateada = raw_date

                    resultados.append({
                        "ID": i + 1, "Fecha": fecha_formateada, "Plataforma": plataforma,
                        "Tipo": tipo, "Creador": info.get('uploader', 'N/A'),
                        "Título": titulo_raw[:65], "Vistas": vistas, "Likes": likes,
                        "Comments": int(info.get('comment_count') or 0),
                        "Saves": int(info.get('repost_count') or 0), "Link": url
                    })
                    exito_extraccion = True
        except Exception:
            pass
        
        # SI FALLA YT-DLP O DEVUELVE 0 EN REDES COMPLEJAS, INVOCAR RESCATE HTML
        if not exito_extraccion:
            status_text.markdown(f"⚠️ **MODO EXTRACCIÓN PROFUNDA (HTML):** `{url[:50]}...`")
            data_html, error_html = extraccion_html_emergencia(url)
            
            if data_html and data_html['Vistas'] > 0:
                data_html["ID"] = i + 1
                resultados.append(data_html)
            else:
                fallidos.append({"ID": i + 1, "Link": raw_url, "Error": f"Extracción Fallida / Métrica en 0"[:60]})

        p_bar.progress((i + 1) / len(urls))
    
    p_bar.empty()
    status_text.empty()
    return pd.DataFrame(resultados), pd.DataFrame(fallidos)

# ==============================================================================
# 7. MOTOR DE BÚSQUEDA MASIVA POR CANAL (SEARCH PRO)
# ==============================================================================

def motor_busqueda_temporal(urls_canales, f_start, f_end, min_views):
    resultados = []
    d_start = int(f_start.strftime('%Y%m%d'))
    d_end = int(f_end.strftime('%Y%m%d'))
    
    p_bar = st.progress(0)
    status = st.empty()
    
    ydl_opts_search = {
        'quiet': True, 'ignoreerrors': True, 'extract_flat': True,
        'playlistend': 70, 'socket_timeout': 15, 'nocheckcertificate': True
    }
    
    for i, raw_url in enumerate(urls_canales):
        url = raw_url.strip()
        if not url: continue
        
        url_lower = url.lower()
        if "facebook.com" in url_lower and "/videos" not in url_lower and "watch" not in url_lower:
            url = url.rstrip("/") + "/videos/"
        elif "youtube.com" in url_lower and "@" in url_lower and "/videos" not in url_lower and "/shorts" not in url_lower:
            url = url.rstrip("/") + "/videos"

        status.markdown(f"🛰️ **ESCANEO RADAR:** `{url[:50]}...`")
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts_search) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if info and 'entries' in info:
                    for vid in info['entries']:
                        if not vid: continue
                        
                        v_date_str = vid.get('upload_date')
                        if not v_date_str and vid.get('timestamp'):
                            v_date_str = datetime.datetime.fromtimestamp(vid.get('timestamp')).strftime('%Y%m%d')
                        
                        v_views = vid.get('view_count')
                        
                        if v_date_str and v_views is not None:
                            v_date_int = int(v_date_str)
                            if d_start <= v_date_int <= d_end and int(v_views) >= min_views:
                                f_radar = f"{v_date_str[6:8]}/{v_date_str[4:6]}/{v_date_str[2:4]}" if len(v_date_str) == 8 else v_date_str
                                resultados.append({
                                    "Fecha": f_radar, "Canal": info.get('title', 'N/A'),
                                    "Título": vid.get('title', 'N/A')[:60], "Vistas": int(v_views),
                                    "Link": vid.get('url') or vid.get('webpage_url') or url
                                })
        except Exception:
            pass
            
        p_bar.progress((i + 1) / len(urls_canales))

    p_bar.empty()
    status.empty()
    return pd.DataFrame(resultados)

# ==============================================================================
# 8. SISTEMA DE VERIFICACIÓN DE ESTADO (DEAD OR ALIVE)
# ==============================================================================

def verificador_enlaces_masivo(urls):
    resultados = []
    p_bar = st.progress(0)
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    for i, url in enumerate(urls):
        url = url.strip()
        if not url: continue
        
        estado = "❌ Caído / Borrado"
        codigo = 404
        
        try:
            r = requests.get(url, headers=headers, timeout=8, allow_redirects=True)
            codigo = r.status_code
            if codigo == 200:
                # Comprobación extra para YouTube y TikTok (a veces devuelven 200 pero el video no existe)
                if "Video no disponible" in r.text or "This video is unavailable" in r.text or "No se pudo encontrar" in r.text:
                    estado = "⚠️ Eliminado u Oculto"
                else:
                    estado = "✅ Activo"
            elif codigo == 403:
                estado = "🔒 Privado"
        except Exception as e:
            estado = f"🚨 Error de conexión"
            codigo = "N/A"
            
        resultados.append({"Link": url, "Estado": estado, "HTTP Code": codigo})
        p_bar.progress((i + 1) / len(urls))
        
    p_bar.empty()
    return pd.DataFrame(resultados)

# ==============================================================================
# 9. IA VISION - OCR PARA IMÁGENES
# ==============================================================================

def procesar_imagen_vision(imagen_cargada, prompt_personalizado):
    try:
        img = Image.open(imagen_cargada)
        modelo_vision = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt_base = """
        Analiza esta imagen (probablemente una captura de métricas de redes sociales).
        Extrae en un formato de tabla Markdown los siguientes datos si están visibles:
        - Nombre de la cuenta / Creador
        - Vistas (Reproducciones)
        - Likes
        - Comentarios
        - Compartidos / Guardados
        Dame SÓLO los datos numéricos exactos extraídos, sin explicaciones.
        """
        
        prompt_final = prompt_personalizado if prompt_personalizado else prompt_base
        respuesta = modelo_vision.generate_content([prompt_final, img])
        return respuesta.text
    except Exception as e:
        return f"Error en procesamiento de visión: {e}"

# ==============================================================================
# 10. INTERFAZ DE USUARIO (SIDEBAR Y ENRUTAMIENTO)
# ==============================================================================

with st.sidebar:
    st.markdown('<p class="bs-latam-sidebar">BS LATAM</p>', unsafe_allow_html=True)
    modulo = st.radio(
        "MÓDULOS OPERATIVOS", 
        ["🚀 EXTRACTOR ELITE", "📂 IA VISION (CAPTURAS)", "🤖 PARTNER IA", "🛰️ SEARCH PRO", "✅ VERIFICADOR DE LINKS"], 
        index=0
    )
    
    st.divider()
    st.markdown("### ⚙️ CONTROLES DEL SISTEMA")
    if st.button("🚨 LIMPIAR CACHÉ Y REINICIAR"):
        st.session_state.clear()
        st.rerun()
        
    st.markdown("---")
    st.caption("VERSIÓN: 34.0-ELITE | BY MRSQUESO")

# ==============================================================================
# 11. MÓDULO 1: EXTRACTOR ELITE
# ==============================================================================

if modulo == "🚀 EXTRACTOR ELITE":
    st.markdown('<div class="module-header">📥 Extractor de Métricas Masivas (Precisión Absoluta)</div>', unsafe_allow_html=True)
    
    texto_entrada = st.text_area(
        "Pega los enlaces (uno por línea o separados por espacios). Soporte nativo para enlaces cortos (/share/):", 
        height=200,
        placeholder="https://www.facebook.com/share/r/1Bz89pWw64/\nhttps://www.tiktok.com/@user/video/123\nhttps://youtube.com/shorts/abc"
    )
    
    c_btn1, c_btn2 = st.columns([1, 4])
    with c_btn1:
        ejecutar = st.button("🔥 INICIAR AUDITORÍA")
    
    if ejecutar:
        raw_words = texto_entrada.replace(',', ' ').replace('\n', ' ').split()
        urls_detectadas = []
        for word in raw_words:
            word = word.strip('"\'()[]')
            wl = word.lower()
            if any(domain in wl for domain in ['tiktok', 'fb.watch', 'facebook', 'fb.com', 'youtube', 'youtu.be']):
                if not word.startswith('http'): word = 'https://' + word
                urls_detectadas.append(word)
        
        if urls_detectadas:
            res, fails = motor_auditor_universal_v32(urls_detectadas)
            st.session_state.db_final = res
            st.session_state.db_fallidos = fails
            
            if not res.empty: st.success(f"✔️ EXTRACCIÓN EXITOSA: {len(res)} registros procesados con precisión.")
            if not fails.empty: st.warning(f"⚠️ AVISO: {len(fails)} enlaces presentaron bloqueos irreversibles o métricas ocultas.")
        else:
            st.error("ERROR: No se detectaron URLs válidas en el texto ingresado.")

    if not st.session_state.db_fallidos.empty:
        with st.expander("⚠️ VER ENLACES CON ERRORES O MÉTRICAS OCULTAS"):
            st.markdown('<div class="error-card">', unsafe_allow_html=True)
            st.dataframe(st.session_state.db_fallidos, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)

    if not st.session_state.db_final.empty:
        df = st.session_state.db_final.copy()
        # Aplicar el multiplicador x3 a los videos largos de YouTube
        df['Vistas_Calc'] = df.apply(lambda row: int(row['Vistas'] * 3) if row['Tipo'] == 'YouTube Video' else int(row['Vistas']), axis=1)
        
        st.divider()
        st.markdown('<div class="sub-header">📊 DATOS EXTRAÍDOS (PRECISIÓN EXACTA)</div>', unsafe_allow_html=True)
        st.dataframe(df.drop(columns=['Vistas_Calc']), use_container_width=True, hide_index=True)

        csv_export = df.drop(columns=['Vistas_Calc']).to_csv(index=False).encode('utf-8-sig')
        st.download_button(label="💾 DESCARGAR HOJA DE CÁLCULO (CSV)", data=csv_export, file_name=f"Reporte_Exacto_BS_{datetime.datetime.now().strftime('%d%m%y_%H%M')}.csv", mime="text/csv")

        st.markdown('<div class="module-header">📋 CENTRO DE COPIADO Y FÓRMULAS</div>', unsafe_allow_html=True)
        
        df_yt_v = df[df['Tipo'] == 'YouTube Video']
        df_shorts = df[df['Tipo'] == 'YouTube Shorts']
        df_fb = df[df['Plataforma'] == 'FACEBOOK']
        df_tk = df[df['Plataforma'] == 'TIKTOK']

        m1, m2, m3, m4 = st.columns(4)
        with m1: st.markdown(f"**TOTAL VISTAS (CON BONO)**\n## {df['Vistas_Calc'].sum():,}")
        with m2: st.markdown(f"**YT LARGOS (x3 APLICADO)**\n## {df_yt_v['Vistas_Calc'].sum():,}")
        with m3: st.markdown(f"**FACEBOOK (EXACTO)**\n## {df_fb['Vistas'].sum():,}")
        with m4: st.markdown(f"**TIKTOK (EXACTO)**\n## {df_tk['Vistas'].sum():,}")

        st.divider()
        st.markdown("### 📥 Bloques de Texto para Sumatorias Rápidas")
        
        col_copy1, col_copy2 = st.columns(2)
        with col_copy1:
            st.markdown("**1. FÓRMULA YT LARGOS (Ya multiplicados x3)**")
            f_yt_largos = "+".join(df_yt_v['Vistas_Calc'].astype(str).tolist())
            st.code(f_yt_largos if f_yt_largos else "0", language="text")
            
            st.markdown("**2. FÓRMULA FACEBOOK**")
            f_fb_str = "+".join(df_fb['Vistas'].astype(str).tolist())
            st.code(f_fb_str if f_fb_str else "0", language="text")
            
            st.markdown("**3. FÓRMULA YT SHORTS**")
            f_shorts_str = "+".join(df_shorts['Vistas'].astype(str).tolist())
            st.code(f_shorts_str if f_shorts_str else "0", language="text")

        with col_copy2:
            st.markdown("**4. FÓRMULA TIKTOK**")
            f_tk_str = "+".join(df_tk['Vistas'].astype(str).tolist())
            st.code(f_tk_str if f_tk_str else "0", language="text")

            st.markdown("**5. FÓRMULA TOTAL GENERAL CONSOLIDADA**")
            f_total_todo = "+".join(df['Vistas_Calc'].astype(str).tolist())
            st.code(f_total_todo if f_total_todo else "0", language="text")
            
            st.divider()
            val_yt_long_x3 = df_yt_v['Vistas_Calc'].sum()
            val_resto = df[df['Tipo'] != 'YouTube Video']['Vistas_Calc'].sum()
            val_booster = val_yt_long_x3 + val_resto
            st.markdown(f"""
            <div style="background:#161b22; padding:15px; border-radius:10px; border:1px solid #E30613;">
                <span style="color:#8b949e;">LÓGICA MATEMÁTICA:</span> (YT Largos x3: <b>{val_yt_long_x3:,}</b>) + Redes Standard: <b>{val_resto:,}</b><br>
                <span style="color:#ffffff; font-size:24px; font-weight:bold;">RESULTADO FINAL: {val_booster:,}</span>
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# 12. MÓDULO 2: IA VISION (CAPTURAS)
# ==============================================================================

elif modulo == "📂 IA VISION (CAPTURAS)":
    st.markdown('<div class="module-header">👁️ Visión Artificial: Extractor de Capturas</div>', unsafe_allow_html=True)
    st.write("Sube capturas de pantalla de métricas. El motor Gemini Vision extraerá los números exactos de la imagen.")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        imagen = st.file_uploader("Sube la captura (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"])
        prompt_ia = st.text_area("Instrucciones específicas (Opcional):", placeholder="Ej: Extrae solo los likes y guárdalos en formato CSV...")
        
        if st.button("🔍 ANALIZAR IMAGEN") and imagen:
            with st.spinner("Procesando imagen neuronalmente..."):
                resultado_vision = procesar_imagen_vision(imagen, prompt_ia)
                st.session_state['ultimo_analisis_vision'] = resultado_vision
                
    with col2:
        if imagen:
            st.image(imagen, caption="Captura Cargada", use_column_width=True)
            
    if 'ultimo_analisis_vision' in st.session_state:
        st.divider()
        st.markdown("### 📋 RESULTADO DE EXTRACCIÓN VISUAL")
        st.info(st.session_state['ultimo_analisis_vision'])

# ==============================================================================
# 13. MÓDULO 3: PARTNER IA (CHAT)
# ==============================================================================

elif modulo == "🤖 PARTNER IA":
    st.markdown('<div class="module-header">🧠 Partner Estratégico IA</div>', unsafe_allow_html=True)
    st.write("Tu asistente para automatizaciones, correos, fórmulas avanzadas y gestión de comunidad de Blood Strike.")
    
    for mensaje in st.session_state.chat_log:
        css_class = "chat-user" if mensaje["role"] == "user" else "chat-ia"
        st.markdown(f'<div class="{css_class}"><b>{mensaje["role"].upper()}:</b><br>{mensaje["content"]}</div>', unsafe_allow_html=True)
        
    prompt_usuario = st.chat_input("Escribe tu consulta estratégica aquí...")
    
    if prompt_usuario:
        st.session_state.chat_log.append({"role": "user", "content": prompt_usuario})
        st.markdown(f'<div class="chat-user"><b>USER:</b><br>{prompt_usuario}</div>', unsafe_allow_html=True)
        
        try:
            historial_formateado = [{"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} for m in st.session_state.chat_log]
            chat = model_ia.start_chat(history=historial_formateado[:-1])
            
            with st.spinner("Sintetizando respuesta táctica..."):
                respuesta = chat.send_message(prompt_usuario)
                st.session_state.chat_log.append({"role": "assistant", "content": respuesta.text})
                st.rerun()
        except Exception as e:
            st.error(f"Falla en el enlace neural: {e}")

# ==============================================================================
# 14. MÓDULO 4: SEARCH PRO (ESCÁNER DE CANALES)
# ==============================================================================

elif modulo == "🛰️ SEARCH PRO":
    st.markdown('<div class="module-header">🛰️ Radar Temporal y Escáner de Canales</div>', unsafe_allow_html=True)
    st.write("Inserta links de perfiles/canales. El sistema rastreará los videos subidos en el rango de fechas establecido.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        fecha_inicio = st.date_input("Fecha Inicio", datetime.date.today() - datetime.timedelta(days=7))
    with col2:
        fecha_fin = st.date_input("Fecha Fin", datetime.date.today())
    with col3:
        min_views = st.number_input("Filtro: Vistas Mínimas", value=1000, step=500)
        
    canales_input = st.text_area("URLs de Canales o Perfiles (Ej: https://www.youtube.com/@CanalX):", height=150)
    
    if st.button("📡 ACTIVAR RASTREO"):
        if canales_input:
            lista_canales = canales_input.split('\n')
            resultados_search = motor_busqueda_temporal(lista_canales, fecha_inicio, fecha_fin, min_views)
            st.session_state.db_search = resultados_search
            
            if not resultados_search.empty:
                st.success(f"🎯 RASTREO COMPLETADO: {len(resultados_search)} videos encontrados en el rango.")
            else:
                st.warning("No se encontraron videos que cumplan con los criterios o los canales bloquearon el escaneo.")
        else:
            st.error("Debes ingresar al menos un canal.")
            
    if not st.session_state.db_search.empty:
        st.dataframe(st.session_state.db_search, use_container_width=True, hide_index=True)
        csv_search = st.session_state.db_search.to_csv(index=False).encode('utf-8-sig')
        st.download_button("💾 DESCARGAR REPORTE RADAR (CSV)", data=csv_search, file_name="Reporte_Radar.csv", mime="text/csv")

# ==============================================================================
# 15. MÓDULO 5: VERIFICADOR DE ENLACES
# ==============================================================================

elif modulo == "✅ VERIFICADOR DE LINKS":
    st.markdown('<div class="module-header">⚖️ Auditor de Disponibilidad de Enlaces</div>', unsafe_allow_html=True)
    st.write("Verifica de forma masiva si los enlaces están vivos (200 OK), borrados (404), o privados.")
    
    links_verificar = st.text_area("Pega los enlaces a verificar:", height=200)
    
    if st.button("🔍 VERIFICAR ESTADO"):
        if links_verificar:
            lista_verificar = [url for url in links_verificar.split() if url.startswith('http')]
            if lista_verificar:
                df_estado = verificador_enlaces_masivo(lista_verificar)
                st.dataframe(df_estado, use_container_width=True, hide_index=True)
                
                vivos = len(df_estado[df_estado['Estado'] == '✅ Activo'])
                caidos = len(df_estado) - vivos
                
                col_r1, col_r2 = st.columns(2)
                col_r1.metric("ENLACES ACTIVOS", vivos)
                col_r2.metric("ENLACES CAÍDOS/ERROR", caidos)
            else:
                st.error("No se encontraron enlaces válidos (HTTP/HTTPS).")
        else:
            st.error("El campo está vacío.")

st.markdown("---")
st.caption(f"BS LATAM Tools • {fecha_actual_global} • Blood Strike")