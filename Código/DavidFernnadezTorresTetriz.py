"""Interfaz gráfica para el juego Tetris."""
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
    
def iniciar_juego():
    ventana = tk.Tk()
    ventana.title("Tetris") 
    ventana.geometry("400x600")
    ventana.resizable(False, False)
    ventana.config(bg="black")

    # Cargar y mostrar el logo de Tetris
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        imagen_logo = Image.open(logo_path)
        imagen_logo = imagen_logo.resize((200, 100), Image.LANCZOS)
        logo = ImageTk.PhotoImage(imagen_logo)
        label_logo = tk.Label(ventana, image=logo, bg="black")
        label_logo.image = logo  # Mantener referencia
        label_logo.pack(pady=20)
    else:
        label_logo = tk.Label(ventana, text="TETRIS", bg="black", fg="white", font=("Arial", 24, "bold"))
        label_logo.pack(pady=20)

    # Botón para jugar
    boton_jugar = tk.Button(ventana, text="Jugar", bg="blue", fg="white", font=("Arial", 14), width=10, height=2, command=lambda: jugar(ventana, boton_jugar))
    boton_jugar.pack(pady=20)
    boton_jugar.bind("<Enter>", lambda e: boton_jugar.config(bg="lightblue"))
    boton_jugar.bind("<Leave>", lambda e: boton_jugar.config(bg="blue"))
    # Botón para salir
    boton_salir = tk.Button(ventana, text="Salir", bg="red", fg="white", font=("Arial", 14), width=10, height=2, command=ventana.quit)
    boton_salir.pack(pady=20)
    boton_salir.bind("<Enter>", lambda e: boton_salir.config(bg="lightcoral"))
    boton_salir.bind("<Leave>", lambda e: boton_salir.config(bg="red"))
    # Botón para estadísticas
    boton_estadisticas = tk.Button(ventana, text="Estadísticas", bg="green", fg="white", font=("Arial", 14), width=10, height=2, command=mostrar_estadisticas)
    boton_estadisticas.pack(pady=20)
    boton_estadisticas.bind("<Enter>", lambda e: boton_estadisticas.config(bg="lightgreen"))
    boton_estadisticas.bind("<Leave>", lambda e: boton_estadisticas.config(bg="green"))

    ventana.mainloop()

def ventana_estadisticas():
    ventana_estadisticas = tk.Toplevel()
    ventana_estadisticas.title("Estadísticas")
    ventana_estadisticas.geometry("300x200")
    ventana_estadisticas.config(bg="black")

    # Aquí puedes agregar widgets para mostrar estadísticas
    label_estadisticas = tk.Label(ventana_estadisticas, text="Estadísticas del juego", bg="black", fg="white", font=("Arial", 14))
    label_estadisticas.pack(pady=20)
    # Botón para cerrar la ventana de estadísticas
    boton_cerrar = tk.Button(ventana_estadisticas, text="Cerrar", bg="red", fg="white", font=("Arial", 14), command=ventana_estadisticas.destroy)
    boton_cerrar.pack(pady=20)
    boton_cerrar.bind("<Enter>", lambda e: boton_cerrar.config(bg="lightcoral"))
    boton_cerrar.bind("<Leave>", lambda e: boton_cerrar.config(bg="red"))

def mostrar_estadisticas():
    messagebox.showinfo("Estadísticas", "Aquí van las estadísticas del juego.")
    ventana_estadisticas()

def jugar(ventana, boton_jugar):
    messagebox.showinfo("Juego", "¡El juego ha comenzado!") 
    boton_jugar.config(state=tk.DISABLED)


iniciar_juego()