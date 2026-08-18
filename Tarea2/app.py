"""
Tarea #2 - Backend (Fase 2)
Oswaldo Antonio Choc Cuteres - 201901844

Expone un endpoint GET /inventario que recibe un item por query string,
lo inyecta como parametro en la consulta principal de Prolog
(procesar_inventario/5) usando PySwip, captura las variables unificadas
y las devuelve formateadas en un JSON. CORS habilitado para permitir
peticiones desde el navegador (frontend).
"""

import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from pyswip import Prolog

app = Flask(__name__)

# Middleware de CORS: permite que el frontend (servido en otro
# origen/puerto, ej. Live Server o file://) pueda hacer fetch a esta API
# sin ser bloqueado por el navegador.
CORS(app)

# Instancia unica del motor de Prolog para toda la vida de la app.
prolog = Prolog()

# Ruta absoluta al archivo .pl, para que funcione sin importar desde
# donde se ejecute "python app.py".
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PL_PATH = os.path.join(BASE_DIR, "inventario.pl")

# Carga (consulta) el archivo de Prolog al iniciar el servidor.
prolog.consult(PL_PATH)


@app.route("/inventario", methods=["GET"])
def obtener_inventario():
    """
    GET /inventario?item=<nombre>

    Ejemplo: GET /inventario?item=espada
    """
    item_buscado = request.args.get("item", "").strip().lower()

    if not item_buscado:
        return jsonify({"error": "Debes enviar el parametro 'item' en la URL, ej: /inventario?item=espada"}), 400

    # Se construye la consulta a Prolog inyectando el parametro recibido
    # desde el frontend. Se envuelve en comillas simples para que
    # siempre sea tratado como atomo valido de Prolog, sin importar
    # el texto que el usuario haya escrito.
    consulta = (
        f"procesar_inventario('{item_buscado}', Total, Invertido, Unico, Ordenado)"
    )

    try:
        resultados = list(prolog.query(consulta))
    except Exception as e:
        return jsonify({"error": f"Error al consultar Prolog: {str(e)}"}), 500

    if not resultados:
        return jsonify({"error": "No se pudo procesar el inventario"}), 404

    # Prolog puede devolver varias soluciones; se toma la primera.
    solucion = resultados[0]

    # Se capturan las variables unificadas por Prolog y se formatean
    # en un diccionario serializable a JSON.
    respuesta = {
        "item_buscado": item_buscado,
        "total_items": solucion["Total"],
        "inventario_invertido": [str(i) for i in solucion["Invertido"]],
        "inventario_unico": [str(i) for i in solucion["Unico"]],
        "inventario_ordenado": [str(i) for i in solucion["Ordenado"]],
    }

    return jsonify(respuesta), 200


@app.route("/", methods=["GET"])
def home():
    # Ruta simple solo para confirmar que el servidor esta arriba.
    return jsonify({"status": "ok", "mensaje": "Backend de inventario RPG corriendo"}), 200


if __name__ == "__main__":
    # Puerto 5000 por defecto de Flask, no hardcodeado a uno que
    # pueda estar ocupado por otro proceso del sistema.
    app.run(host="0.0.0.0", port=5000, debug=True)
