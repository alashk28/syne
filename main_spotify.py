import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import os

# Claves directas
cid = 'dfe6dd59c5d443a680ff422dfe3afdab'
secret = 'af25cb2ea5414edf82cf74d709ae0815'
uri = 'http://127.0.0.1:8000'

print("Iniciando programa...")

try:
    auth_manager = SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri=uri, scope="user-read-recently-played")
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
    # Obtener canciones
    results = sp.current_user_recently_played(limit=20)
    print("Conexion exitosa con Spotify")
    
    lista = []
    for item in results['items']:
        lista.append({'titulo': item['track']['name'], 'artista': item['track']['artists'][0]['name']})
    
    if not os.path.exists('data'): os.makedirs('data')
    pd.DataFrame(lista).to_csv('data/analisis_mood.csv', index=False)
    print("Archivo guardado en la carpeta data")

except Exception as e:
    print(f"Error real: {e}")