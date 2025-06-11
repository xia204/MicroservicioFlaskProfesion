from flask import Blueprint, request, jsonify
from src.services.profesiones_service import ProfesionesService

profesiones_controller = Blueprint('profesiones', __name__)

@profesiones_controller.route('/profesiones', methods=['GET'])
def get_profesiones():
    #Get all professions
    try:
        profesiones = ProfesionesService.get_all()
        return jsonify([profesion.to_dict() for profesion in profesiones]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@profesiones_controller.route('/profesiones/<string:profesion_id>', methods=['GET'])
def get_profesion(profesion_id):
    #Get a profession by ID
    try:
        profesion = ProfesionesService.get_by_id(profesion_id)
        if not profesion:
            return jsonify({'error': 'Profesion no encontrada'}), 404
        return jsonify(profesion.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@profesiones_controller.route('/profesiones/<string:nombre>', methods=['GET'])
def get_profesion_by_nombre(nombre):
    #Get a profession by name
    try:
        profesion = ProfesionesService.get_by_nombre(nombre)
        if not profesion:
            return jsonify({'error': 'Profesion no encontrada'}), 404
        return jsonify(profesion.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@profesiones_controller.route('/profesiones', methods=['POST'])
def create_profesion():
    #Create a new profession
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        
        if not nombre or not descripcion:
            return jsonify({'error': 'Nombre y descripcion son requeridos'}), 400
        
        nueva_profesion = ProfesionesService.create(nombre, descripcion)
        return jsonify(nueva_profesion.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@profesiones_controller.route('/profesiones/<string:profesion_id>', methods=['PUT'])
def update_profesion(profesion_id):
    #Update a profession
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        
        profesion_actualizada = ProfesionesService.update(profesion_id, nombre, descripcion)
        if not profesion_actualizada:
            return jsonify({'error': 'Profesion no encontrada'}), 404
        return jsonify(profesion_actualizada.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500  
    
@profesiones_controller.route('/profesiones/<string:profesion_id>', methods=['DELETE'])
def delete_profesion(profesion_id):
    #Delete a profession
    try:
        if not ProfesionesService.delete(profesion_id):
            return jsonify({'error': 'Profesion no encontrada'}), 404
        return jsonify({'message': 'Profesion eliminada exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500