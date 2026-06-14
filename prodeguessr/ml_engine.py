import numpy as np
from scipy.stats import poisson

# Base de datos ampliada de Fuerza Táctica (Ataque/Defensa 0-100) y xG Promedio
# Estos valores simulan el rendimiento esperado para 2026 basado en tendencias actuales.
TEAM_STATS = {
    "Argentina": {"ataque": 92, "defensa": 88, "xg_promedio": 1.9},
    "Canadá": {"ataque": 74, "defensa": 72, "xg_promedio": 1.0},
    "Francia": {"ataque": 93, "defensa": 89, "xg_promedio": 2.2},
    "Colombia": {"ataque": 82, "defensa": 80, "xg_promedio": 1.4},
    "Brasil": {"ataque": 91, "defensa": 85, "xg_promedio": 2.1},
    "Escocia": {"ataque": 76, "defensa": 78, "xg_promedio": 1.1},
    "México": {"ataque": 79, "defensa": 77, "xg_promedio": 1.3},
    "Ecuador": {"ataque": 78, "defensa": 81, "xg_promedio": 1.2},
    "Alemania": {"ataque": 89, "defensa": 86, "xg_promedio": 2.0},
    "Japón": {"ataque": 83, "defensa": 82, "xg_promedio": 1.6},
    "España": {"ataque": 90, "defensa": 87, "xg_promedio": 2.3},
    "Costa Rica": {"ataque": 70, "defensa": 75, "xg_promedio": 0.8},
    "Inglaterra": {"ataque": 91, "defensa": 88, "xg_promedio": 2.1},
    "Irán": {"ataque": 75, "defensa": 79, "xg_promedio": 1.0}
}

def predecir_marcador(local, visitante):
    """
    Usa Distribución de Poisson para calcular el marcador exacto más probable.
    """
    
    # 1. Obtener stats (con valores por defecto si el equipo es nuevo)
    stats_local = TEAM_STATS.get(local, {"ataque": 75, "defensa": 75, "xg_promedio": 1.2})
    stats_visitante = TEAM_STATS.get(visitante, {"ataque": 75, "defensa": 75, "xg_promedio": 1.2})

    # 2. Calcular Goles Esperados (xG) Ajustados por Matchup
    # Factor de ventaja local: 1.1x
    factor_ventaja_local = 1.1
    
    # Cálculo de fuerza relativa
    fuerza_ofensiva_local = (stats_local["ataque"] / stats_visitante["defensa"]) * stats_local["xg_promedio"] * factor_ventaja_local
    fuerza_ofensiva_visitante = (stats_visitante["ataque"] / stats_local["defensa"]) * stats_visitante["xg_promedio"]

    # Redondeamos para usar en Poisson
    lambda_local = max(0.1, fuerza_ofensiva_local) # Evitar negativos
    lambda_visitante = max(0.1, fuerza_ofensiva_visitante)

    # 3. Matriz de Probabilidad de Poisson (0 a 5 goles)
    max_prob = 0
    mejor_marcador = (0, 0)
    
    # Exploramos combinaciones de goles hasta 5
    for g_local in range(6):
        for g_visitante in range(6):
            prob_combinacion = poisson.pmf(g_local, lambda_local) * poisson.pmf(g_visitante, lambda_visitante)
            
            if prob_combinacion > max_prob:
                max_prob = prob_combinacion
                mejor_marcador = (g_local, g_visitante)

    # 4. Generar Narrativa Táctica
    diff_goles = mejor_marcador[0] - mejor_marcador[1]
    
    if diff_goles > 0:
        ganador = local
        narrativa = f"El modelo detecta una superioridad táctica de {local}. Su ataque ({stats_local['ataque']}) explota las debilidades defensivas de {visitante}. Se espera que {local} controle la posesión y marque mediante jugadas combinadas, mientras que {visitante} dependerá de contragolpes aislados."
    elif diff_goles < 0:
        ganador = visitante
        narrativa = f"Sorpresa táctica: {visitante} tiene las herramientas para neutralizar a {local}. Su eficiencia en transición rápida y solidez defensiva ({stats_visitante['defensa']}) les permitirá aprovechar los espacios dejados por la línea alta de {local}. El marcador refleja una victoria merecida por eficacia clínica."
    else:
        ganador = "Empate"
        narrativa = f"Equilibrio total. Las métricas de ambos equipos son muy similares en todas las líneas. El partido se decidirá en detalles mínimos, probablemente un balón parado o un error individual. La defensa de ambos equipos anulará las creatividades ofensivas, llevando a un resultado justo."

    return {
        "goles_local": mejor_marcador[0],
        "goles_visitante": mejor_marcador[1],
        "xg_local": round(lambda_local, 2),
        "xg_visitante": round(lambda_visitante, 2),
        "ganador": ganador,
        "razon": narrativa,
        "confianza": f"{round(max_prob * 100, 1)}%"
    }