from flask import Flask, jsonify, request
import mysql.connector
import os
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
    plantel = request.args.get('plantel')
    if not plantel:
        return jsonify({"error": "Se requiere el parámetro 'plantel'"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            p.id, p.nombre, p.coordenadas, p.plantel,
            c.nombre AS categoria, c.color, c.fillColor, c.fillOpacity
        FROM poligonos p
        JOIN categorias c ON p.categoria_id = c.id
        WHERE p.plantel = %s
    """, (plantel,))
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
    plantel = request.args.get('plantel')
    if not plantel:
        return jsonify({"error": "Se requiere el parámetro 'plantel'"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM marcadores WHERE activo = 1 AND plantel = %s", (plantel,))
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultados)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
