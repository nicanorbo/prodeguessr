import requests

API_KEY = "2d3b6acc2c164c9ba075f7310a89c269" 
HEADERS = {'X-Auth-Token': API_KEY}

def obtener_partidos():
    url = "https://api.football-data.org/v4/competitions/WC/matches" 
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        if response.status_code == 200:
            data = response.json()
            matches_list = data.get('matches', [])
            if matches_list:
                return [{"local": m['homeTeam']['name'], "visitante": m['awayTeam']['name'], "fecha": m['utcDate'], "es_real": True} for m in matches_list[:10]]
    except Exception:
        pass

    return [
        {"local": "Argentina", "visitante": "Canadá", "fecha": "2026-06-15T20:00:00Z", "es_real": False},
        {"local": "Francia", "visitante": "Colombia", "fecha": "2026-06-16T15:00:00Z", "es_real": False},
        {"local": "Brasil", "visitante": "Escocia", "fecha": "2026-06-17T18:00:00Z", "es_real": False},
        {"local": "México", "visitante": "Ecuador", "fecha": "2026-06-18T21:00:00Z", "es_real": False},
        {"local": "Alemania", "visitante": "Japón", "fecha": "2026-06-19T14:00:00Z", "es_real": False}
    ]
