from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required

from app.extensions import bcrypt, db
from app.models import Rol, Usuario
from app.services.audit import log_action
from app.utils.auth import role_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/users", methods=["GET", "POST"])
@login_required
@role_required("Admin", "Líder")
def manage_users():
    roles = Rol.query.order_by(Rol.nombre.asc()).all()
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        rol_id = request.form.get("rol_id")
        if nombre and email and password and rol_id:
            password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
            user = Usuario(nombre=nombre, email=email, password_hash=password_hash, rol_id=int(rol_id))
            db.session.add(user)
            db.session.commit()
            log_action(user.id, "creado", "Usuario", user.id, f"Usuario creado: {email}")
            return redirect(url_for("admin.manage_users"))

    users = Usuario.query.order_by(Usuario.nombre.asc()).all()
    return render_template("manage_users.html", users=users, roles=roles)


@admin_bp.route("/users/<int:user_id>/role", methods=["POST"])
@login_required
@role_required("Admin")  # Vista solo admin (RBAC)
def update_user_role(user_id):
    rol_id = request.form.get("rol_id")
    user = Usuario.query.get_or_404(user_id)
    if rol_id:
        user.rol_id = int(rol_id)
        db.session.commit()
        log_action(user_id, "actualizado", "Usuario", user_id, "Rol actualizado")
    return redirect(url_for("admin.manage_users"))


@admin_bp.route("/users/<int:user_id>/password", methods=["POST"])
@login_required
@role_required("Admin")
def reset_user_password(user_id):
    password = request.form.get("password", "")
    user = Usuario.query.get_or_404(user_id)
    if password:
        user.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        db.session.commit()
        log_action(user_id, "actualizado", "Usuario", user_id, "Contraseña restablecida")
    return redirect(url_for("admin.manage_users"))
