import os
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# 1. Cargamos las claves del archivo .env
load_dotenv()

# 2. Configuración de conexión (usando variables de entorno)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv('SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
    scope="user-read-recently-played"
))

try:
    print("--- Iniciando extracción de datos de Mood para Synesthesia ---")
    
    # 3. Buscamos tus canciones recientes
    results = sp.current_user_recently_played(limit=20)
    tracks = results['items']
    
    lista_moods = []
    
    for item in tracks:
        track = item['track']
        t_id = track['id']
        
        # 4. OBTENER EL MOOD (Audio Features)
        features = sp.audio_features([t_id])[0]
        
        # Clasificación básica de estado de ánimo
        valence = features['valence'] # Qué tan "positiva" es (0 a 1)
        energy = features['energy']   # Qué tan "enérgica" es (0 a 1)
        
        mood = "Neutral"
        if valence > 0.5 and energy > 0.5: mood = "Alegre / Enérgico"
        elif valence < 0.5 and energy < 0.5: mood = "Triste / Melancólico"
        elif valence > 0.5 and energy < 0.5: mood = "Relajado / Chill"
        else: mood = "Intenso / Oscuro"

        lista_moods.append({
            'titulo': track['name'],
            'artista': track['artists'][0]['name'],
            'mood': mood,
            'danceability': features['danceability'],
            'energy': energy,
            'valence': valence,
            'fecha_escuchada': item['played_at']
        })
    
    # 5. Crear el DataFrame y la carpeta data
    df = pd.DataFrame(lista_moods)
    
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Carpeta 'data' creada con éxito.")
    
    # 6. Guardar el archivo final
    df.to_csv('data/analisis_mood.csv', index=False)
    print(f"¡ÉXITO! Se han guardado {len(df)} canciones con su análisis en 'data/analisis_mood.csv'.")

except Exception as e:
    print(f"Error durante la ejecución: {e}")