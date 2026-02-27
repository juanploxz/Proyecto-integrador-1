import pandas as pd
import json

# Lee el archivo CSV
df = pd.read_csv('movies_initial.csv')

# Guarda el DataFrame como JSON
df.to_json('movies.json', orient='records')

# (Opcional) Leer para comprobar que sí quedó bien
with open('movie/management/commands/movies.json', 'r', encoding='utf-8') as file:
    movies = json.load(file)

print("Total movies:", len(movies))
print("First movie:", movies[0] if movies else "No data")