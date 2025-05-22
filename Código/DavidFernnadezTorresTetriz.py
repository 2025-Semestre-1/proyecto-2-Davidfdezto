"""Interfaz gráfica para el juego Tetris."""
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# Fuente retro para los botones
FUENTE_RETRO = ("Press Start 2P", 12, "bold")

def longitud(secuencia):
    """Función personalizada para reemplazar len()"""
    contador = 0
    for _ in secuencia:
        contador += 1
    return contador

def agregar(lista, elemento):
    """Función personalizada para reemplazar append()"""
    return lista + [elemento]  # Crear una nueva lista con el elemento añadido

def iniciar_juego():
    ventana = tk.Tk()
    ventana.title("Tetris") 
    ventana.geometry("400x600")
    ventana.resizable(False, False)
    ventana.config(bg="#1a1a2e")  # Azul marino oscuro
    
    # Cargar y mostrar el logo de Tetris
    img = Image.open("Código/logo.png")
    # Redimensionar la imagen
    img = img.resize((250, 125), Image.Resampling.LANCZOS)
    title = ImageTk.PhotoImage(img)
    tetris = tk.Label(ventana, image=title, bg="#1a1a2e")  # Mismo color de fondo
    tetris.image = title 
    tetris.pack(pady=20)

    # Botón para jugar
    boton_jugar = tk.Button(
        ventana,
        text="JUGAR",
        bg="#4ecca3", fg="#1a1a2e",
        font=FUENTE_RETRO,
        width=10, height=2,
        command=lambda: jugar(ventana, boton_jugar),
        relief=tk.GROOVE
    )
    boton_jugar.pack(pady=20)
    boton_jugar.bind("<Enter>", lambda e: boton_jugar.config(bg="#6be0bc"))
    boton_jugar.bind("<Leave>", lambda e: boton_jugar.config(bg="#4ecca3"))
    
    # Botón para salir
    boton_salir = tk.Button(
        ventana,
        text="SALIR",
        bg="#e84545", fg="white",
        font=FUENTE_RETRO,
        width=10, height=2,
        command=ventana.quit,
        relief=tk.GROOVE
    )
    boton_salir.pack(pady=20)
    boton_salir.bind("<Enter>", lambda e: boton_salir.config(bg="#ff6b6b"))
    boton_salir.bind("<Leave>", lambda e: boton_salir.config(bg="#e84545"))
    
    # Botón de estadísticas (texto más largo → width mayor)
    boton_estadisticas = tk.Button(
        ventana,
        text="ESTADÍSTICAS",
        bg="#ffd369", fg="#1a1a2e",
        font=FUENTE_RETRO,     # ← aquí
        width=14,    # ↑ antes era 10
        height=2,
        command=ventana_estadisticas,
        relief=tk.GROOVE
    )
    boton_estadisticas.pack(pady=20)
    boton_estadisticas.bind("<Enter>", lambda e: boton_estadisticas.config(bg="#ffe085"))
    boton_estadisticas.bind("<Leave>", lambda e: boton_estadisticas.config(bg="#ffd369"))

    ventana.mainloop()

def ventana_estadisticas():
    ventana_estadisticas = tk.Toplevel()
    ventana_estadisticas.title("Estadísticas")
    ventana_estadisticas.geometry("600x700")
    ventana_estadisticas.config(bg="#1a1a2e")  # Color coherente con ventana principal

    # Aquí puedes agregar widgets para mostrar estadísticas
    label_estadisticas = tk.Label(
        ventana_estadisticas,
        text="ESTADÍSTICAS DEL JUEGO",
        bg="#1a1a2e", fg="white",
        font=FUENTE_RETRO   
    )
    label_estadisticas.pack(pady=20)
    
    # Botón para cerrar la ventana de estadísticas
    boton_cerrar = tk.Button(
        ventana_estadisticas,
        text="CERRAR",
        bg="#e84545", fg="white",
        font=FUENTE_RETRO,   # ← y aquí
        command=ventana_estadisticas.destroy,
        relief=tk.GROOVE
    )
    boton_cerrar.pack(pady=20, side=tk.BOTTOM)
    boton_cerrar.bind("<Enter>", lambda e: boton_cerrar.config(bg="#ff6b6b"))
    boton_cerrar.bind("<Leave>", lambda e: boton_cerrar.config(bg="#e84545"))
    #Texto de estadísticas
    texto_estadisticas = tk.Text(
        ventana_estadisticas,
        bg="#1a1a2e", fg="white",
        font=FUENTE_RETRO,   # ← y aquí
        width=30, height=20, wrap=tk.WORD
    )
    texto_estadisticas.pack(pady=20)
    texto_estadisticas.insert(tk.END, "Ranking de las últimas partidas:\n\n")
    


def interpretar_matriz():
    """Lee la matriz desde un archivo de texto"""
    try:
        # Intentar abrir el archivo (probando diferentes nombres)
        archivo_encontrado = False
        matriz = []
        
        for nombre_archivo in ["matriz", "Matriz", "matriz.txt", "Matriz.txt"]:
            try:
                ruta_completa = f"Código/{nombre_archivo}"
                print(f"Intentando abrir: {ruta_completa}")
                with open(ruta_completa, "r") as archivo:
                    lineas = archivo.readlines()
                    archivo_encontrado = True
                    break
            except FileNotFoundError:
                continue
        
        if not archivo_encontrado:
            print("No se encontró el archivo de matriz")
            messagebox.showerror("Error", "No se encontró el archivo de matriz")
            return None
            
        # Procesar cada línea del archivo
        for linea in lineas:
            linea = linea.strip()  # Quitar espacios y saltos de línea
            if not linea:  # Ignorar líneas vacías
                continue
                
            # Separar por comas (o por el separador que uses)
            elementos = linea.split(",")
            fila = []
            for elemento in elementos:
                fila = agregar(fila, elemento.strip())
            matriz = agregar(matriz, fila)

        return matriz
        
    except Exception as e:
        print(f"Error al leer la matriz desde archivo: {e}")
        messagebox.showerror("Error", f"Error al leer la matriz: {e}")
        return None


def mostrar_matriz(ventana_juego):
    # Frame contenedor para la matriz
    frame_juego = tk.Frame(ventana_juego, bg="#1a1a2e", bd=4, relief=tk.GROOVE)
    frame_juego.pack(pady=30, padx=30)
    
    matriz = interpretar_matriz()
    # Verificar si la matriz se cargó correctamente
    if matriz is None:
        return
    
    
    # Recorrer la matriz y crear labels coloreados
    for i in range(longitud(matriz)): 
        for j in range(longitud(matriz[i])): 
            # Convertir explícitamente a string y eliminar espacios
            celda = str(matriz[i][j]).strip()
            # Asignar colores según el contenido O la posición
            es_borde = (i == 0 or i == longitud(matriz) - 1 or j == 0 or j == longitud(matriz[i]) - 1)
            
            # Usar la posición o el contenido, lo que sea más fiable
            if es_borde or celda == "+":
                color = "#ff6b6b"  # Rojo brillante para bordes
            else:
                color = "#1a1a2e"  # Color de fondo para el interior
            
            # Crear una label con borde visible
            label = tk.Label(
                frame_juego,
                bg=color,
                width=3,  
                height=1,
                borderwidth=1,
                relief=tk.RAISED  # Da efecto 3D a las celdas
            )
            
            # Colocar en la cuadrícula sin espacios
            label.grid(row=i, column=j, padx=0, pady=0)
    
    # Ajustar la ventana al contenido
    ventana_juego.update_idletasks()
    ventana_juego.geometry("")

def jugar(ventana, boton_jugar):
    print("Iniciando juego...")
    messagebox.showinfo("Juego", "¡El juego ha comenzado!") 
    boton_jugar.config(state=tk.DISABLED)
    
    # Crear ventana de juego
    ventana_juego = tk.Toplevel()
    ventana_juego.title("Tetris")
    ventana_juego.geometry("500x700")
    ventana_juego.resizable(False, False)  # Mejor mantenerla fija en juego real
    ventana_juego.config(bg="#1a1a2e")
    mostrar_matriz(ventana_juego)


if __name__ == "__main__":
    iniciar_juego()