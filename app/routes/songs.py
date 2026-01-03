from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models import Cancion
from app.services.audit import log_action
from app.utils.auth import role_required

songs_bp = Blueprint("songs", __name__, url_prefix="/songs")


@songs_bp.route("/manage", methods=["GET", "POST"])
@login_required
@role_required("Admin", "Líder")
def manage_songs():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        artista = request.form.get("artista", "").strip()
        tono = request.form.get("tono", "").strip()
        if titulo:
            song = Cancion(
                titulo=titulo,
                artista=artista or None,
                tono=tono or None,
                creado_por_id=current_user.id,
                editado_por_id=current_user.id,
            )
            db.session.add(song)
            db.session.commit()
            log_action(current_user.id, "creado", "Cancion", song.id, f"Canción creada: {titulo}")
            return redirect(url_for("songs.manage_songs"))

    songs = Cancion.query.order_by(Cancion.titulo.asc()).all()
    return render_template("manage_songs.html", songs=songs)


@songs_bp.route("/<int:song_id>/edit", methods=["POST"])
@login_required
@role_required("Admin", "Líder")
def edit_song(song_id):
    song = Cancion.query.get_or_404(song_id)
    titulo = request.form.get("titulo", "").strip()
    artista = request.form.get("artista", "").strip()
    tono = request.form.get("tono", "").strip()
    if titulo:
        song.titulo = titulo
    song.artista = artista or None
    song.tono = tono or None
    song.editado_por_id = current_user.id
    db.session.commit()
    log_action(current_user.id, "actualizado", "Cancion", song.id, f"Canción editada: {song.titulo}")
    return redirect(url_for("songs.manage_songs"))
