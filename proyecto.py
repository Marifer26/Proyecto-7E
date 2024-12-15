import tkinter as tk
from tkinter import messagebox
import sqlite3
from collections import Counter

# Función para conectar a la base de datos externa
def conectar_base_datos():
    return sqlite3.connect("pastel.db")

# Funciones para manejar el diagnóstico
def diagnosticar():
    conexion = conectar_base_datos()
    cursor = conexion.cursor()

    respuestas = Counter()

    # Obtener preguntas desde la base de datos
    cursor.execute("SELECT pregunta, problema FROM preguntas")
    preguntas = cursor.fetchall()

    total_problemas = Counter([pregunta[1] for pregunta in preguntas])

    for texto, problema in preguntas:
        respuesta = messagebox.askyesno("Diagnóstico", texto)
        if respuesta:
            respuestas[problema] += 1

    if respuestas:
        # Calcular probabilidades conjuntas
        total_respuestas = sum(respuestas.values())
        resultados = []
        for problema, count in respuestas.items():
            probabilidad = (count / total_respuestas) * 100
            cursor.execute("SELECT solucion FROM problemas WHERE nombre = ?", (problema,))
            solucion = cursor.fetchone()
            if solucion:
                resultados.append((problema, solucion[0], probabilidad))

        # Mostrar resultados ordenados por probabilidad
        resultados.sort(key=lambda x: x[2], reverse=True)
        mensaje = "Resultados del diagnóstico:\n\n"
        for problema, solucion, probabilidad in resultados:
            mensaje += f"Problema: {problema}\nProbabilidad: {probabilidad:.1f}%\nSolución: {solucion}\n\n"
        messagebox.showinfo("Resultado", mensaje)
    else:
        messagebox.showinfo("Resultado", "Tu pastel parece estar bien!")

    conexion.close()

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Diagnóstico de Pasteles")
ventana.geometry("500x300")
ventana.configure(bg="#E6E6FA")

# Etiqueta principal
titulo = tk.Label(ventana, text="Tuviste problema al hornear tu postre ?", bg="#E6E6FA", fg="#8E44AD", font=("Arial", 16, "bold"))
titulo.pack(pady=20)

# Botón de diagnóstico
boton_diagnostico = tk.Button(ventana, text="Iniciar Diagnóstico", bg="#D5F5E3", font=("Arial", 12, "bold"), command=diagnosticar)
boton_diagnostico.pack(pady=20)

# Botón para salir
boton_salir = tk.Button(ventana, text="Salir", bg="#F5B7B1", font=("Arial", 12, "bold"), command=ventana.quit)
boton_salir.pack(pady=10)

ventana.mainloop()
