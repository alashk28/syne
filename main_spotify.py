import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import os

# Claves directas (ya validadas)
cid = 'dfe6dd59c5d443a680ff422dfe3afdab'
secret = 'af25cb2ea5414edf82cf74d709ae0815'
uri = 'http://127.0.0.1:8000'

print("Iniciando programa con análisis de Mood...")

try:
    auth_manager = SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri=uri, scope="user-read-recently-played")
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
    # 1. Obtener canciones recientes
    results = sp.current_user_recently_played(limit=20)
    print("Conexión exitosa. Analizando sentimientos musicales...")
    
    lista_moods = []
    for item in results['items']:
        track = item['track']
        # 2. Obtener características de audio (el MOOD)
        f = sp.audio_features([track['id']])[0]
        
        # Clasificación lógica para tu trabajo
        if f['valence'] > 0.5 and f['energy'] > 0.5: mood = "Alegre / Enérgico"
        elif f['valence'] < 0.5 and f['energy'] < 0.5: mood = "Triste / Melancólico"
        elif f['valence'] > 0.5 and f['energy'] < 0.5: mood = "Relajado / Chill"
        else: mood = "Intenso / Oscuro"
        
        lista_moods.append({
            'titulo': track['name'],
            'artista': track['artists'][0]['name'],
            'mood': mood,
            'valence': f['valence'],
            'energy': f['energy']
        })
    
    # 3. Guardar el archivo completo
    if not os.path.exists('data'): os.makedirs('data')
    pd.DataFrame(lista_moods).to_csv('data/analisis_mood.csv', index=False)
    print("¡ÉXITO! Ahora el archivo en la carpeta 'data' ya tiene la columna MOOD.")

except Exception as e:
    print(f"Error real: {e}")