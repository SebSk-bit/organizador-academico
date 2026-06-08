from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
def crear_base_datos():

    conexion = sqlite3.connect("database.db")

    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tareas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        materia TEXT,
        descripcion TEXT,
        fecha TEXT,
        estado TEXT
    )
    """)

    conexion.commit()
    conexion.close()
@app.route("/")
def inicio():

    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT COUNT(*) FROM tareas WHERE materia='Matemáticas' AND estado='Pendiente'")
    matematicas = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tareas WHERE materia='Lengua y Literatura' AND estado='Pendiente'")
    lengua = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tareas WHERE materia='Inglés' AND estado='Pendiente'")
    ingles = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tareas WHERE materia='Física' AND estado='Pendiente'")
    fisica = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tareas WHERE materia='Química' AND estado='Pendiente'")
    quimica = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tareas WHERE materia='Otras' AND estado='Pendiente'")
    otras = cursor.fetchone()[0]

    conexion.close()

    return render_template(
        "index.html",
        matematicas=matematicas,
        lengua=lengua,
        ingles=ingles,
        fisica=fisica,
        quimica=quimica,
        otras=otras
    )

@app.route("/guardar", methods=["POST"])
def guardar():

    titulo = request.form["titulo"]
    materia = request.form["materia"]
    descripcion = request.form["descripcion"]
    fecha = request.form["fecha"]

    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute("""
    INSERT INTO tareas
    (titulo, materia, descripcion, fecha, estado)
    VALUES (?, ?, ?, ?, ?)
    """, (titulo, materia, descripcion, fecha, "Pendiente"))

    conexion.commit()
    conexion.close()

    return redirect("/")
@app.route("/eliminar/<int:id>")
def eliminar(id):

    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT materia FROM tareas WHERE id = ?",
        (id,)
    )

    resultado = cursor.fetchone()

    if resultado:
        materia = resultado[0]
    else:
        conexion.close()
        return redirect("/")

    cursor.execute(
        "DELETE FROM tareas WHERE id = ?",
        (id,)
    )

    conexion.commit()
    conexion.close()

    if materia == "Matemáticas":
        return redirect("/matematicas")
    elif materia == "Inglés":
        return redirect("/ingles")
    elif materia == "Física":
        return redirect("/fisica")
    elif materia == "Química":
        return redirect("/quimica")
    elif materia == "Lengua y Literatura":
        return redirect("/lengua")
    else:
        return redirect("/otras")
@app.route("/completar/<int:id>")
def completar(id):

    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT materia FROM tareas WHERE id = ?",
        (id,)
    )

    materia = cursor.fetchone()[0]

    cursor.execute("""
    UPDATE tareas
    SET estado = 'Completada'
    WHERE id = ?
    """, (id,))

    conexion.commit()
    conexion.close()

    if materia == "Matemáticas":
        return redirect("/matematicas")
    elif materia == "Inglés":
        return redirect("/ingles")
    elif materia == "Física":
        return redirect("/fisica")
    elif materia == "Química":
        return redirect("/quimica")
    elif materia == "Lengua y Literatura":
        return redirect("/lengua")
    else:
        return redirect("/otras")
@app.route("/matematicas")
def matematicas():

    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT * FROM tareas
    WHERE materia = 'Matemáticas'
    ORDER BY fecha ASC
    """)

    tareas = cursor.fetchall()

    conexion.close()

    return render_template(
        "materia.html",
        tareas=tareas,
        nombre_materia="Matemáticas",
        clase_color="matematicas"
    )
@app.route("/lengua")
def lengua():

    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT * FROM tareas
    WHERE materia = 'Lengua y Literatura'
    ORDER BY fecha ASC
    """)

    tareas = cursor.fetchall()

    conexion.close()

    return render_template(
        "materia.html",
        tareas=tareas,
        nombre_materia="Lengua y Literatura",
        clase_color="lengua"
    )
@app.route("/ingles")
def ingles():

    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT * FROM tareas
    WHERE materia = 'Inglés'
    ORDER BY fecha ASC
    """)

    tareas = cursor.fetchall()

    conexion.close()

    return render_template(
        "materia.html",
        tareas=tareas,
        nombre_materia="Inglés",
        clase_color="ingles"
    )
@app.route("/fisica")
def fisica():

    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT * FROM tareas
    WHERE materia = 'Física'
    ORDER BY fecha ASC
    """)

    tareas = cursor.fetchall()

    conexion.close()

    return render_template(
        "materia.html",
        tareas=tareas,
        nombre_materia="Física",
        clase_color="fisica"
    )
@app.route("/quimica")
def quimica():

    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT * FROM tareas
    WHERE materia = 'Química'
    ORDER BY fecha ASC
    """)

    tareas = cursor.fetchall()

    conexion.close()

    return render_template(
        "materia.html",
        tareas=tareas,
        nombre_materia="Química",
        clase_color="quimica"
    )
@app.route("/otras")
def otras():

    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT * FROM tareas
    WHERE materia = 'Otras'
    ORDER BY fecha ASC
    """)

    tareas = cursor.fetchall()

    conexion.close()

    return render_template(
        "materia.html",
        tareas=tareas,
        nombre_materia="Otras",
        clase_color="otras"
    )
crear_base_datos()

if __name__ == "__main__":
    app.run(debug=True)