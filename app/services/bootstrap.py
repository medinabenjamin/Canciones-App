import os

from app.extensions import bcrypt, db
from app.models import Rol, Usuario


def ensure_roles_and_admin():
    inspector = db.inspect(db.engine)
    if not inspector.has_table("roles") or not inspector.has_table("usuarios"):
        return

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

    admin_role = Rol.query.filter_by(nombre="Admin").first()
    admin_exists = False
    if admin_role:
        admin_exists = Usuario.query.filter_by(rol_id=admin_role.id).first() is not None

    if not admin_exists and admin_role:
        admin_email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
        admin_password = os.environ.get("ADMIN_PASSWORD", "admin123")
        admin_name = os.environ.get("ADMIN_NAME", "Administrador")
        password_hash = bcrypt.generate_password_hash(admin_password).decode("utf-8")
        admin_user = Usuario(
            nombre=admin_name,
            email=admin_email,
            password_hash=password_hash,
            rol=admin_role,
        )
        db.session.add(admin_user)
        db.session.commit()
