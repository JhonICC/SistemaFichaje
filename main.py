import tkinter as tk
from datetime import datetime
import json
import csv
import os
import winsound

# ------------------------
# CONFIGURACIÓN DE DATOS
# ------------------------
with open("empleados.json", "r", encoding="utf-8") as f:
    empleados = json.load(f)

CSV_FILE = "fichaje.csv"

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["fecha", "hora", "id", "nombre", "accion"])

# ------------------------
# FUNCIONES DE NEGOCIO
# ------------------------
def buscar_empleado(id_input):
    for emp in empleados:
        if emp["id"] == id_input:
            return emp
    return None

def verificar_si_ya_ficho_entrada_hoy(id_input):
    hoy = datetime.now().strftime("%Y-%m-%d")
    try:
        with open(CSV_FILE, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["fecha"] == hoy and row["id"] == id_input and row["accion"] == "Entrada":
                    return True
    except:
        pass
    return False

def registrar_fichaje(id_input, nombre, accion):
    fecha = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M:%S")
    with open(CSV_FILE, "a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([fecha, hora, id_input, nombre, accion])

# ------------------------
# FUNCIONES DE LA INTERFAZ
# ------------------------
def beep():
    winsound.Beep(1000, 100)  # beep simple, puedes cambiar por un wav con PlaySound

def procesar_id():
    beep()
    user_id = entry_id.get()
    empleado = buscar_empleado(user_id)
    if not empleado:
        mostrar_resultado("⚠️ ID no encontrado", "red")
        return

    nombre = empleado["nombre"]
    if verificar_si_ya_ficho_entrada_hoy(user_id):
        mostrar_opciones_fichaje(user_id, nombre, modo="salida")
    else:
        mostrar_opciones_fichaje(user_id, nombre, modo="entrada")

def mostrar_opciones_fichaje(id_input, nombre, modo):
    limpiar_interfaz()
    global frame_main
    frame_main = tk.Frame(root, bg="#34495e")
    frame_main.pack(expand=True)

    lbl_info = tk.Label(frame_main, text=f"Hola {nombre}", font=("Helvetica", 22), bg="#34495e", fg="white")
    lbl_info.grid(row=0, column=0, columnspan=3, pady=10)

    if modo == "entrada":
        tk.Label(frame_main, bg="#34495e", width=8).grid(row=1, column=0)
        tk.Button(frame_main, text="Entrada", font=("Helvetica", 20), bg="#27ae60", fg="white",
                  width=8, height=2, command=lambda: (beep(), confirmar_fichaje(id_input, nombre, "Entrada"))
        ).grid(row=1, column=1, padx=20, pady=20)
    else:
        tk.Label(frame_main, bg="#34495e", width=8).grid(row=1, column=0)
        tk.Button(frame_main, text="Salida", font=("Helvetica", 20), bg="#2980b9", fg="white",
                  width=8, height=2, command=lambda: (beep(), confirmar_fichaje(id_input, nombre, "Salida"))
        ).grid(row=1, column=1, padx=20, pady=20)

    tk.Button(frame_main, text="Atrás", font=("Helvetica", 20), bg="#e67e22", fg="white",
              width=8, height=2, command=lambda: (beep(), volver_a_teclado())
    ).grid(row=1, column=2, padx=20, pady=20)

def confirmar_fichaje(id_input, nombre, accion):
    registrar_fichaje(id_input, nombre, accion)
    mostrar_resultado(f"✅ {accion} registrada\npara {nombre}", "#2ecc71")
    root.after(2000, volver_a_teclado)

def mostrar_resultado(mensaje, color):
    limpiar_interfaz()
    global frame_main
    frame_main = tk.Frame(root, bg="#34495e")
    frame_main.pack(expand=True)
    lbl_resultado = tk.Label(frame_main, text=mensaje, font=("Helvetica", 22), bg="#34495e", fg=color)
    lbl_resultado.pack(pady=40)

def volver_a_teclado():
    limpiar_interfaz()
    construir_teclado()

def limpiar_interfaz():
    for widget in root.winfo_children():
        widget.destroy()

# ------------------------
# TECLADO NUMÉRICO
# ------------------------
def escribir_numero(num):
    beep()
    entry_id.insert(tk.END, str(num))

def corregir():
    beep()
    contenido = entry_id.get()
    entry_id.delete(0, tk.END)
    entry_id.insert(0, contenido[:-1])

def construir_teclado():
    global entry_id, frame_main
    frame_main = tk.Frame(root, bg="#34495e")
    frame_main.pack(expand=True)

    entry_id = tk.Entry(frame_main, font=("Helvetica", 28), justify="center", bg="#ecf0f1", fg="#2c3e50")
    entry_id.pack(pady=20)
    
    frame_teclado = tk.Frame(frame_main, bg="#34495e")
    frame_teclado.pack()
    
    botones = [
        ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
        ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
        ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
        ('0', 3, 1)
    ]
    for (texto, fila, col) in botones:
        tk.Button(frame_teclado, text=texto, width=5, height=2, font=("Helvetica", 20, "bold"),
                  bg="#2980b9", fg="white", activebackground="#3498db",
                  command=lambda t=texto: escribir_numero(t)).grid(row=fila, column=col, padx=8, pady=8)

    tk.Button(frame_teclado, text="←", width=5, height=2, font=("Helvetica", 20, "bold"),
              bg="#e67e22", fg="white", command=corregir).grid(row=3, column=0, padx=8, pady=8)
    tk.Button(frame_teclado, text="OK", width=5, height=2, font=("Helvetica", 20, "bold"),
              bg="#27ae60", fg="white", command=procesar_id).grid(row=3, column=2, padx=8, pady=8)

# ------------------------
# INICIAR APP
root = tk.Tk()
root.title("Sistema de Fichajes")
root.configure(bg="#34495e")
root.geometry("600x500")  # ventana inicial
root.minsize(500, 400)    # tamaño mínimo
construir_teclado()
root.mainloop()
