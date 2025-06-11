# src/models/ciudadano_model.py
from src.models.db import db
from datetime import datetime

# src/models/ciudadano_model.py
class Profesion(db.Model):
    __tablename__ = 'profesiones'
    id = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    descripcion = db.Column(db.String, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)  # <-- Agrega esto

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'fecha': self.fecha
        }
