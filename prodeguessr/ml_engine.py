from scipy.stats import poisson

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
    "Japón": {"ataque": 83, "defensa": 82, "xg_promedio": 1.6}
}

def predecir_marcador(local, visitante):
    stats_local = TEAM_STATS.get(local, {"ataque": 75, "defensa": 75, "xg_promedio": 1.2})
    stats_visitante = TEAM_STATS.get(visitante, {"ataque": 75, "defensa": 75, "xg_promedio": 1.2})

    lambda_local = max(0.1, (stats_local["ataque"] / stats_visitante["defensa"]) * stats_local["xg_promedio"] * 1.1)
    lambda_visitante = max(0.1, (stats_visitante["ataque"] / stats_local["defensa"]) * stats_visitante["xg_promedio"])

    max_prob = 0
    mejor_marcador = (0, 0)
    
    for g_local in range(6):
        for g_visitante in range(6):
            prob = poisson.pmf(g_local, lambda_local) * poisson.pmf(g_visitante, lambda_visitante)
            if prob > max_prob:
                max_prob = prob
                mejor_marcador = (g_local, g_visitante)

    diff = mejor_marcador[0] - mejor_marcador[1]
    if diff > 0:
        razon = f"El modelo detecta una superioridad táctica de {local}. Su ataque ({stats_local['ataque']}) explota las debilidades defensivas de {visitante}. Se espera que controle la posesión y marque mediante jugadas combinadas."
    elif diff < 0:
        razon = f"Sorpresa táctica: {visitante} tiene las herramientas para neutralizar a {local}. Su eficiencia en transición rápida y solidez defensiva ({stats_visitante['defensa']}) les permitirá aprovechar los espacios dejados por la línea alta rival."
    else:
        razon = f"Equilibrio total. Las métricas de ambos equipos son muy similares. El partido se decidirá en detalles mínimos, probablemente un balón parado. La defensa de ambos anulará las creatividades ofensivas."

    return {
        "goles_local": mejor_marcador[0],
        "goles_visitante": mejor_marcador[1],
        "xg_local": round(lambda_local, 2),
        "xg_visitante": round(lambda_visitante, 2),
        "razon": razon,
        "confianza": f"{round(max_prob * 100, 1)}%"
    }
