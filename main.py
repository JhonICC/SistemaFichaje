import tkinter as tk
from datetime import datetime
import json

with open("empleados.json", "r", encoding="utf-8") as f:
    empleados = json.load(f)

def buscar_empleado(id_input):
    for emp in empleados:
        if emp["id"] == id_input:
            return emp
    return None

def procesar_id():
    user_id = entry_id.get()
    empleado = buscar_empleado(user_id)
    if not empleado:
        lbl_resultado.config(text="⚠️ ID no encontrado", fg="red")
    else:
        nombre = empleado["nombre"]
        hora = datetime.now().strftime("%H:%M:%S")
        lbl_resultado.config(text=f"✅ Fichaje: {nombre} a las {hora}", fg="#2ecc71")
    entry_id.delete(0, tk.END)

def escribir_numero(num):
    entry_id.insert(tk.END, str(num))

def corregir():
    contenido = entry_id.get()
    entry_id.delete(0, tk.END)
    entry_id.insert(0, contenido[:-1])

# ---------- INTERFAZ PERSONALIZADA ----------
root = tk.Tk()
root.title("Sistema de Fichajes")
root.configure(bg="#84c1fa")  # fondo general

# Entry
entry_id = tk.Entry(root, font=("Helvetica", 28), justify="center", bg="#ecf0f1", fg="#000000")
entry_id.pack(pady=20)

# Teclado numérico
frame_teclado = tk.Frame(root, bg="#0300a8")
frame_teclado.pack()

botones = [
    ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
    ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
    ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
    ('0', 3, 1)
]

for (texto, fila, col) in botones:
    tk.Button(frame_teclado, text=texto, width=5, height=2, font=("Helvetica", 20, "bold"),
              bg="#2980b9", fg="white", activebackground="#3498db", activeforeground="white",
              command=lambda t=texto: escribir_numero(t)).grid(row=fila, column=col, padx=8, pady=8)

# Botón Corregir
tk.Button(frame_teclado, text="←", width=5, height=2, font=("Helvetica", 20, "bold"),
          bg="#e67e22", fg="white", activebackground="#d35400",
          command=corregir).grid(row=3, column=0, padx=8, pady=8)

# Botón OK
tk.Button(frame_teclado, text="OK", width=5, height=2, font=("Helvetica", 20, "bold"),
          bg="#27ae60", fg="white", activebackground="#2ecc71",
          command=procesar_id).grid(row=3, column=2, padx=8, pady=8)

# Resultado
lbl_resultado = tk.Label(root, text="", font=("Helvetica", 16), bg="#34495e", fg="white")
lbl_resultado.pack(pady=20)

root.mainloop()
