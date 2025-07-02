import tkinter as tk
from datetime import datetime
import json

# Cargar empleados desde el JSON
with open("empleados.json", "r", encoding="utf-8") as f:
    empleados = json.load(f)

# Buscar empleado por ID
def buscar_empleado(id_input):
    for emp in empleados:
        if emp["id"] == id_input:
            return emp
    return None

# Función para procesar el ID cuando se pulsa OK
def procesar_id():
    user_id = entry_id.get()
    empleado = buscar_empleado(user_id)
    
    if not empleado:
        lbl_resultado.config(text="⚠️ ID no encontrado", fg="red")
    else:
        nombre = empleado["nombre"]
        hora = datetime.now().strftime("%H:%M:%S")
        lbl_resultado.config(text=f"✅ Fichaje: {nombre} a las {hora}", fg="green")
    
    entry_id.delete(0, tk.END)

# Función para escribir número en el Entry
def escribir_numero(num):
    entry_id.insert(tk.END, str(num))

# Función para borrar último carácter
def corregir():
    contenido = entry_id.get()
    entry_id.delete(0, tk.END)
    entry_id.insert(0, contenido[:-1])

# -----------------------------
# INTERFAZ
root = tk.Tk()
root.title("Sistema de Fichajes")

# Entry donde se muestra el ID
entry_id = tk.Entry(root, font=("Arial", 24), justify="center")
entry_id.pack(pady=10)

# Teclado numérico
frame_teclado = tk.Frame(root)
frame_teclado.pack()

botones = [
    ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
    ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
    ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
    ('0', 3, 1)
]

for (texto, fila, col) in botones:
    tk.Button(frame_teclado, text=texto, width=5, height=2, font=("Arial", 18),
              command=lambda t=texto: escribir_numero(t)).grid(row=fila, column=col, padx=5, pady=5)

# Botón Corregir
tk.Button(frame_teclado, text="←", width=5, height=2, font=("Arial", 18),
          command=corregir).grid(row=3, column=0, padx=5, pady=5)

# Botón OK
tk.Button(frame_teclado, text="OK", width=5, height=2, font=("Arial", 18),
          command=procesar_id).grid(row=3, column=2, padx=5, pady=5)

# Resultado
lbl_resultado = tk.Label(root, text="", font=("Arial", 14))
lbl_resultado.pack(pady=10)

root.mainloop()
