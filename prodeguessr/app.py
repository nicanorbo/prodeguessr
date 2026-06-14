import streamlit as st
import time
from api_client import obtener_partidos
from ml_engine import predecir_marcador

st.set_page_config(page_title="ProdeGuessr 2026", page_icon="🏆", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&display=swap');
    body { background-color: #050505; color: #ffffff; font-family: 'Montserrat', sans-serif; }
    .main-header { text-align: center; font-size: 3.5rem; font-weight: 900; margin-bottom: 0.2rem; background: linear-gradient(90deg, #00B0B9 0%, #D2125E 50%, #FFD700 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .sub-header { text-align: center; color: #aaaaaa; font-size: 1rem; margin-bottom: 2rem; text-transform: uppercase; letter-spacing: 2px; }
    .match-selector { background-color: #1a1a1a; padding: 15px; border-radius: 10px; border: 1px solid #333; margin-bottom: 20px; }
    .prediction-card { background: linear-gradient(145deg, #1a1a1a, #0d0d0d); border: 1px solid #00B0B9; border-radius: 20px; padding: 30px; margin-top: 20px; box-shadow: 0 0 20px rgba(0, 176, 185, 0.15); }
    .score-box { font-size: 4rem; font-weight: 900; color: #FFD700; text-align: center; text-shadow: 0 0 10px rgba(255, 215, 0, 0.3); margin: 20px 0; }
    .team-display { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
    .team-name { font-size: 1.8rem; font-weight: 700; }
    .flag { font-size: 3rem; }
    .analysis-text { background-color: rgba(0, 176, 185, 0.1); border-left: 4px solid #D2125E; padding: 15px; border-radius: 0 10px 10px 0; margin-top: 20px; font-size: 1rem; line-height: 1.6; color: #e0e0e0; }
    .stats-row { display: flex; justify-content: space-around; margin-top: 15px; font-size: 0.9rem; color: #888; }
    .stButton>button { background: linear-gradient(90deg, #D2125E 0%, #00B0B9 100%); color: white; font-weight: 800; font-size: 1.2rem; border: none; border-radius: 50px; padding: 15px 30px; width: 100%; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">PRODEGUESSR</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Predicción Exacta con IA • Mundial 2026</div>', unsafe_allow_html=True)

partidos = obtener_partidos()

if not partidos:
    st.error("No se pudieron cargar partidos. Verifica tu conexión o la API.")
else:
    opciones = [f"{p['local']} vs {p['visitante']}" for p in partidos]
    st.markdown('<div class="match-selector">', unsafe_allow_html=True)
    seleccion_str = st.selectbox("🔥 Elige el partido del día:", opciones, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    local_name, visitante_name = seleccion_str.split(" vs ")

    if st.button("🔮 PREDECIR MARCADOR EXACTO"):
        with st.spinner("🧠 Analizando tácticas, forma física y historial..."):
            time.sleep(2)
            resultado = predecir_marcador(local_name, visitante_name)
            
            flag_local = get_flag(local_name)
            flag_visitante = get_flag(visitante_name)

            st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                st.markdown(f"<div style='text-align:center'><div class='flag'>{flag_local}</div><div class='team-name'>{local_name}</div></div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div class='score-box'>{resultado['goles_local']} - {resultado['goles_visitante']}</div>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"<div style='text-align:center'><div class='flag'>{flag_visitante}</div><div class='team-name'>{visitante_name}</div></div>", unsafe_allow_html=True)

            st.markdown(f"<div class='analysis-text'><strong>🧠 ANÁLISIS TÁCTICO:</strong><br>{resultado['razon']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stats-row'><span>📊 xG {local_name}: <strong>{resultado['xg_local']}</strong></span><span>🎯 Confianza: <strong style='color:#00B0B9'>{resultado['confianza']}</strong></span><span>📊 xG {visitante_name}: <strong>{resultado['xg_visitante']}</strong></span></div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

def get_flag(pais):
    mapa = {"Argentina": "🇦🇷", "Canadá": "🇨🇦", "Francia": "🇫🇷", "Colombia": "🇨🇴", "Brasil": "🇧🇷", "Escocia": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "México": "🇲🇽", "Ecuador": "🇪🇨", "Alemania": "🇩🇪", "Japón": "🇯🇵", "España": "🇪🇸", "Costa Rica": "🇨🇷", "Inglaterra": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Irán": "🇮🇷"}
    return mapa.get(pais, "🏳️")
