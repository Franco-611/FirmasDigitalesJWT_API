from flask import Blueprint, jsonify, request
import psycopg2
from datetime import datetime
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import jwt, os


# Función para cargar la clave privada desde un archivo
def load_private_key(filename):
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, filename)
    with open(file_path, "rb") as key_file:
        private_key_data = key_file.read()
        private_key = serialization.load_pem_private_key(
            private_key_data,
            password=None,
            backend=default_backend()
        )
    return private_key

def generarPublicKey():
    # Clave privada para firmar el JWT
    private_key = load_private_key("private_key.pem")
    # Generar clave pública a partir de la clave privada
    public_key = private_key.public_key()

    # Convertir clave pública a formato PEM
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )



    return public_key_pem.decode()

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


@routes.route('/publicKey', methods=['GET'])
def get_publicKey():
    if connection:
        public_key = generarPublicKey()
        return jsonify({'publicKey': public_key})
    else:
        return jsonify({'error': 'Error al conectar con la base de datos'}), 500
    

@routes.route('/decifrar', methods=['PUT'])
def get_decifrar():
    if connection:
        user_data = request.get_json()
        public_key_data = user_data.get('public_key')
        jwt_token = user_data.get('jwt_token')

        public_key_data_bytes = public_key_data.encode('utf-8')  # Convertir a bytes si los datos están en Unicode

        public_key = serialization.load_pem_public_key(
            public_key_data_bytes,
            backend=default_backend())


        # Verificar la firma del JWT y extraer la información del payload
        decoded_payload = jwt.decode(jwt_token, public_key, algorithms=['RS256'])


        return jsonify({'textoN': decoded_payload})
    else:
        return jsonify({'error': 'Error al conectar con la base de datos'}), 500
    

@routes.route('/insertar', methods=['POST'])
def insertar():
    if connection:
        user_data = request.get_json()
        user = user_data.get('usuario')
        contr = user_data.get('contra')

        try:
            cursor = connection.cursor()
            query_string = "INSERT INTO usuarios (usuario, contraseña) VALUES (%s, %s);"
            cursor.execute(query_string, (user, contr))
            connection.commit()  # Realizar la transacción
            cursor.close()
            return jsonify({'message': 'Usuario creado exitosamente'}), 201
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()  # Revertir la transacción en caso de error
            return jsonify({'error': str(error)}), 500
        
    else:
        return jsonify({'error': 'Error al conectar con la base de datos'}), 500