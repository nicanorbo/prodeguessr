import requests
import pandas as pd

# TU API KEY INTEGRADA
API_KEY = "2d3b6acc2c164c9ba075f7310a89c269" 
HEADERS = {'X-Auth-Token': API_KEY}

def obtener_partidos():
    """
    Intenta obtener partidos reales de la API. 
    Si falla o no hay datos futuros, carga los partidos del Mundial 2026.
    """
    
    # Intentamos buscar partidos de la Copa Mundial (ID común suele ser WC o 2000, probamos uno genérico)
    # Nota: En la versión gratuita, a veces 'WC' no está disponible hasta cerca del evento.
    url = "https://api.football-data.org/v4/competitions/WC/matches" 
    
    try:
        print("🔄 Conectando a API Football-Data.org...")
        response = requests.get(url, headers=HEADERS, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            matches_list = data.get('matches', [])
            
            if matches_list:
                partidos_procesados = []
                for match in matches_list[:10]: # Tomamos los primeros 10
                    partidos_procesados.append({
                        "local": match['homeTeam']['name'],
                        "visitante": match['awayTeam']['name'],
                        "fecha": match['utcDate'],
                        "es_real": True
                    })
                print("✅ Datos reales obtenidos de la API.")
                return partidos_procesados
            else:
                print("⚠️ La API respondió pero no hay partidos disponibles en este endpoint.")
                
    except Exception as e:
        print(f"❌ Error de conexión con la API: {e}")

    # --- MODO RESPALDO: MUNDIAL 2026 SIMULADO ---
    print("🌍 Cargando modo simulación: Mundial 2026 (Datos de Respaldo)")
    return [
        {"local": "Argentina", "visitante": "Canadá", "fecha": "2026-06-15T20:00:00Z", "es_real": False},
        {"local": "Francia", "visitante": "Colombia", "fecha": "2026-06-16T15:00:00Z", "es_real": False},
        {"local": "Brasil", "visitante": "Escocia", "fecha": "2026-06-17T18:00:00Z", "es_real": False},
        {"local": "México", "visitante": "Ecuador", "fecha": "2026-06-18T21:00:00Z", "es_real": False},
        {"local": "Alemania", "visitante": "Japón", "fecha": "2026-06-19T14:00:00Z", "es_real": False},
        {"local": "España", "visitante": "Costa Rica", "fecha": "202