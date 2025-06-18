# src/models/ciudadano_model.py
from src.models.db import db
from datetime import datetime
from src.utils.status import obtener_status   

# src/models/ciudadano_model.py
class Profesion(db.Model):
    __tablename__ = 'profesiones'
    id = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    status_id = db.Column(db.String, nullable=False)
    descripcion = db.Column(db.String, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)  # <-- Agrega esto

    def to_dict(self, status_data=None):
        if not status_data:
            status_data = obtener_status(self.status_id)
        return {
            'id': self.id,
            'nombre': self.nombre,
            'status': status_data,
            'descripcion': self.descripcion,
            'fecha': self.fecha
        }