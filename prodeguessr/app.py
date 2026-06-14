import streamlit as st
import time
from api_client import obtener_partidos
from ml_engine import predecir_marcador

st.set_page_config(page_title="ProdeGuessr 2026", page_icon="🏆", layout="wide")

# CSS mejorado - Estética profesional de predicciones deportivas
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
    
    body {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    .main-header {
        text-align: center;
        font-size: 3rem;
        font-weight: 900;
        margin: 2rem 0 0.5rem 0;
        background: linear-gradient(90deg, #00B0B9 0%, #D2125E 50%, #FFD700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }
    .sub-header {
        text-align: center;
        color: #888;
        font-size: 0.9rem;
        margin-bottom: 3rem;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-weight: 600;
    }
    .matches-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
        gap: 20px;
        margin: 2rem 0;
    }
    .match-card {
        background: linear-gradient(145deg, #1a1a1a, #0d0d0d);
        border: 1px solid #333;
        border-radius: 16px;
        padding: 25px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .match-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #00B0B9, #D2125E);
    }
    .match-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 176, 185, 0.2);
        border-color: #00B0B9;
    }
    .match-teams {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    .team-block {
        text-align: center;
        flex: 1;
    }
    .team-flag {
        font-size: 3.5rem;
        margin-bottom: 10px;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
    }
    .team-name {
        font-size: 1.1rem;
        font-weight: 700;
        color: #fff;
        margin-top: 8px;
    }
    .vs-badge {
        background: linear-gradient(135deg, #D2125E, #00B0B9);
        color: white;
        font-weight: 900;
        font-size: 0.9rem;
        padding: 8px 16px;
        border-radius: 20px;
        margin: 0 15px;
    }
    .predict-btn {
        background: linear-gradient(90deg, #D2125E 0%, #00B0B9 100%);
        color: white;
        font-weight: 700;
        font-size: 1rem;
        border: none;
        border-radius: 12px;
        padding: 14px 24px;
        width: 100%;
        cursor: pointer;
        transition: all 0.3s;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 15px;
    }
    .predict-btn:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 20px rgba(210, 18, 94, 0.5);
    }
    .prediction-result {
        background: rgba(0, 176, 185, 0.1);
        border-left: 4px solid #00B0B9;
        padding: 20px;
        border-radius: 0 12px 12px 0;
        margin-top: 20px;
        animation: slideIn 0.5s ease-out;
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    .score-display {
        font-size: 2.5rem;
        font-weight: 900;
        color: #FFD700;
        text-align: center;
        margin: 15px 0;
        text-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
    }
    .analysis-box {
        background: rgba(0, 0, 0, 0.3);
        padding: 15px;
        border-radius: 8px;
        margin-top: 15px;
        font-size: 0.95rem;
        line-height: 1.6;
        color: #e0e0e0;
    }
    .stats-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 10px;
        margin-top: 15px;
        font-size: 0.85rem;
    }
    .stat-item {
        background: rgba(255, 255, 255, 0.05);
        padding: 10px;
        border-radius: 8px;
        text-align: center;
    }
    .stat-label {
        color: #888;
        font-size: 0.75rem;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    .stat-value {
        color: #00B0B9;
        font-weight: 700;
        font-size: 1.1rem;
    }
    .stButton>button {
        background: linear-gradient(90deg, #D2125E 0%, #00B0B9 100%);
        color: white;
        font-weight: 700;
        font-size: 1rem;
        border: none;
        border-radius: 12px;
        padding: 14px 24px;
        width: 100%;
        cursor: pointer;
        transition: all 0.3s;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 15px;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 20px rgba(210, 18, 94, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">⚽ PRODEGUESSR 🏆</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Predicciones Exactas • Mundial 2026</div>', unsafe_allow_html=True)

# Cargar partidos
partidos = obtener_partidos()

if not partidos:
    st.error("No se pudieron cargar partidos. Verifica tu conexión.")
else:
    # Crear grid de partidos
    st.markdown('<div class="matches-grid">', unsafe_allow_html=True)
    
    for idx, partido in enumerate(partidos):
        local = partido['local']
        visitante = partido['visitante']
        
        flag_local = get_flag(local)
        flag_visitante = get_flag(visitante)
        
        # Tarjeta de partido
        st.markdown(f"""
        <div class="match-card">
            <div class="match-teams">
                <div class="team-block">
                    <div class="team-flag">{flag_local}</div>
                    <div class="team-name">{local}</div>
                </div>
                <div class="vs-badge">VS</div>
                <div class="team-block">
                    <div class="team-flag">{flag_visitante}</div>
                    <div class="team-name">{visitante}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Botón de predicción
        if st.button(f"🔮 PREDECIR", key=f"btn_{idx}"):
            with st.spinner("Analizando estadísticas..."):
                time.sleep(1.5)
                resultado = predecir_marcador(local, visitante)
                
                st.markdown(f"""
                <div class="prediction-result">
                    <div class="score-display">{resultado['goles_local']} - {resultado['goles_visitante']}</div>
                    <div class="analysis-box">
                        <strong>📊 Análisis:</strong><br>
                        {resultado['razon']}
                    </div>
                    <div class="stats-grid">
                        <div class="stat-item">
                            <div class="stat-label">xG {local}</div>
                            <div class="stat-value">{resultado['xg_local']}</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-label">Confianza</div>
                            <div class="stat-value">{resultado['confianza']}</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-label">xG {visitante}</div>
                            <div class="stat-value">{resultado['xg_visitante']}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def get_flag(pais):
    mapa = {
        "Argentina": "🇦🇷", "Canadá": "🇨🇦", "Francia": "🇫🇷", "Colombia": "🇨🇴",
        "Brasil": "🇧🇷", "Escocia": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "México": "🇲🇽", "Ecuador": "🇪🇨",
        "Alemania": "🇩🇪", "Japón": "🇯🇵", "España": "🇪🇸", "Costa Rica": "🇨🇷",
        "Inglaterra": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Irán": "🇮🇷", "Estados Unidos": "🇺🇸", "Uruguay": "🇺🇾"
    }
    return mapa.get(pais, "🏳️")
