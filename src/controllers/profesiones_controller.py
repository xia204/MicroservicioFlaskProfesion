from flask import Blueprint, request, jsonify
from src.services.profesiones_service import ProfesionesService
import requests
from src.utils.status import obtener_status

profesiones_controller = Blueprint('profesiones', __name__)

STATUS_URL_BASE = 'http://localhost:8080/api/status'

def obtener_status(status_id):
    response = requests.get(f'http://localhost:8080/api/status/{status_id}')
    if response.status_code == 200:
        status_data = response.json()
        return {
            'id': status_data.get('id'),
            'nombre': status_data.get('nombre')
        }
    return None


@profesiones_controller.route('/profesiones', methods=['GET'])
def get_profesiones():
    try:
        profesiones = ProfesionesService.get_all()
        resultado = []

        for profesion in profesiones:
            status_data = obtener_status(profesion.status_id)
            resultado.append(profesion.to_dict(status_data))

        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@profesiones_controller.route('/profesiones/<string:profesion_id>', methods=['GET'])
def get_profesion(profesion_id):
    try:
        profesion = ProfesionesService.get_by_id(profesion_id)
        if not profesion:
            return jsonify({'error': 'Profesion no encontrada'}), 404
        
        status_data = obtener_status(profesion.status_id)
        return jsonify(profesion.to_dict(status_data)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@profesiones_controller.route('/profesiones/nombre/<string:nombre>', methods=['GET'])
def get_profesion_by_nombre(nombre):
    try:
        profesion = ProfesionesService.get_by_nombre(nombre)
        if not profesion:
            return jsonify({'error': 'Profesion no encontrada'}), 404
        
        status_data = obtener_status(profesion.status_id)
        return jsonify(profesion.to_dict(status_data)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@profesiones_controller.route('/profesiones', methods=['POST'])
def create_profesion():
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        status_id = data.get('status_id')

        if not nombre or not descripcion or not status_id:
            return jsonify({'error': 'Nombre, descripcion y status_id son requeridos'}), 400

        # Validar que el status exista
        status_data = obtener_status(status_id)
        if not status_data:
            return jsonify({'error': 'status_id inválido o no encontrado en el microservicio status'}), 400

        nueva_profesion = ProfesionesService.create(nombre, descripcion, status_id)
        return jsonify(nueva_profesion.to_dict(status_data)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@profesiones_controller.route('/profesiones/<string:profesion_id>', methods=['PUT'])
def update_profesion(profesion_id):
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        status_id = data.get('status_id')

        # Si se actualiza el status, validarlo
        if status_id:
            status_data = obtener_status(status_id)
            if not status_data:
                return jsonify({'error': 'status_id inválido o no encontrado'}), 400
        else:
            status_data = None

        profesion_actualizada = ProfesionesService.update(profesion_id, nombre, descripcion, status_id)
        if not profesion_actualizada:
            return jsonify({'error': 'Profesion no encontrada'}), 404

        return jsonify(profesion_actualizada.to_dict(status_data)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@profesiones_controller.route('/profesiones/<string:profesion_id>', methods=['DELETE'])
def delete_profesion(profesion_id):
    try:
        if not ProfesionesService.delete(profesion_id):
            return jsonify({'error': 'Profesion no encontrada'}), 404
        return jsonify({'message': 'Profesion eliminada exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
