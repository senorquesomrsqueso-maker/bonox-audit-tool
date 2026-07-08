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
import random
import instaloader

# ==============================================================================
# 1. CONFIGURACIÓN ESTRUCTURAL 
# ==============================================================================

# Configuración Inicial del Dashboard
st.set_page_config(
    page_title="BS LATAM - TOOL EXTENSIÓN",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

fecha_actual_global = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

    /* ESTILO RESUMEN TÁCTICO */
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
        <p class="m-title">AUDIT-ELITE V33</p>
        <p class="s-title">SISTEMA AISLADO BS LATAM • FB / YT / TK / IG-SNIPER</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. GESTIÓN DE MEMORIA Y VARIABLES DE ESTADO
# ==============================================================================

if 'db_final' not in st.session_state: 
    st.session_state.db_final = pd.DataFrame()

if 'db_fallidos' not in st.session_state: 
    st.session_state.db_fallidos = pd.DataFrame()

if 'db_ig_final' not in st.session_state: 
    st.session_state.db_ig_final = pd.DataFrame()

if 'db_ig_fallidos' not in st.session_state: 
    st.session_state.db_ig_fallidos = pd.DataFrame()

# ==============================================================================
# 4. FUNCIONES CORE - LÓGICA DE PROCESAMIENTO
# ==============================================================================

def limpiar_url_táctica(url):
    """Limpia parámetros de rastreo FB/TK."""
    url = url.strip().replace('"', '').replace("'", "")
    url_l = url.lower()
    
    if "web.facebook.com" in url_l:
        url = url.replace("web.facebook.com", "www.facebook.com")
    
    if '?si=' in url: 
        url = url.split('?si=')[0]
    if '&pp=' in url: 
        url = url.split('&pp=')[0]
        
    if 'facebook.com' in url or 'fb.watch' in url:
        if '?' in url and 'fb.watch' not in url:
            url = url.split('?')[0]
            
    return url

def limpiar_url_instagram(url):
    """Extrae el shortcode puro de un enlace de Instagram y lo formatea correctamente."""
    url = url.strip().replace('"', '').replace("'", "")
    url = url.split('?')[0]
    match = re.search(r'instagram\.com/(?:p|reel|reels|tv)/([^/?]+)', url)
    if match:
        return f"https://www.instagram.com/reel/{match.group(1)}/"
    return url

def obtener_tipo_video(url, info_dict):
    """Determina la categoría exacta del contenido."""
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

# ------------------------------------------------------------------------------
# MOTOR 1: EXTRACTOR GENERAL (FB, YT, TK) - AISLADO
# ------------------------------------------------------------------------------
def motor_auditor_universal_v32(urls):
    """Core de scraping masivo enfocado EXCLUSIVAMENTE en FB, YT y TK."""
    resultados = []
    fallidos = []
    
    p_bar = st.progress(0)
    status_text = st.empty()
    
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'
    ]

    for i, raw_url in enumerate(urls):
        url = limpiar_url_táctica(raw_url)
        status_text.markdown(f"🔍 **AUDITANDO (#{i+1}):** `{url[:50]}...`")
        
        ydl_opts = {
            'quiet': True,
            'ignoreerrors': True,
            'skip_download': True,
            'no_warnings': True,
            'http_headers': {'User-Agent': random.choice(user_agents)},
            'extract_flat': False
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if info:
                    titulo_raw = info.get('title', 'N/A')
                    vistas = int(info.get('view_count') or 0)
                    likes = int(info.get('like_count') or 0)
                    tipo = obtener_tipo_video(url, info)
                    plataforma = tipo.split(' ')[0].upper()

                    # 🛠️ PARCHE FACEBOOK
                    if plataforma == 'FACEBOOK':
                        match_fb = re.search(r"([\d\.]+[KMkm]?)\s*views.*?([\d\.]+[KMkm]?)\s*reactions\s*\|\s*(.*)", titulo_raw, re.IGNORECASE)
                        if match_fb:
                            vistas = convertir_k_m(match_fb.group(1))
                            likes = convertir_k_m(match_fb.group(2))
                            titulo_raw = match_fb.group(3).strip()
                        else:
                            match_fb_views = re.search(r"([\d\.]+[KMkm]?)\s*views\s*\|\s*(.*)", titulo_raw, re.IGNORECASE)
                            if match_fb_views:
                                vistas = convertir_k_m(match_fb_views.group(1))
                                titulo_raw = match_fb_views.group(2).strip()

                    resultados.append({
                        "ID": i + 1,
                        "Fecha": info.get('upload_date', 'N/A'),
                        "Plataforma": plataforma,
                        "Tipo": tipo,
                        "Creador": info.get('uploader', 'N/A'),
                        "Título": titulo_raw[:65],
                        "Vistas": vistas,
                        "Likes": likes,
                        "Comments": int(info.get('comment_count') or 0),
                        "Saves": int(info.get('repost_count') or 0),
                        "Link": url
                    })
                else:
                    fallidos.append({"ID": i + 1, "Link": raw_url, "Error": "Sin respuesta / Privado"})
        
        except Exception as e_scrap:
            fallidos.append({"ID": i + 1, "Link": raw_url, "Error": str(e_scrap)[:50]})
        
        p_bar.progress((i + 1) / len(urls))
    
    p_bar.empty()
    status_text.empty()
    return pd.DataFrame(resultados), pd.DataFrame(fallidos)

# ------------------------------------------------------------------------------
# MOTOR 2: IG SNIPER (EXCLUSIVO INSTAGRAM)
# ------------------------------------------------------------------------------
def motor_ig_sniper(urls):
    """
    Motor IG Sniper Definitivo: Utiliza inyección de cookies de sesión 
    para bypassear la seguridad antibot de Instagram.
    """
    resultados = []
    fallidos = []
    p_bar = st.progress(0)
    status_text = st.empty()
    
    # 1. Recuperamos tu huella digital desde los secretos
    SESSION_ID = st.secrets.get("IG_SESSION_ID", "")
    
    if not SESSION_ID:
        st.error("🚨 ERROR CRÍTICO: No se encontró 'IG_SESSION_ID' en los secrets. El Sniper fallará.")
        return pd.DataFrame(), pd.DataFrame([{"Link": "Todos", "Error": "Falta Cookie de Sesión"}])

    # 2. Inicializamos el motor de Instaloader de forma silenciosa
    L = instaloader.Instaloader(
        quiet=True,
        download_pictures=False,
        download_video_thumbnails=False,
        download_videos=False,
        download_comments=False
    )
    
    # 3. Inyectamos la cookie de sesión en el motor para simular que eres tú
    L.context._session.cookies.set("sessionid", SESSION_ID, domain=".instagram.com")
    L.context._session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    })

    for i, raw_url in enumerate(urls):
        url = limpiar_url_instagram(raw_url)
        status_text.markdown(f"📸 **INFILTRACIÓN IG ({i+1}/{len(urls)}):** `{url[:40]}...`")
        
        try:
            # Extraemos el shortcode (el ID del video/post)
            match = re.search(r'instagram\.com/(?:p|reel|reels|tv)/([^/?]+)', url)
            if not match:
                raise ValueError("No se detectó un ID válido en el enlace.")
            
            shortcode = match.group(1)
            
            # 4. Extracción táctica de la metadata
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            
            # Limpieza del título
            titulo_raw = post.caption if post.caption else "Sin Descripción"
            titulo_limpio = str(titulo_raw).replace('\n', ' ')[:65]
            
            # Verificamos si es video para sacar vistas, si es foto solo likes
            vistas = post.video_view_count if post.is_video else 0
            
            resultados.append({
                "ID": i + 1, 
                "Plataforma": "INSTAGRAM", 
                "Tipo": "Reel" if post.is_video else "Post",
                "Creador": post.owner_username, 
                "Título": titulo_limpio,
                "Vistas": vistas, 
                "Likes": post.likes,
                "Comments": post.comments, 
                "Saves": 0, 
                "Link": raw_url
            })
            
            # Pequeña pausa táctica para no alertar a los servidores de IG
            time.sleep(random.uniform(1.5, 3.5))
            
        except instaloader.exceptions.LoginRequiredException:
            fallidos.append({"ID": i + 1, "Link": raw_url, "Error": "Cookie Expirada. Renueva el SESSION_ID."})
            break # Si la cookie expira, detenemos el motor para evitar baneos
        except Exception as e:
            fallidos.append({"ID": i + 1, "Link": raw_url, "Error": f"Muro IG: {str(e)[:30]}"})

        p_bar.progress((i + 1) / len(urls))

    p_bar.empty()
    status_text.empty()
    return pd.DataFrame(resultados), pd.DataFrame(fallidos)
# ------------------------------------------------------------------------------
# MOTOR 3: SEARCH PRO (RADAR TEMPORAL)
# ------------------------------------------------------------------------------
def motor_busqueda_temporal(urls_canales, f_start, f_end, min_views):
    """MOTOR REPARADO: Añade headers de evasión y soporte explícito para FB, YT y TK."""
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
        'sleep_interval': 1,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }
    }
    
    for i, url in enumerate(urls_canales):
        url = url.strip()
        if not url: continue
        
        url_lower = url.lower()
        if "facebook.com" in url_lower and "/videos" not in url_lower and "watch" not in url_lower:
            if not url.endswith("/"): url += "/"
            url += "videos/"
        elif "youtube.com" in url_lower and "@" in url_lower and "/videos" not in url_lower and "/shorts" not in url_lower:
            if not url.endswith("/"): url += "/"
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
    
    # 🌟 ACTUALIZACIÓN: Nuevos módulos enfocados a la extracción pura
    modulo = st.radio(
        "MÓDULOS OPERATIVOS", 
        ["🚀 EXTRACTOR ELITE", "📸 IG SNIPER", "🛰️ SEARCH PRO"],
        index=0
    )
    
    st.divider()
    
    if st.button("🚨 REINICIO DE CACHÉ"):
        st.session_state.clear()
        st.rerun()
    
    st.markdown("---")
    st.caption(f"VERSIÓN: 33.0.0-SNIPER")
    st.caption(f"ÚLTIMO SYNC: {datetime.datetime.now().strftime('%H:%M:%S')}")

# ==============================================================================
# 6. MÓDULO 1: EXTRACTOR ELITE (FB, YT, TK)
# ==============================================================================

if modulo == "🚀 EXTRACTOR ELITE":
    st.markdown('<div class="module-header">📥 Extractor Masivo (FB / YT / TK)</div>', unsafe_allow_html=True)
    st.info("⚠️ Este módulo está optimizado para Facebook, YouTube y TikTok. Para Instagram, utiliza el módulo **IG SNIPER**.")
    
    texto_entrada = st.text_area(
        "Pega los enlaces (uno por línea o separados por espacios):", 
        height=200, 
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
            # Filtramos que no pase enlaces de Instagram por aquí accidentalmente
            if any(domain in wl for domain in ['tiktok.com', 'facebook.com', 'fb.watch', 'fb.com', 'youtube.com', 'youtu.be', '/shorts/', '/photo/']):
                if not word.startswith('http'):
                    word = 'https://' + word
                urls_detectadas.append(word)
        
        if urls_detectadas:
            res, fails = motor_auditor_universal_v32(urls_detectadas)
            st.session_state.db_final = res
            st.session_state.db_fallidos = fails
            
            if not res.empty: st.success(f"PROCESO FINALIZADO: {len(res)} registros extraídos con éxito.")
            if not fails.empty: st.warning(f"AVISO: {len(fails)} enlaces presentaron anomalías.")
        else:
            st.error("ERROR: No se detectaron URLs válidas de FB, YT o TK.")

    # --- VISUALIZACIÓN DE RESULTADOS GENERALES ---
    if not st.session_state.db_fallidos.empty:
        with st.expander("⚠️ VER ENLACES NO PROCESADOS / ERRORES"):
            st.markdown('<div class="error-card">', unsafe_allow_html=True)
            st.dataframe(st.session_state.db_fallidos, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)

    if not st.session_state.db_final.empty:
        df = st.session_state.db_final.copy()
        
        # NÚCLEO MATEMÁTICO
        df['Vistas_Calc'] = df.apply(lambda row: int(row['Vistas'] * 3) if row['Tipo'] == 'YouTube Video' else int(row['Vistas']), axis=1)
        
        st.divider()
        st.markdown('<div class="sub-header">📊 DATOS EXTRAÍDOS</div>', unsafe_allow_html=True)
        st.dataframe(df.drop(columns=['Vistas_Calc']), use_container_width=True, hide_index=True)

        st.markdown('<div class="module-header">📋 CENTRO DE COPIADO</div>', unsafe_allow_html=True)
        
        val_yt_long_x3 = df[df['Tipo'] == 'YouTube Video']['Vistas_Calc'].sum()
        val_resto = df[df['Tipo'] != 'YouTube Video']['Vistas_Calc'].sum()
        val_booster = val_yt_long_x3 + val_resto
        
        st.markdown(f"""
        <div style="background:#161b22; padding:15px; border-radius:10px; border:1px solid #E30613;">
            <span style="color:#8b949e;">LÓGICA:</span> (YT Largos x3: <b>{val_yt_long_x3:,}</b>) + Resto Global: <b>{val_resto:,}</b><br>
            <span style="color:#ffffff; font-size:24px; font-weight:bold;">RESULTADO FINAL: {val_booster:,}</span>
        </div>
        """, unsafe_allow_html=True)
        
        f_total_todo = "+".join(df['Vistas_Calc'].astype(str).tolist())
        st.code(f_total_todo if f_total_todo else "0", language="text")

# ==============================================================================
# 7. MÓDULO 2: IG SNIPER (NUEVO MÓDULO AISLADO)
# ==============================================================================

elif modulo == "📸 IG SNIPER":
    st.markdown('<div class="module-header">📸 IG Sniper (Extractor Dedicado)</div>', unsafe_allow_html=True)
    st.info("Este módulo está completamente aislado del motor principal. Emplea un sistema de API Residencial para bypassear la seguridad de Instagram.")
    
    texto_ig = st.text_area(
        "Pega los enlaces de Instagram (uno por línea):", 
        height=200, 
        placeholder="https://www.instagram.com/reel/XXXXXXX/\nhttps://www.instagram.com/p/YYYYYYY/"
    )
    
    if st.button("🚀 EJECUTAR IG SNIPER"):
        raw_words = texto_ig.replace(',', ' ').replace('\n', ' ').split()
        urls_ig = []
        for word in raw_words:
            word = word.strip('"\'()[]')
            if 'instagram.com' in word.lower():
                if not word.startswith('http'): word = 'https://' + word
                urls_ig.append(word)
                
        if urls_ig:
            res_ig, fails_ig = motor_ig_sniper(urls_ig)
            st.session_state.db_ig_final = res_ig
            st.session_state.db_ig_fallidos = fails_ig
            
            if not res_ig.empty: st.success(f"IG SNIPER: {len(res_ig)} registros extraídos.")
            if not fails_ig.empty: st.warning(f"IG SNIPER: {len(fails_ig)} enlaces fallaron.")
        else:
            st.error("No se detectaron URLs de Instagram válidas.")

    # --- VISUALIZACIÓN IG ---
    if not st.session_state.db_ig_fallidos.empty:
        with st.expander("⚠️ VER ERRORES DE INSTAGRAM"):
            st.dataframe(st.session_state.db_ig_fallidos, use_container_width=True, hide_index=True)

    if not st.session_state.db_ig_final.empty:
        df_ig = st.session_state.db_ig_final.copy()
        st.divider()
        st.markdown('<div class="sub-header">📊 DATA DE INSTAGRAM</div>', unsafe_allow_html=True)
        st.dataframe(df_ig, use_container_width=True, hide_index=True)

        st.markdown('<div class="module-header">📋 COPIADO INSTAGRAM</div>', unsafe_allow_html=True)
        st.markdown(f"**VISTAS TOTALES IG:** {df_ig['Vistas'].sum():,}")
        f_ig_str = "+".join(df_ig['Vistas'].astype(str).tolist())
        st.code(f_ig_str if f_ig_str else "0", language="text")

# ==============================================================================
# 8. MÓDULO 3: SEARCH PRO (SISTEMA RADAR TEMPORAL)
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
                st.warning("No se encontraron videos que cumplan con los filtros.")
        else:
            st.error("Error: Debe ingresar al menos un canal para el radar.")

# ==============================================================================
# PIE DE PÁGINA
# ==============================================================================

st.markdown("---")
st.caption(f"BS LATAM Tools Extension • {fecha_actual_global} • Blood Strike")
