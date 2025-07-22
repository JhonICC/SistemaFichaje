import tkinter as tk
from datetime import datetime, timedelta
import json
import csv
import os
import winsound
from collections import defaultdict
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

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

def obtener_estado_empleado(id_input):
    hoy = datetime.now().strftime("%Y-%m-%d")
    acciones = []
    try:
        with open(CSV_FILE, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["fecha"] == hoy and row["id"] == id_input:
                    acciones.append(row["accion"])
    except:
        pass

    # Estado según la última acción registrada
    ultimo = acciones[-1] if acciones else None

    estado = {
        "ultima": ultimo,
        "acciones": acciones
    }
    return estado

def registrar_fichaje(id_input, nombre, accion):
    fecha = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M:%S")
    with open(CSV_FILE, "a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([fecha, hora, id_input, nombre, accion])

def calcular_duracion(hora_inicio, hora_fin):
    """Devuelve la duración en formato HH:MM entre dos horas."""
    if not hora_inicio or not hora_fin:
        return timedelta()
    formato = "%H:%M:%S"
    try:
        inicio = datetime.strptime(hora_inicio, formato)
        fin = datetime.strptime(hora_fin, formato)
        if fin < inicio:  # por si salieran después de medianoche (no común, pero por si acaso)
            fin += timedelta(days=1)
        return fin - inicio
    except ValueError:
        return timedelta()

def generar_resumen_diario():
    hoy = datetime.now().strftime("%Y-%m-%d")
    resumen_path = f"Resumenes/resumen_{hoy}.xlsx"
    fichajes_por_empleado = defaultdict(lambda: {
        "nombre": "",
        "acciones": {"Entrada": "", "Descanso": "", "Regreso": "", "Salida": ""}
    })

    # Leer fichajes
    try:
        with open(CSV_FILE, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["fecha"] == hoy:
                    id_emp = row["id"]
                    fichajes_por_empleado[id_emp]["nombre"] = row["nombre"]
                    fichajes_por_empleado[id_emp]["acciones"][row["accion"]] = row["hora"]
    except FileNotFoundError:
        print("⚠️ Archivo de fichajes no encontrado.")
        return

    # Crear archivo Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Resumen Diario"

    headers = ["ID", "Nombre", "Entrada", "Descanso", "Regreso", "Salida", "Descanso Total", "Trabajo Total"]
    ws.append(headers)

    for id_emp, datos in fichajes_por_empleado.items():
        entrada = datos["acciones"]["Entrada"]
        descanso = datos["acciones"]["Descanso"]
        regreso = datos["acciones"]["Regreso"]
        salida = datos["acciones"]["Salida"]

        # Calcular tiempos
        tiempo_descanso = calcular_duracion(descanso, regreso)
        tiempo_trabajo = calcular_duracion(entrada, salida) - tiempo_descanso

        # Formateo
        def fmt(t):
            if not t or t.total_seconds() == 0:
                return "00:00"
            total_minutes = int(t.total_seconds() // 60)
            horas = total_minutes // 60
            minutos = total_minutes % 60
            return f"{horas:02}:{minutos:02}"

        fila = [
            id_emp,
            datos["nombre"],
            entrada,
            descanso,
            regreso,
            salida,
            fmt(tiempo_descanso),
            fmt(tiempo_trabajo)
        ]
        ws.append(fila)

    # Estilizar cabecera
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center")

    # Ajustar ancho de columnas
    for column_cells in ws.columns:
        length = max(len(str(cell.value)) if cell.value else 0 for cell in column_cells)
        ws.column_dimensions[column_cells[0].column_letter].width = length + 4

    # Guardar archivo
    wb.save(resumen_path)
    print(f"✅ Resumen diario guardado en: {resumen_path}")


# ------------------------
# FUNCIONES DE LA INTERFAZ
# ------------------------
def beep():
    winsound.Beep(1000, 100)

def procesar_id():
    beep()
    user_id = entry_id.get()
    empleado = buscar_empleado(user_id)
    if not empleado:
        mostrar_resultado("⚠️ ID no encontrado", "red")
        root.after(3000, volver_a_teclado)
        return

    nombre = empleado["nombre"]
    estado = obtener_estado_empleado(user_id)
    ultima = estado["ultima"]

    if ultima in [None, "Salida"]:
        mostrar_opciones_fichaje(user_id, nombre, ["Entrada", "Atrás"])
    elif ultima == "Entrada":
        mostrar_opciones_fichaje(user_id, nombre, ["Descanso", "Salida", "Atrás"])
    elif ultima == "Descanso":
        mostrar_opciones_fichaje(user_id, nombre, ["Regreso", "Salida", "Atrás"])
    elif ultima == "Regreso":
        mostrar_opciones_fichaje(user_id, nombre, ["Salida", "Atrás"])
    else:
        mostrar_resultado("⚠️ Acción no válida", "red")
        root.after(2000, volver_a_teclado)

def mostrar_opciones_fichaje(id_input, nombre, acciones):
    limpiar_interfaz()
    global frame_main
    frame_main = tk.Frame(root, bg="#34495e")
    frame_main.pack(expand=True)

    lbl_info = tk.Label(frame_main, text=f"Hola {nombre}", font=("Helvetica", 22), bg="#34495e", fg="white")
    lbl_info.grid(row=0, column=0, columnspan=3, pady=10)

    for i, accion in enumerate(acciones):
        color = {
            "Entrada": "#27ae60",
            "Salida": "#2980b9",
            "Descanso": "#f39c12",
            "Regreso": "#8e44ad",
            "Atrás": "#e67e22"
        }.get(accion, "gray")

        tk.Button(frame_main, text=accion, font=("Helvetica", 20), bg=color, fg="white",
                  width=10, height=2,
                  command=lambda a=accion: (beep(), manejar_accion(a, id_input, nombre))
        ).grid(row=1, column=i, padx=10, pady=20)

def manejar_accion(accion, id_input, nombre):
    if accion == "Atrás":
        volver_a_teclado()
    else:
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
root.geometry("600x500")
root.minsize(500, 400)
construir_teclado()

def al_cerrar():
    generar_resumen_diario()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", al_cerrar)

root.mainloop()
