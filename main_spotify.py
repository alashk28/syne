import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import os

# ====== CREDENCIALES ======
cid = "dfe6dd59c5d443a680ff422dfe3afdab"
secret = "af25cb2ea5414edf82cf74d709ae0815"
uri = "http://127.0.0.1:8000"

print("Iniciando análisis de Mood Musical (versión universitaria)...")

try:
    # ====== AUTENTICACIÓN ======
    scope = "user-read-recently-played"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=cid,
        client_secret=secret,
        redirect_uri=uri,
        scope=scope,
        open_browser=True,
        cache_path=".cache"
    ))

    # ====== CANCIONES RECIENTES ======
    results = sp.current_user_recently_played(limit=20)
    print("Conexión exitosa. Analizando canciones...")

    lista_moods = []

    for item in results["items"]:
        track = item["track"]
        if not track:
            continue

        popularity = track["popularity"]
        duration = track["duration_ms"] / 1000  # segundos
        explicit = track["explicit"]

        # ====== CLASIFICACIÓN DE MOOD ======
        if popularity > 75 and duration < 240:
            mood = "Alegre / Comercial"
        elif explicit and popularity > 60:
            mood = "Intenso / Explícito"
        elif popularity < 40 and duration > 260:
            mood = "Triste / Melancólico"
        elif duration > 300:
            mood = "Relajado / Ambiental"
        else:
            mood = "Neutro / Variado"

        lista_moods.append({
            "titulo": track["name"],
            "artista": track["artists"][0]["name"],
            "popularidad": popularity,
            "duracion_seg": int(duration),
            "explicit": explicit,
            "mood": mood
        })

    # ====== GUARDAR RESULTADOS ======
    if not os.path.exists("data"):
        os.makedirs("data")

    df = pd.DataFrame(lista_moods)
    df.to_csv("data/analisis_mood.csv", index=False)

    print("✅ ÉXITO: data/analisis_mood.csv generado")

except Exception as e:
    print("Error:", e)
