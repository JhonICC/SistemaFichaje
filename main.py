import tkinter as tk
from tkinter import messagebox
import json
import csv
import os
from datetime import datetime

# Cargar empleados
with open('empleados.json', 'r', encoding='utf-8') as f:
    empleados = json.load(f)

def buscar_empleado(id_usuario):
    for e in empleados:
        if e['id'] == id_usuario:
            return e
    return None

def ha_fichado_entrada(id_usuario):
    hoy = datetime.now().strftime('%Y-%m-%d')
    if not os.path.exists('fichajes.csv'):
        return False
    with open('fichajes.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for fila in reader:
            if fila['id'] == id_usuario and fila['fecha'] == hoy and fila['tipo'] == 'entrada':
                return True
    return False

def guardar_fichaje(empleado, tipo):
    ahora = datetime.now()
    fecha = ahora.strftime('%Y-%m-%d')
    hora = ahora.strftime('%H:%M:%S')
    archivo = 'fichajes.csv'

    nuevo_registro = [empleado['id'], empleado['nombre'], fecha, hora, tipo]

    existe = os.path.isfile(archivo)
    with open(archivo, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not existe:
            writer.writerow(['id', 'nombre', 'fecha', 'hora', 'tipo'])
        writer.writerow(nuevo_registro)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Fichaje simple")
        self.codigo = ""

        self.label = tk.Label(root, text="Introduce tu ID", font=("Arial", 24))
        self.label.pack(pady=10)

        self.display = tk.Label(root, text="", font=("Arial", 30))
        self.display.pack(pady=10)

        self.frame = tk.Frame(root)
        self.frame.pack()

        # Crear botones 0-9
        for i in range(10):
            btn = tk.Button(self.frame, text=str(i), font=("Arial", 18), width=4, height=2,
                            command=lambda x=i: self.agregar_digito(str(x)))
            btn.grid(row=i//5, column=i%5, padx=5, pady=5)

        self.borrar_btn = tk.Button(root, text="Borrar", font=("Arial", 18), command=self.borrar)
        self.borrar_btn.pack(pady=5)

    def agregar_digito(self, digito):
        if len(self.codigo) < 4:
            self.codigo += digito
            self.display.config(text=self.codigo)
        if len(self.codigo) == 4:
            self.procesar_codigo()

    def borrar(self):
        self.codigo = ""
        self.display.config(text="")

    def procesar_codigo(self):
        empleado = buscar_empleado(self.codigo)
        if not empleado:
            messagebox.showerror("Error", "ID no encontrado")
            self.borrar()
            return

        if not ha_fichado_entrada(self.codigo):
            guardar_fichaje(empleado, 'entrada')
            messagebox.showinfo("Fichaje", f"{empleado['nombre']} ha fichado ENTRADA")
        else:
            guardar_fichaje(empleado, 'salida')
            messagebox.showinfo("Fichaje", f"{empleado['nombre']} ha fichado SALIDA")

        self.borrar()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
