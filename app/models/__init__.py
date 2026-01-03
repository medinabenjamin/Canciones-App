from app.extensions import db


playlist_cancion = db.Table(
    "playlist_cancion",
    db.Column("playlist_id", db.Integer, db.ForeignKey("playlists.id"), primary_key=True),
    db.Column("cancion_id", db.Integer, db.ForeignKey("canciones.id"), primary_key=True),
)


class Rol(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    descripcion = db.Column(db.String(255))

    usuarios = db.relationship("Usuario", back_populates="rol", lazy=True)


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=True)

    rol = db.relationship("Rol", back_populates="usuarios")
    participaciones = db.relationship("Participacion", back_populates="usuario", lazy=True)


class Cancion(db.Model):
    __tablename__ = "canciones"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    artista = db.Column(db.String(200))
    tono = db.Column(db.String(40))

    participaciones = db.relationship("Participacion", back_populates="cancion", lazy=True)
    playlists = db.relationship("PlaylistPlan", secondary=playlist_cancion, back_populates="canciones")


class Servicio(db.Model):
    __tablename__ = "servicios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.String(255))

    participaciones = db.relationship("Participacion", back_populates="servicio", lazy=True)


class Participacion(db.Model):
    __tablename__ = "participaciones"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    cancion_id = db.Column(db.Integer, db.ForeignKey("canciones.id"), nullable=False)
    servicio_id = db.Column(db.Integer, db.ForeignKey("servicios.id"), nullable=True)
    instrumento = db.Column(db.String(120))

    usuario = db.relationship("Usuario", back_populates="participaciones")
    cancion = db.relationship("Cancion", back_populates="participaciones")
    servicio = db.relationship("Servicio", back_populates="participaciones")


class PlaylistPlan(db.Model):
    __tablename__ = "playlists"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.String(255))
    fecha = db.Column(db.Date)

    canciones = db.relationship("Cancion", secondary=playlist_cancion, back_populates="playlists")
