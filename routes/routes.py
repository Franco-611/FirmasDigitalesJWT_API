from flask import Blueprint, jsonify, request
import psycopg2
from datetime import datetime


# Crear un Blueprint
routes = Blueprint('routes', __name__)

# Establece la conexión a la base de datos
try:
    connection = psycopg2.connect(
        host='localhost',
        database='FirmasDigitalesJWT',
        user='auth',
        password='prueba'
    )
except Exception as error:
    print(f"No se pudo conectar a la base de datos debido a: {error}")
    connection = None

@routes.route('/usuarios', methods=['GET'])
def get_users():
    if connection:
        cursor = connection.cursor()
        # Ejecuta la consulta para obtener todos los usuarios
        cursor.execute("SELECT * FROM usuarios;")  # Cambiado para seleccionar solo las columnas necesarias

        # Fetchall devuelve una lista de tuplas, convertimos cada tupla a un dict
        users = [{'usuario': row[0], 'contrasena': row[1]} for row in cursor.fetchall()]
        cursor.close()
        return jsonify(users)
    else:
        return jsonify({'error': 'Error al conectar con la base de datos'}), 500
    

@routes.route('/canciones', methods=['GET'])
def get_canciones():
    if connection:
        cursor = connection.cursor()
        # Ejecuta la consulta para obtener todos los usuarios
        cursor.execute("SELECT * FROM canciones;")  # Cambiado para seleccionar solo las columnas necesarias

        # Fetchall devuelve una lista de tuplas, convertimos cada tupla a un dict
        users = [{'nombre': row[0], 'info': row[1]} for row in cursor.fetchall()]
        cursor.close()
        return jsonify(users)
    else:
        return jsonify({'error': 'Error al conectar con la base de datos'}), 500
