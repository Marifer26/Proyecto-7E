import sqlite3

def crear_base_datos():
    conexion = sqlite3.connect("pastel.db")
    cursor = conexion.cursor()

    # Crear tabla de problemas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS problemas (
            id INTEGER PRIMARY KEY,
            nombre TEXT UNIQUE,
            solucion TEXT
        )
    ''')

    # Crear tabla de preguntas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS preguntas (
            id INTEGER PRIMARY KEY,
            pregunta TEXT,
            problema TEXT,
            FOREIGN KEY (problema) REFERENCES problemas (nombre)
        )
    ''')

    # Insertar problemas
    problemas = [
        ("Pastel quemado", "Reduce la temperatura del horno y revisa el tiempo de cocción."),
        ("Pastel crudo", "Asegúrate de que el horno esté precalentado y extiende el tiempo de cocción."),
        ("Pastel desinflado", "No abras el horno durante la cocción y verifica que el polvo de hornear esté fresco."),
        ("Pastel con grietas", "Usa menos temperatura y evita sobrebatir la mezcla.")
    ]
    cursor.executemany("INSERT OR IGNORE INTO problemas (nombre, solucion) VALUES (?, ?)", problemas)

    # Insertar preguntas
    preguntas = [
        ("¿Notas un olor a quemado inusual?", "Pastel quemado"),
        ("¿El pastel tiene un color muy oscuro en las orillas?", "Pastel quemado"),
        ("¿El pastel tiene una textura muy húmeda en el centro?", "Pastel crudo"),
        ("¿El centro del pastel parece gelatinoso?", "Pastel crudo"),
        ("¿Se hundió el pastel después de sacarlo del horno?", "Pastel desinflado"),
        ("¿Notaste que el pastel no subió bien?", "Pastel desinflado"),
        ("¿Las superficies del pastel están agrietadas y desiguales?", "Pastel con grietas"),
        ("¿Hay líneas profundas en la parte superior del pastel?", "Pastel con grietas")
    ]
    cursor.executemany("INSERT OR IGNORE INTO preguntas (pregunta, problema) VALUES (?, ?)", preguntas)

    conexion.commit()
    conexion.close()
    print("Base de datos creada exitosamente.")

crear_base_datos()

