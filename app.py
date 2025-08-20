from flask import Flask, render_template, request
import requests
import re

app = Flask(__name__)

# Configuración del repositorio de GitHub
OWNER = "ucbtrigales"
REPO = "acordes"
PATH = "Chordpro"  # Si los archivos están dentro de una subcarpeta, cámbialo aquí

# Función para obtener la lista de canciones desde GitHub
def get_song_list_github(owner, repo, path=""):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "acordes-app"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")
    items = response.json()
    songs = [item["name"] for item in items if item["name"].endswith((".cho", ".txt", ".chordpro"))]
    return songs

#función para transformar los acordes de chordpro 
def chordpro_to_html(content):
    """
    Convierte chordpro a HTML con acordes encima de la letra.
    """
    lines = content.splitlines()
    html_lines = []

    for line in lines:
        if line.startswith("{title:") or line.startswith("{t:"):
            title = line.split(":", 1)[1].rstrip("}").strip()
            html_lines.append(f"<h2>{title}</h2>")
        elif line.startswith("{artist:") or line.startswith("{a:"):
            artist = line.split(":", 1)[1].rstrip("}").strip()
            html_lines.append(f"<h4>{artist}</h4>")
        elif line.startswith("{"):
            continue
        else:
            # Reemplaza los acordes con la etiqueta span y la clase 'chord'
            line_with_chords = re.sub(r"\[([^\]]+)\]", r"<span class='chord'>\1</span>", line)
            
            # Ahora, la línea completa tiene las etiquetas, solo necesitamos un contenedor.
            html_lines.append(f"<p>{line_with_chords}</p>")

    return "\n".join(html_lines)

# Función para obtener el contenido de una canción desde GitHub
def get_song_content_github(owner, repo, filename, path=""):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}/{filename}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "acordes-app"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")
    item = response.json()
    download_url = item["download_url"]
    raw = requests.get(download_url)
    return raw.text

# Ruta principal: lista de canciones ordenadas alfabéticamente
@app.route("/")
def index():
    songs = get_song_list_github(OWNER, REPO, PATH)
    sorted_songs = sorted(songs, key=lambda s: s.lower())
    alphabetized_songs = {}
    for song in sorted_songs:
        first_letter = song[0].upper()
        alphabetized_songs.setdefault(first_letter, []).append(song)
    return render_template("index.html", alphabetized_songs=alphabetized_songs)

# Ruta de búsqueda
@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query")
    songs = get_song_list_github(OWNER, REPO, PATH)
    results = [song for song in songs if query.lower() in song.lower()]
    return render_template("search_results.html", query=query, results=results)

# Ruta para mostrar el contenido de una canción
@app.route("/song/<filename>")
def show_song(filename):
    try:
        song_content = get_song_content_github(OWNER, REPO, filename, PATH)
        html_content = chordpro_to_html(song_content)
        return render_template("show_song.html", song_content=html_content, filename=filename, key="E")
    except Exception as e:
        return f"Error al cargar la canción: {e}", 500

if __name__ == "__main__":
    app.run(debug=True)