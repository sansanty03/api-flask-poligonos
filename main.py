from flask import Flask, jsonify
from flask_cors import CORS  # 👈 AÑADE ESTA LÍNEA
import mysql.connector
import os
import json

app = Flask(__name__)
CORS(app)  # 👈 AÑADE ESTA LÍNEA TAMBIÉN (DESPUÉS DE CREAR app)

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ['MYSQLHOST'],
        user=os.environ['MYSQLUSER'],
        password=os.environ['MYSQLPASSWORD'],
        database=os.environ['MYSQLDATABASE'],
        port=int(os.environ['MYSQLPORT'])
    )

@app.route('/poligonos', methods=['GET'])
def obtener_poligonos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            p.id, p.nombre, p.coordenadas,
            c.nombre AS categoria, c.color, c.fillColor, c.fillOpacity
        FROM poligonos p
        JOIN categorias c ON p.categoria_id = c.id
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()

    for r in resultados:
        try:
            r['coordenadas'] = json.loads(r['coordenadas'])
        except:
            r['coordenadas'] = []

    return jsonify(resultados)

@app.route('/marcadores', methods=['GET'])
def obtener_marcadores():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM marcadores WHERE activo = 1")
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultados)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
