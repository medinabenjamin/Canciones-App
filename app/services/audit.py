from app.extensions import db
from app.models import AuditLog


def log_action(usuario_id, accion, entidad, entidad_id=None, detalle=None):
    log = AuditLog(
        usuario_id=usuario_id,
        accion=accion,
        entidad=entidad,
        entidad_id=entidad_id,
        detalle=detalle,
    )
    db.session.add(log)
    db.session.commit()
