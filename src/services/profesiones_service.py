from src.models.db import db

from src.models.profesiones_model import Profesion
from datetime import datetime
import uuid

class ProfesionesService:
    @staticmethod
    def get_all():
        return Profesion.query.all()

    @staticmethod
    def get_by_id(profesion_id):
        return Profesion.query.filter_by(id=profesion_id).first()

    @staticmethod
    def get_by_nombre(nombre):
        return Profesion.query.filter_by(nombre=nombre).first()

    @staticmethod
    def create(nombre, descripcion):
        nueva_profesion = Profesion(
            id=str(uuid.uuid4()),
            nombre=nombre,
            descripcion=descripcion,
            fecha=datetime.utcnow()
        )
        db.session.add(nueva_profesion)
        db.session.commit()
        return nueva_profesion

    @staticmethod
    def update(profesion_id, nombre=None, descripcion=None):
        profesion = Profesion.query.filter_by(id=profesion_id).first()
        if not profesion:
            return None
        if nombre:
            profesion.nombre = nombre
        if descripcion:
            profesion.descripcion = descripcion
        db.session.commit()
        return profesion

    @staticmethod
    def delete(profesion_id):
        profesion = Profesion.query.filter_by(id=profesion_id).first()
        if not profesion:
            return False
        db.session.delete(profesion)
        db.session.commit()
        return True