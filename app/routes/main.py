import re

from flask import Blueprint, current_app, render_template, request

from app.services.github import get_song_content, get_song_list

main_bp = Blueprint("main", __name__)


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
            line_with_chords = re.sub(r"\[([^\]]+)\]", r"<span class='chord'>\1</span>", line)
            html_lines.append(f"<p>{line_with_chords}</p>")

    return "\n".join(html_lines)


@main_bp.route("/")
def index():
    owner = current_app.config["GITHUB_OWNER"]
    repo = current_app.config["GITHUB_REPO"]
    path = current_app.config["GITHUB_PATH"]

    songs = get_song_list(owner, repo, path)
    sorted_songs = sorted(songs, key=lambda s: s.lower())
    alphabetized_songs = {}
    for song in sorted_songs:
        first_letter = song[0].upper()
        alphabetized_songs.setdefault(first_letter, []).append(song)
    return render_template("index.html", alphabetized_songs=alphabetized_songs)


@main_bp.route("/search", methods=["POST"])
def search():
    query = request.form.get("query")
    owner = current_app.config["GITHUB_OWNER"]
    repo = current_app.config["GITHUB_REPO"]
    path = current_app.config["GITHUB_PATH"]

    songs = get_song_list(owner, repo, path)
    results = [song for song in songs if query and query.lower() in song.lower()]
    return render_template("search_results.html", query=query, results=results)


@main_bp.route("/song/<filename>")
def show_song(filename):
    owner = current_app.config["GITHUB_OWNER"]
    repo = current_app.config["GITHUB_REPO"]
    path = current_app.config["GITHUB_PATH"]

    try:
        song_content = get_song_content(owner, repo, filename, path)
        html_content = chordpro_to_html(song_content)
        return render_template(
            "show_song.html",
            song_content=html_content,
            filename=filename,
            key="E",
        )
    except Exception as exc:
        return f"Error al cargar la canción: {exc}", 500
