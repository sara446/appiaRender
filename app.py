from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista de tareas en memoria
tareas = []
task_id_counter = 1


@app.route("/tasks", methods=["GET"])
def obtener_tareas():
    return jsonify(tareas)


@app.route("/tasks", methods=["POST"])
def crear_tarea():
    global task_id_counter  # Usar variable global para el contador de tareas
    datos = request.get_json()  # Se debe usar 'request' en lugar de 'solicitud'

    if not datos or "titulo" not in datos:  # 'titulo' es con 't' minúscula
        return jsonify({"error": "El título es obligatorio"}), 400

    tarea = {
        "id": task_id_counter,
        "titulo": datos["titulo"],  # 'titulo' con 't' minúscula
        "descripcion": datos.get("descripcion", ""),  # 'descripcion' con 'd' minúscula
        "hecho": False,
    }

    tareas.append(tarea)  # 'añadir' debe ser 'append'
    task_id_counter += 1
    return jsonify(tarea), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def actualizar_tarea(task_id):
    datos = request.get_json()
    tarea = next(
        (t for t in tareas if t["id"] == task_id), None
    )  # Corregir 'siguiente' por 'next'

    if not tarea:
        return jsonify({"error": "Tarea no encontrada"}), 404

    if "titulo" in datos:
        tarea["titulo"] = datos["titulo"]
    if "descripcion" in datos:
        tarea["descripcion"] = datos["descripcion"]
    if "hecho" in datos:
        tarea["hecho"] = datos["hecho"]

    return jsonify(tarea)


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def eliminar_tarea(task_id):
    global tareas
    tarea = next((t for t in tareas if t["id"] == task_id), None)

    if not tarea:
        return jsonify({"error": "Tarea no encontrada"}), 404

    tareas = [t for t in tareas if t["id"] != task_id]  # Corregir el filtrado de tareas
    return jsonify({"message": "Tarea eliminada"})


if __name__ == "__main__":
    app.run(debug=True)
