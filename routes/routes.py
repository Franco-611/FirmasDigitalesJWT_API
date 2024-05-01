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


