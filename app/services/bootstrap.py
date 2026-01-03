import os

from app.extensions import bcrypt, db
from app.models import Rol, Usuario


def ensure_roles_and_admin():
    role_names = [
        ("Admin", "Acceso total al sistema"),
        ("Líder", "Gestiona canciones y usuarios asignados"),
        ("Músico", "Acceso a canciones y participación"),
        ("Invitado", "Acceso limitado de lectura"),
    ]
    for name, description in role_names:
        role = Rol.query.filter_by(nombre=name).first()
        if not role:
            db.session.add(Rol(nombre=name, descripcion=description))

    db.session.commit()

    if Usuario.query.count() == 0:
        admin_email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
        admin_password = os.environ.get("ADMIN_PASSWORD", "admin123")
        admin_name = os.environ.get("ADMIN_NAME", "Administrador")
        admin_role = Rol.query.filter_by(nombre="Admin").first()
        password_hash = bcrypt.generate_password_hash(admin_password).decode("utf-8")
        admin_user = Usuario(
            nombre=admin_name,
            email=admin_email,
            password_hash=password_hash,
            rol=admin_role,
        )
        db.session.add(admin_user)
        db.session.commit()
