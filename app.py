import streamlit as st
import yt_dlp
import pandas as pd
import re
import datetime
import random
import os
import instaloader

# ==============================================================================
# 1. CONFIGURACIÓN ESTRUCTURAL BONOX
# ==============================================================================

st.set_page_config(
    page_title="BONOX - DATA AUDIT V1.0",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="expanded"
)

fecha_actual_global = datetime.datetime.now().strftime("%Y-%m-%d")

# ==============================================================================
# 2. CAPA DE DISEÑO VISUAL "BONOX EXECUTIVE" (BLANCO Y DORADO)
# ==============================================================================

st.markdown("""
    <style>
    /* Estética General Minimalista y Elegante */
    .main { 
        background-color: #0a0a0a; 
        color: #ffffff; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
    }

    .stApp { 
        background-color: #0a0a0a; 
    }
    
    /* BLOQUE DE TÍTULO PRINCIPAL */
    .title-box { 
        border-left: 15px solid #D4AF37; /* Dorado */
        padding: 40px 60px; 
        margin: 20px 0 50px 0; 
        background: linear-gradient(90deg, #1a1a1a 0%, rgba(10,10,10,0) 100%);
        border-radius: 0 30px 30px 0;
    }

    .m-title { 
        font-size: 55px; 
        font-weight: 900; 
        color: #ffffff; 
        text-transform: uppercase; 
        letter-spacing: 10px; 
        margin: 0; 
        line-height: 1.1; 
    }

    .s-title { 
        font-size: 22px; 
        color: #D4AF37; 
        font-family: 'Courier New', monospace; 
        margin-top: 15px; 
        letter-spacing: 4px; 
        font-weight: bold;
    }

    /* ESTILO DE LOS ENCABEZADOS DE MÓDULO */
    .module-header {
        font-size: 30px; 
        font-weight: 700; 
        color: #ffffff;
        margin-top: 40px; 
        margin-bottom: 25px;
        border-bottom: 2px solid #D4AF37; 
        padding-bottom: 15px;
    }

    .sub-header {
        font-size: 20px; 
        font-weight: 600; 
        color: #D4AF37;
        margin-top: 20px; 
        text-transform: uppercase; 
        letter-spacing: 2px;
    }

    /* BOTONERÍA ÉLITE DORADA */
    .stButton>button { 
        background: linear-gradient(135deg, #D4AF37 0%, #AA8C2C 100%) !important;
        color: #000000 !important; 
        font-weight: 900 !important; 
        text-transform: uppercase; 
        border-radius: 10px; 
        height: 60px; 
        width: 100%; 
        font-size: 20px !important;
        border: none; 
        box-shadow: 0 5px 15px rgba(212,175,55,0.3);
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: scale(1.02) translateY(-2px);
        box-shadow: 0 10px 25px rgba(212,175,55,0.5);
        color: #ffffff !important;
    }
    
    /* INPUTS Y TEXT AREAS MASIVAS */
    .stTextArea textarea, .stTextInput input, .stNumberInput input { 
        background-color: #1a1a1a !important; 
        color: #ffffff !important; 
        border: 1px solid #D4AF37 !important; 
        border-radius: 8px;
        font-size: 16px; 
        padding: 15px;
    }

    .stTextArea textarea:focus, .stTextInput input:focus { 
        border-color: #ffffff !important; 
    }

    /* TABLAS Y DATAFRAMES */
    [data-testid="stDataFrame"] {
        border: 1px solid #D4AF37; 
        border-radius: 10px; 
        overflow: hidden;
        background-color: #1a1a1a;
    }
    
    /* BLOQUES DE CÓDIGO (Optimización para copiado) */
    .stCodeBlock {
        border: 1px solid #D4AF37;
        border-radius: 8px;
    }

    /* CONTENEDORES DE ERROR PERSONALIZADOS */
    .error-card {
        background-color: #2d0000;
        border: 1px solid #ff4b4b;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }

    /* ESTILO RESUMEN TÁCTICO BONOX */
    .tactical-summary {
        background: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%);
        border: 1px solid #D4AF37;
        border-left: 5px solid #D4AF37;
        padding: 20px;
        border-radius: 8px;
        color: #ffffff;
        font-family: 'Courier New', monospace;
    }

    .tactical-item { 
        margin-bottom: 8px; 
        display: flex; 
        justify-content: space-between; 
    }

    .tactical-label { 
        color: #cccccc; 
        text-transform: uppercase; 
        font-size: 14px; 
    }

    .tactical-value { 
        color: #D4AF37; 
        font-weight: bold; 
        font-size: 16px;
    }
    </style>
    
    <div class="title-box">
        <p class="m-title">BONOX EXECUTIVE</p>
        <p class="s-title">SISTEMA INTEGRAL DE AUDITORÍA • FB / YT / TK / IG</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. GESTIÓN DE MEMORIA
# ==============================================================================

if 'db_final' not in st.session_state: 
    st.session_state.db_final = pd.DataFrame()

if 'db_fallidos' not in st.session_state: 
    st.session_state.db_fallidos = pd.DataFrame()

# ==============================================================================
# 4. FUNCIONES CORE - LÓGICA DE PROCESAMIENTO
# ==============================================================================

def limpiar_url_táctica(url):
    """Limpia parámetros de rastreo y corrige dominios."""
    url = url.strip().replace('"', '').replace("'", "")
    url_l = url.lower()
    
    if "web.facebook.com" in url_l:
        url = url.replace("web.facebook.com", "www.facebook.com")
    
    if '?si=' in url: url = url.split('?si=')[0]
    if '&pp=' in url: url = url.split('&pp=')[0]
    
    # Limpieza específica para Instagram
    if 'instagram.com' in url_l and '?' in url_l:
        url = url.split('?')[0]
        
    if 'facebook.com' in url or 'fb.watch' in url:
        if '?' in url and 'fb.watch' not in url:
            url = url.split('?')[0]
            
    return url

def obtener_tipo_video(url, info_dict=None):
    """Determina la categoría exacta del contenido. Permite validación temprana."""
    url_l = url.lower()
    if "facebook.com" in url_l or "fb.watch" in url_l or "fb.com" in url_l:
        return "Facebook Video"
    
    if "tiktok.com" in url_l:
        if "/photo/" in url_l: return "TikTok Photo Carousel"
        return "TikTok Video"
        
    if "instagram.com" in url_l or "instagr.am" in url_l:
        if "/reel/" in url_l or "/reels/" in url_l: return "Instagram Reel"
        return "Instagram Post"
    
    if "youtube.com" in url_l or "youtu.be" in url_l:
        duration = info_dict.get('duration', 0) if info_dict else 0
        if "/shorts/" in url_l or (duration and duration <= 65):
            return "YouTube Shorts"
        return "YouTube Video"
    
    return "Contenido Externo"

def convertir_k_m(valor_str):
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
    resultados = []
    fallidos = []
    p_bar = st.progress(0)
    status_text = st.empty()
    
    # Inicialización del motor exclusivo para Instagram
    try:
        ig_loader = instaloader.Instaloader(quiet=True)
    except Exception:
        ig_loader = None
    
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    ]

    for i, raw_url in enumerate(urls):
        url = limpiar_url_táctica(raw_url)
        status_text.markdown(f"🔍 **AUDITANDO ({i+1}/{len(urls)}):** `{url[:50]}...`")
        
        # Determinación temprana de plataforma para bifurcar motores
        tipo_preliminar = obtener_tipo_video(url)
        plataforma = tipo_preliminar.split(' ')[0].upper()
        
        # ==========================================================
        # MOTOR INSTAGRAM (Instaloader API nativa)
        # ==========================================================
        if plataforma == 'INSTAGRAM':
            try:
                if not ig_loader:
                    raise Exception("Motor Instaloader no disponible.")
                    
                match = re.search(r'/(?:p|reel|reels|tv)/([^/?#&]+)', url)
                if not match:
                    raise Exception("Formato de URL de Instagram no reconocido.")
                
                shortcode = match.group(1)
                post = instaloader.Post.from_shortcode(ig_loader.context, shortcode)
                
                vistas = post.video_view_count if post.is_video else 0
                likes = post.likes
                comments = post.comments
                titulo_raw = post.caption[:65] if post.caption else "Instagram Content"
                
                resultados.append({
                    "ID": i + 1,
                    "Plataforma": plataforma,
                    "Tipo": tipo_preliminar,
                    "Creador": post.owner_username,
                    "Título": titulo_raw,
                    "Vistas": vistas,
                    "Likes": likes,
                    "Comments": comments,
                    "Saves": 0, # Métrica privada en IG
                    "Link": url
                })
            except Exception as e_ig:
                fallidos.append({"ID": i + 1, "Link": raw_url, "Error": f"Error Instagram: {str(e_ig)[:40]}"})
                
        # ==========================================================
        # MOTOR CLÁSICO FB / YT / TK (YT-DLP)
        # ==========================================================
        else:
            ydl_opts = {
                'quiet': True,
                'ignoreerrors': True,
                'skip_download': True,
                'no_warnings': True,
                'extract_flat': False,
                'http_headers': {
                    'User-Agent': random.choice(user_agents)
                }
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    
                    if info:
                        titulo_raw = info.get('title', 'N/A')
                        vistas = int(info.get('view_count') or 0)
                        likes = int(info.get('like_count') or 0)
                        comments = int(info.get('comment_count') or 0)
                        saves = int(info.get('repost_count') or 0)
                        
                        # Recalcular tipo para determinar si YT es Short o Largo según duración
                        tipo_final = obtener_tipo_video(url, info)
                        plataforma_final = tipo_final.split(' ')[0].upper()

                        # Parche FB
                        if plataforma_final == 'FACEBOOK':
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
                            "Plataforma": plataforma_final,
                            "Tipo": tipo_final,
                            "Creador": info.get('uploader', 'N/A'),
                            "Título": titulo_raw[:65],
                            "Vistas": vistas,
                            "Likes": likes,
                            "Comments": comments,
                            "Saves": saves,
                            "Link": url
                        })
                    else:
                        fallidos.append({"ID": i + 1, "Link": raw_url, "Error": "Sin respuesta / Privado / Bloqueado"})
            
            except Exception as e_scrap:
                fallidos.append({"ID": i + 1, "Link": raw_url, "Error": str(e_scrap)[:50]})
        
        p_bar.progress((i + 1) / len(urls))
    
    p_bar.empty()
    status_text.empty()
    return pd.DataFrame(resultados), pd.DataFrame(fallidos)

def motor_busqueda_temporal(urls_canales, f_start, f_end, min_views):
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
                    for vid in info['entries']:
                        if not vid: continue
                        v_date_str = vid.get('upload_date')
                        v_views = vid.get('view_count')
                        
                        if v_date_str and v_views is not None:
                            if d_start <= int(v_date_str) <= d_end and int(v_views) >= min_views:
                                resultados.append({
                                    "Fecha": f"{v_date_str[:4]}-{v_date_str[4:6]}-{v_date_str[6:]}",
                                    "Fuente": info.get('title', 'N/A'),
                                    "Título": vid.get('title', 'N/A')[:60],
                                    "Vistas": int(v_views),
                                    "Likes": int(vid.get('like_count') or 0),
                                    "Comments": int(vid.get('comment_count') or 0),
                                    "Saves": int(vid.get('repost_count') or 0),
                                    "Link": vid.get('url') or vid.get('webpage_url') or url
                                })
        except:
            pass
            
        p_bar.progress((i + 1) / len(urls_canales))

    p_bar.empty()
    status.empty()
    return pd.DataFrame(resultados)

# ==============================================================================
# 5. SIDEBAR - CONTROL DE MISIONES BONOX
# ==============================================================================

with st.sidebar:
    # Intenta cargar el logo si existe en la carpeta
    try:
        st.image("unnamed.png", use_container_width=True)
    except:
        st.markdown('<h1 style="color:#D4AF37; text-align:center;">BONOX</h1>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    modulo = st.radio(
        "MÓDULOS DE AUDITORÍA", 
        ["🚀 EXTRACTOR DE MÉTRICAS", "🛰️ RADAR DE CANALES"],
        index=0
    )
    
    st.divider()
    
    if st.button("🔄 LIMPIAR DATOS"):
        st.session_state.clear()
        st.rerun()

# ==============================================================================
# 6. MÓDULO 1: EXTRACTOR ELITE
# ==============================================================================

if modulo == "🚀 EXTRACTOR DE MÉTRICAS":
    st.markdown('<div class="module-header">📥 Extractor de Métricas Masivas</div>', unsafe_allow_html=True)
    
    texto_entrada = st.text_area(
        "Pega los enlaces (Soporta YouTube, Facebook, TikTok e Instagram):", 
        height=200, 
        placeholder="https://www.instagram.com/reel/...\nhttps://www.tiktok.com/..."
    )
    
    if st.button("⚡ INICIAR EXTRACCIÓN"):
        raw_words = texto_entrada.replace(',', ' ').replace('\n', ' ').split()
        urls_detectadas = []
        for word in raw_words:
            word = word.strip('"\'()[]')
            wl = word.lower()
            if any(domain in wl for domain in ['tiktok.com', 'facebook.com', 'fb.', 'youtube.com', 'youtu.be', '/shorts/', 'instagram.com', 'instagr.am']):
                if not word.startswith('http'):
                    word = 'https://' + word
                urls_detectadas.append(word)
        
        if urls_detectadas:
            res, fails = motor_auditor_universal_v32(urls_detectadas)
            st.session_state.db_final = res
            st.session_state.db_fallidos = fails
            
            if not res.empty:
                st.success(f"ÉXITO: {len(res)} enlaces procesados correctamente.")
            if not fails.empty:
                st.warning(f"AVISO: {len(fails)} enlaces fallaron (Posiblemente privados o bloqueados por la plataforma).")
        else:
            st.error("ERROR: No se detectaron URLs válidas.")

    # --- VISUALIZACIÓN DE RESULTADOS ---
    if not st.session_state.db_fallidos.empty:
        with st.expander("⚠️ VER ENLACES CON ERROR"):
            st.dataframe(st.session_state.db_fallidos, use_container_width=True, hide_index=True)

    if not st.session_state.db_final.empty:
        df = st.session_state.db_final.copy()
        
        # Matemáticas Ponderadas (YT x3)
        df['Vistas_Calc'] = df.apply(
            lambda row: int(row['Vistas'] * 3) if row['Tipo'] == 'YouTube Video' else int(row['Vistas']), 
            axis=1
        )
        
        st.divider()
        st.markdown('<div class="sub-header">📊 DATOS EXTRAÍDOS</div>', unsafe_allow_html=True)
        st.dataframe(df.drop(columns=['Vistas_Calc']), use_container_width=True, hide_index=True)

        st.markdown('<div class="module-header">📋 CENTRO DE REPORTES Y FÓRMULAS</div>', unsafe_allow_html=True)
        
        df_yt_v = df[df['Tipo'] == 'YouTube Video']
        df_shorts = df[df['Tipo'] == 'YouTube Shorts']
        df_fb = df[df['Plataforma'] == 'FACEBOOK']
        df_tk = df[df['Plataforma'] == 'TIKTOK']
        df_ig = df[df['Plataforma'] == 'INSTAGRAM'] # <-- Nueva variable IG

        # Grid de métricas 
        m1, m2, m3, m4, m5 = st.columns(5)
        with m1: st.markdown(f"**YT LARGOS (x3)**\n### {df_yt_v['Vistas_Calc'].sum():,}")
        with m2: st.markdown(f"**FACEBOOK**\n### {df_fb['Vistas'].sum():,}")
        with m3: st.markdown(f"**TIKTOK**\n### {df_tk['Vistas'].sum():,}")
        with m4: st.markdown(f"**INSTAGRAM**\n### {df_ig['Vistas'].sum():,}")
        with m5: st.markdown(f"**TOTAL GLOBAL**\n### {df['Vistas_Calc'].sum():,}")

        st.divider()
        st.markdown("### 📥 Fórmulas Listas para Copiar")
        
        col_copy1, col_copy2 = st.columns(2)
        
        with col_copy1:
            st.markdown("**1. YT LARGOS (Ya multiplicado x3)**")
            st.code("+".join(df_yt_v['Vistas_Calc'].astype(str).tolist()) or "0", language="text")
            
            st.markdown("**2. FACEBOOK**")
            st.code("+".join(df_fb['Vistas'].astype(str).tolist()) or "0", language="text")
            
            st.markdown("**3. YT SHORTS**")
            st.code("+".join(df_shorts['Vistas'].astype(str).tolist()) or "0", language="text")

        with col_copy2:
            st.markdown("**4. TIKTOK**")
            st.code("+".join(df_tk['Vistas'].astype(str).tolist()) or "0", language="text")
            
            st.markdown("**5. INSTAGRAM**")
            st.code("+".join(df_ig['Vistas'].astype(str).tolist()) or "0", language="text")

            st.markdown("**6. SUMA TOTAL (GLOBAL PONDERADA)**")
            st.code("+".join(df['Vistas_Calc'].astype(str).tolist()) or "0", language="text")
            
        st.divider()
        st.markdown("**📑 RESUMEN TÁCTICO BONOX**")
        st.markdown(f"""
            <div class="tactical-summary">
                <div class="tactical-item"><span class="tactical-label">Protocolo:</span><span class="tactical-value">BONOX DATA AUDIT</span></div>
                <div class="tactical-item"><span class="tactical-label">Enlaces Exitosos:</span><span class="tactical-value">{len(df)}</span></div>
                <div class="tactical-item"><span class="tactical-label">YouTube Largos (x3):</span><span class="tactical-value">{df_yt_v['Vistas_Calc'].sum():,}</span></div>
                <div class="tactical-item"><span class="tactical-label">YouTube Shorts:</span><span class="tactical-value">{df_shorts['Vistas'].sum():,}</span></div>
                <div class="tactical-item"><span class="tactical-label">Facebook:</span><span class="tactical-value">{df_fb['Vistas'].sum():,}</span></div>
                <div class="tactical-item"><span class="tactical-label">TikTok:</span><span class="tactical-value">{df_tk['Vistas'].sum():,}</span></div>
                <div class="tactical-item"><span class="tactical-label">Instagram:</span><span class="tactical-value">{df_ig['Vistas'].sum():,}</span></div>
                <div style="border-top: 1px dashed #D4AF37; margin-top: 10px; padding-top: 10px;" class="tactical-item">
                    <span class="tactical-label" style="color:#ffffff;">IMPACTO TOTAL:</span>
                    <span class="tactical-value" style="font-size: 20px; color: #ffffff;">{df['Vistas_Calc'].sum():,}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# 7. MÓDULO 2: SEARCH PRO (RADAR TEMPORAL)
# ==============================================================================

elif modulo == "🛰️ RADAR DE CANALES":
    st.markdown('<div class="module-header">🚀 Radar de Búsqueda Masiva</div>', unsafe_allow_html=True)
    st.markdown("Busca videos dentro de fechas específicas en canales de **TikTok, YouTube o Facebook**.")
    
    area_search = st.text_area("Canales a rastrear (uno por línea):", height=150, placeholder="https://youtube.com/@CanalX\nhttps://facebook.com/PaginaY")
    
    col_s1, col_s2, col_s3 = st.columns(3)
    f_inicio = col_s1.date_input("Desde:", value=datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, 1))
    f_fin = col_s2.date_input("Hasta:", value=datetime.datetime.now().date())
    v_umbral = col_s3.number_input("Vistas Mínimas:", value=1000)

    if st.button("📡 ACTIVAR BARRIDO"):
        perfiles = [p.strip() for p in area_search.split('\n') if p.strip()]
        
        if perfiles:
            with st.status("Analizando feeds...", expanded=True) as status:
                res_search = motor_busqueda_temporal(perfiles, f_inicio, f_fin, v_umbral)
                status.update(label="✅ Escaneo Completado", state="complete", expanded=False)
            
            if not res_search.empty:
                st.markdown('<div class="sub-header">📊 RESULTADOS DEL RADAR</div>', unsafe_allow_html=True)
                st.dataframe(res_search, use_container_width=True, hide_index=True)
                
                st.markdown('<div class="tactical-summary">', unsafe_allow_html=True)
                st.markdown(f"**VISTAS TOTALES:** {res_search['Vistas'].sum():,}")
                st.markdown(f"**VIDEOS ENCONTRADOS:** {len(res_search)}")
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("**FÓRMULA COPIABLE:**")
                st.code("+".join(res_search['Vistas'].astype(str).tolist()) or "0", language="text")
            else:
                st.warning("No se encontraron videos que cumplan con los criterios.")
        else:
            st.error("Ingresa al menos un canal.")

# ==============================================================================
# FOOTER
# ==============================================================================
st.markdown("---")
st.caption(f"© {datetime.datetime.now().year} BONOX EXECUTIVE TOOLS • Módulo de Auditoría de Datos")
