"""Interfaz gráfica para el juego Tetris."""
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random

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


def mostrar_matriz(frame_matriz):
    # Frame contenedor para la matriz - ya recibimos el frame como parámetro
    matriz = interpretar_matriz()
    # Verificar si la matriz se cargó correctamente
    if matriz is None:
        return
    
    # Configurar el frame para expandirse
    for i in range(longitud(matriz)):
        frame_matriz.grid_rowconfigure(i, weight=1)
    for j in range(longitud(matriz[0])):
        frame_matriz.grid_columnconfigure(j, weight=1)
    
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
                frame_matriz,
                bg=color,
                borderwidth=1,
                relief=tk.RAISED  # Da efecto 3D a las celdas
            )
            
            # Colocar en la cuadrícula para que se expanda
            label.grid(row=i, column=j, sticky="nsew", padx=0, pady=0)


# Definiciones de las piezas de Tetris (tetriminos)
TETRIMINOS = {
    'I': [
        [[0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0]],
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0]],
        [[0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0]]
    ],
    'J': [
        [[1, 0, 0],
         [1, 1, 1],
         [0, 0, 0]],
        [[0, 1, 1],
         [0, 1, 0],
         [0, 1, 0]],
        [[0, 0, 0],
         [1, 1, 1],
         [0, 0, 1]],
        [[0, 1, 0],
         [0, 1, 0],
         [1, 1, 0]]
    ],
    'L': [
        [[0, 0, 1],
         [1, 1, 1],
         [0, 0, 0]],
        [[0, 1, 0],
         [0, 1, 0],
         [0, 1, 1]],
        [[0, 0, 0],
         [1, 1, 1],
         [1, 0, 0]],
        [[1, 1, 0],
         [0, 1, 0],
         [0, 1, 0]]
    ],
    'O': [
        [[0, 1, 1, 0],
         [0, 1, 1, 0],
         [0, 0, 0, 0]]
    ],
    'S': [
        [[0, 1, 1],
         [1, 1, 0],
         [0, 0, 0]],
        [[0, 1, 0],
         [0, 1, 1],
         [0, 0, 1]],
        [[0, 0, 0],
         [0, 1, 1],
         [1, 1, 0]],
        [[1, 0, 0],
         [1, 1, 0],
         [0, 1, 0]]
    ],
    'T': [
        [[0, 1, 0],
         [1, 1, 1],
         [0, 0, 0]],
        [[0, 1, 0],
         [0, 1, 1],
         [0, 1, 0]],
        [[0, 0, 0],
         [1, 1, 1],
         [0, 1, 0]],
        [[0, 1, 0],
         [1, 1, 0],
         [0, 1, 0]]
    ],
    'Z': [
        [[1, 1, 0],
         [0, 1, 1],
         [0, 0, 0]],
        [[0, 0, 1],
         [0, 1, 1],
         [0, 1, 0]],
        [[0, 0, 0],
         [1, 1, 0],
         [0, 1, 1]],
        [[0, 1, 0],
         [1, 1, 0],
         [1, 0, 0]]
    ]
}

# Colores para cada pieza
COLORES_TETRIMINOS = {
    'I': "#00f0f0",  # Cian
    'J': "#0000f0",  # Azul
    'L': "#f0a000",  # Naranja
    'O': "#f0f000",  # Amarillo
    'S': "#00f000",  # Verde
    'T': "#a000f0",  # Púrpura
    'Z': "#f00000"   # Rojo
}


def inicializar_tablero(frame_matriz):
    """Crea el tablero de juego como una matriz 2D de labels"""
    FILAS, COLUMNAS = 20, 10  # Dimensiones estándar del Tetris
    
    # Crear matriz vacía
    tablero = []
    
    # Configurar el frame para expandirse uniformemente
    for i in range(FILAS):
        frame_matriz.grid_rowconfigure(i, weight=1)
    for j in range(COLUMNAS):
        frame_matriz.grid_columnconfigure(j, weight=1)
    
    # Crear las celdas del tablero
    for i in range(FILAS):
        fila = []
        for j in range(COLUMNAS):
            # Crear label como celda
            celda = tk.Label(
                frame_matriz,
                bg="#1a2a6d",  # Color de fondo inicial
                borderwidth=1,
                relief=tk.RAISED  # Da efecto 3D a las celdas
            )
            celda.grid(row=i, column=j, sticky="nsew", padx=0, pady=0)
            fila = agregar(fila, celda)  # Usar agregar en vez de append
        tablero = agregar(tablero, fila)  # Usar agregar en vez de append
    
    return tablero


def iniciar_nuevas_piezas():
    """Genera una pieza actual y la siguiente aleatoriamente"""
    tipos = list(TETRIMINOS.keys())
    pieza_actual = random.choice(tipos)
    pieza_siguiente = random.choice(tipos)
    return pieza_actual, pieza_siguiente


def mostrar_siguiente_pieza(frame_siguiente, tipo_pieza):
    """Muestra la siguiente pieza en el panel lateral"""
    # Limpiar el frame
    for widget in frame_siguiente.winfo_children():
        widget.destroy()
    
    # Configurar grid
    pieza = TETRIMINOS[tipo_pieza][0]  # Tomar la primera rotación
    filas, columnas = longitud(pieza), longitud(pieza[0]);
    
    # Crear las celdas para la pieza
    for i in range(filas):
        for j in range(columnas):
            color = COLORES_TETRIMINOS[tipo_pieza] if pieza[i][j] == 1 else "#1a2a2e"
            celda = tk.Label(
                frame_siguiente,
                bg=color,
                width=2, height=1,
                borderwidth=1,
                relief=tk.RAISED
            )
            # Centrar la pieza
            celda.grid(row=i+1, column=j+1, padx=1, pady=1)


def actualizar_tablero(game_data):
    """Actualiza la visualización del tablero con la pieza actual"""
    # Limpiar solo las celdas que no están fijas
    tablero = game_data["tablero"]
    tablero_fijo = game_data.get("tablero_fijo", [])
    
    # Primero pintar el fondo en todas las celdas
    for i in range(longitud(tablero)):
        for j in range(longitud(tablero[0])):
            # Si la celda no está fijada, pintarla de fondo
            if tablero_fijo is None or i >= longitud(tablero_fijo) or j >= longitud(tablero_fijo[i]) or tablero_fijo[i][j] is None:
                tablero[i][j].config(bg="#1a2a6d")
    
    # Mostrar piezas fijas
    if tablero_fijo:
        for i in range(longitud(tablero_fijo)):
            for j in range(longitud(tablero_fijo[i])):
                if tablero_fijo[i][j] is not None:
                    tablero[i][j].config(bg=tablero_fijo[i][j])
    
    # Mostrar la pieza actual
    pieza = TETRIMINOS[game_data["pieza_actual"]][game_data["rotacion"]]
    color = COLORES_TETRIMINOS[game_data["pieza_actual"]]
    
    for i in range(longitud(pieza)):
        for j in range(longitud(pieza[i])):
            if pieza[i][j] == 1:
                y = game_data["y"] + i
                x = game_data["x"] + j
                
                # Verificar que está dentro de los límites
                if 0 <= y < longitud(tablero) and 0 <= x < longitud(tablero[0]):
                    tablero[y][x].config(bg=color)


def jugar(ventana, boton_jugar):
    print("Iniciando juego...")
    messagebox.showinfo("Juego", "¡El juego ha comenzado!") 
    boton_jugar.config(state=tk.DISABLED)
    
    # Crear ventana de juego
    ventana_juego = tk.Toplevel()
    ventana_juego.title("Tetris")
    ventana_juego.geometry("800x700")  # Más ancho para acomodar panel derecho
    ventana_juego.resizable(False, False)
    ventana_juego.config(bg="#1a1a2e")
    
    # Crear layout dividido en dos secciones
    # Frame para la matriz de juego (izquierda)
    frame_matriz = tk.Frame(ventana_juego, bg="#1a2a2e", bd=4, relief=tk.GROOVE)
    frame_matriz.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)

    # Frame para información del juego (derecha)
    frame_info = tk.Frame(ventana_juego, bg="#1a2a2e", bd=4, relief=tk.GROOVE, width=300)
    frame_info.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH)
    
    # Título para el panel de información
    label_info = tk.Label(
        frame_info,
        text="INFORMACIÓN",
        bg="#1a2a2e",
        fg="white",
        font=FUENTE_RETRO
    )
    label_info.pack(pady=10)
    
    # Etiqueta para la siguiente pieza
    label_siguiente = tk.Label(
        frame_info,
        text="SIGUIENTE PIEZA",
        bg="#1a2a2e",
        fg="white",
        font=FUENTE_RETRO
    )
    label_siguiente.pack(pady=20)
    
    # Frame para mostrar la siguiente pieza
    frame_siguiente = tk.Frame(
        frame_info,
        bg="#1a2a2e", 
        bd=2,
        relief=tk.SUNKEN,
        width=150,
        height=150
    )
    frame_siguiente.pack(pady=10)
    
    # Mostrar puntuación
    label_puntos = tk.Label(
        frame_info,
        text="PUNTOS: 0",
        bg="#1a2a2e",
        fg="white",
        font=FUENTE_RETRO
    )
    label_puntos.pack(pady=20)
    
    # Inicializar el juego y crear el tablero
    tablero = inicializar_tablero(frame_matriz)
    
    # Iniciar la pieza actual y su posición
    pieza_actual, pieza_siguiente = iniciar_nuevas_piezas()
    
    # Mostrar la siguiente pieza en el panel
    mostrar_siguiente_pieza(frame_siguiente, pieza_siguiente)
    
    # Variables de control del juego
    game_data = {
        "tablero": tablero,
        "pieza_actual": pieza_actual,
        "tipo_pieza": list(TETRIMINOS.keys())[0],  # Iniciar con la primera pieza
        "rotacion": 0,
        "x": 5,  # Posición horizontal inicial
        "y": 0,  # Posición vertical inicial
        "pieza_siguiente": pieza_siguiente,
        "frame_siguiente": frame_siguiente,
        "puntos": 0,
        "label_puntos": label_puntos,
        "juego_activo": True,
        "ventana_juego": ventana_juego,  # Guardar referencia a la ventana
        "boton_jugar": boton_jugar  # Guardar referencia al botón
    }
    
    # Actualizar visualización inicial
    actualizar_tablero(game_data)
    
    # Configurar eventos de teclado
    ventana_juego.bind("<Left>", lambda event: mover_pieza(game_data, -1, 0))
    ventana_juego.bind("<Right>", lambda event: mover_pieza(game_data, 1, 0))
    ventana_juego.bind("<Down>", lambda event: mover_pieza(game_data, 0, 1))
    ventana_juego.bind("<space>", lambda event: rotar_pieza(game_data))
    ventana_juego.focus_set()  # Dar foco a la ventana para capturar eventos de teclado
    
    # Iniciar bucle de caída automática
    ventana_juego.after(1000, lambda: caida_automatica(ventana_juego, game_data))


def mover_pieza(game_data, delta_x, delta_y):
    """Mueve la pieza en la dirección especificada si es posible"""
    if not game_data["juego_activo"]:
        return
    
    # Guardar posición actual para poder restaurarla
    x_original, y_original = game_data["x"], game_data["y"]
    
    # Intentar mover
    game_data["x"] += delta_x
    game_data["y"] += delta_y
    
    # Verificar si es un movimiento válido
    if es_movimiento_valido(game_data):
        # Actualizar tablero
        actualizar_tablero(game_data)
    else:
        # Restaurar posición
        game_data["x"], game_data["y"] = x_original, y_original
        
        # Si intentó moverse hacia abajo y falló, significa que la pieza debe fijarse
        if delta_y > 0:
            fijar_pieza(game_data)


def rotar_pieza(game_data):
    """Rota la pieza si es posible"""
    if not game_data["juego_activo"]:
        return
    
    # Guardar rotación actual
    rotacion_original = game_data["rotacion"]
    
    # Calcular nueva rotación
    rotaciones_totales = longitud(TETRIMINOS[game_data["pieza_actual"]])
    game_data["rotacion"] = (game_data["rotacion"] + 1) % rotaciones_totales
    
    # Verificar si es un movimiento válido
    if es_movimiento_valido(game_data):
        # Actualizar tablero
        actualizar_tablero(game_data)
    else:
        # Restaurar rotación
        game_data["rotacion"] = rotacion_original


def actualizar_tablero(game_data):
    """Actualiza la visualización del tablero con la pieza actual"""
    # Limpiar solo las celdas que no están fijas
    tablero = game_data["tablero"]
    tablero_fijo = game_data.get("tablero_fijo", [])
    
    # Primero pintar el fondo en todas las celdas
    for i in range(longitud(tablero)):
        for j in range(longitud(tablero[0])):
            # Si la celda no está fijada, pintarla de fondo
            if tablero_fijo is None or i >= longitud(tablero_fijo) or j >= longitud(tablero_fijo[i]) or tablero_fijo[i][j] is None:
                tablero[i][j].config(bg="#1a2a6d")
    
    # Mostrar piezas fijas
    if tablero_fijo:
        for i in range(longitud(tablero_fijo)):
            for j in range(longitud(tablero_fijo[i])):
                if tablero_fijo[i][j] is not None:
                    tablero[i][j].config(bg=tablero_fijo[i][j])
    
    # Mostrar la pieza actual
    pieza = TETRIMINOS[game_data["pieza_actual"]][game_data["rotacion"]]
    color = COLORES_TETRIMINOS[game_data["pieza_actual"]]
    
    for i in range(longitud(pieza)):
        for j in range(longitud(pieza[i])):
            if pieza[i][j] == 1:
                y = game_data["y"] + i
                x = game_data["x"] + j
                
                # Verificar que está dentro de los límites
                if 0 <= y < longitud(tablero) and 0 <= x < longitud(tablero[0]):
                    tablero[y][x].config(bg=color)


def fijar_pieza(game_data):
    """Fija la pieza en su posición actual y genera una nueva"""
    # Obtener información de la pieza actual
    pieza = TETRIMINOS[game_data["pieza_actual"]][game_data["rotacion"]]
    color = COLORES_TETRIMINOS[game_data["pieza_actual"]]
    
    # Si no existe el tablero fijo, crearlo
    if "tablero_fijo" not in game_data:
        # Inicializar tablero_fijo como una matriz del mismo tamaño que tablero, con None
        tablero_fijo = []
        for i in range(longitud(game_data["tablero"])):
            fila = []
            for j in range(longitud(game_data["tablero"][0])):
                fila = agregar(fila, None)
            tablero_fijo = agregar(tablero_fijo, fila)
        game_data["tablero_fijo"] = tablero_fijo
    
    # Fijar la pieza en el tablero_fijo
    for i in range(longitud(pieza)):
        for j in range(longitud(pieza[i])):
            if pieza[i][j] == 1:
                y = game_data["y"] + i
                x = game_data["x"] + j
                
                # Verificar que está dentro de los límites
                if 0 <= y < longitud(game_data["tablero_fijo"]) and 0 <= x < longitud(game_data["tablero_fijo"][0]):
                    game_data["tablero_fijo"][y][x] = color
    
    # Verificar líneas completas
    lineas_completas = verificar_lineas_completas(game_data)
    
    if lineas_completas:
        # Eliminar líneas completas
        for linea in lineas_completas:
            eliminar_linea(game_data, linea)
        
        # Sumar puntos: 100 puntos por cada línea completada
        puntos_nuevos = longitud(lineas_completas) * 100
        game_data["puntos"] += puntos_nuevos
        
        # Actualizar el contador de puntos
        game_data["label_puntos"].config(text=f"PUNTOS: {game_data['puntos']}")
    
    # Generar una nueva pieza
    pieza_actual, pieza_siguiente = game_data["pieza_siguiente"], iniciar_nuevas_piezas()[0]
    game_data["pieza_actual"] = pieza_actual
    game_data["pieza_siguiente"] = pieza_siguiente
    game_data["rotacion"] = 0
    game_data["x"] = 5
    game_data["y"] = 0
    
    # Mostrar la siguiente pieza
    mostrar_siguiente_pieza(game_data["frame_siguiente"], pieza_siguiente)
    
    # Verificar si es game over (si no hay espacio para la nueva pieza)
    if not es_movimiento_valido(game_data):
        game_data["juego_activo"] = False
        messagebox.showinfo("Game Over", f"¡Juego terminado!\nPuntuación final: {game_data['puntos']}")
        
        # Habilitar el botón de jugar en la ventana principal
        game_data["boton_jugar"].config(state=tk.NORMAL)
        
        # Cerrar la ventana de juego después de mostrar el mensaje
        game_data["ventana_juego"].destroy()
        return  # Salir de la función para evitar actualizar el tablero
    
    # Actualizar el tablero
    actualizar_tablero(game_data)


def verificar_lineas_completas(game_data):
    """Verifica si hay líneas horizontales completas y devuelve sus índices"""
    tablero_fijo = game_data["tablero_fijo"]
    lineas_completas = []
    
    # Verificar cada fila
    for i in range(longitud(tablero_fijo)):
        fila_completa = True
        for j in range(longitud(tablero_fijo[i])):
            if tablero_fijo[i][j] is None:
                fila_completa = False
                break
        
        if fila_completa:
            lineas_completas = agregar(lineas_completas, i)
    
    return lineas_completas


def eliminar_linea(game_data, indice_linea):
    """Elimina una línea y mueve todas las líneas superiores hacia abajo"""
    tablero_fijo = game_data["tablero_fijo"]
    
    # Comenzar desde la línea a eliminar y mover hacia arriba
    for i in range(indice_linea, 0, -1):
        for j in range(longitud(tablero_fijo[i])):
            # Copiar el color de la línea de arriba
            tablero_fijo[i][j] = tablero_fijo[i-1][j]
    
    # Limpiar la línea superior
    for j in range(longitud(tablero_fijo[0])):
        tablero_fijo[0][j] = None


def es_movimiento_valido(game_data):
    """Verifica si la posición y rotación actuales son válidas"""
    pieza = TETRIMINOS[game_data["pieza_actual"]][game_data["rotacion"]]
    tablero_fijo = game_data.get("tablero_fijo")  # Puede ser None al inicio
    
    for i in range(longitud(pieza)):
        for j in range(longitud(pieza[i])):
            if pieza[i][j] == 1:
                # Calcular posición en el tablero
                y = game_data["y"] + i
                x = game_data["x"] + j
                
                # Verificar límites del tablero
                if (x < 0 or x >= longitud(game_data["tablero"][0]) or 
                    y < 0 or y >= longitud(game_data["tablero"])):
                    return False
                
                # Verificar colisión con piezas fijas
                if tablero_fijo is not None and y < longitud(tablero_fijo) and x < longitud(tablero_fijo[y]):
                    if tablero_fijo[y][x] is not None:
                        return False
    
    return True


def fijar_pieza(game_data):
    """Fija la pieza en su posición actual y genera una nueva"""
    # Obtener información de la pieza actual
    pieza = TETRIMINOS[game_data["pieza_actual"]][game_data["rotacion"]]
    color = COLORES_TETRIMINOS[game_data["pieza_actual"]]
    
    # Si no existe el tablero fijo, crearlo
    if "tablero_fijo" not in game_data:
        # Inicializar tablero_fijo como una matriz del mismo tamaño que tablero, con None
        tablero_fijo = []
        for i in range(longitud(game_data["tablero"])):
            fila = []
            for j in range(longitud(game_data["tablero"][0])):
                fila = agregar(fila, None)
            tablero_fijo = agregar(tablero_fijo, fila)
        game_data["tablero_fijo"] = tablero_fijo
    
    # Fijar la pieza en el tablero_fijo
    for i in range(longitud(pieza)):
        for j in range(longitud(pieza[i])):
            if pieza[i][j] == 1:
                y = game_data["y"] + i
                x = game_data["x"] + j
                
                # Verificar que está dentro de los límites
                if 0 <= y < longitud(game_data["tablero_fijo"]) and 0 <= x < longitud(game_data["tablero_fijo"][0]):
                    game_data["tablero_fijo"][y][x] = color
    
    # Verificar líneas completas
    lineas_completas = verificar_lineas_completas(game_data)
    
    if lineas_completas:
        # Eliminar líneas completas
        for linea in lineas_completas:
            eliminar_linea(game_data, linea)
        
        # Sumar puntos: 100 puntos por cada línea completada
        puntos_nuevos = longitud(lineas_completas) * 100
        game_data["puntos"] += puntos_nuevos
        
        # Actualizar el contador de puntos
        game_data["label_puntos"].config(text=f"PUNTOS: {game_data['puntos']}")
    
    # Generar una nueva pieza
    pieza_actual, pieza_siguiente = game_data["pieza_siguiente"], iniciar_nuevas_piezas()[0]
    game_data["pieza_actual"] = pieza_actual
    game_data["pieza_siguiente"] = pieza_siguiente
    game_data["rotacion"] = 0
    game_data["x"] = 5
    game_data["y"] = 0
    
    # Mostrar la siguiente pieza
    mostrar_siguiente_pieza(game_data["frame_siguiente"], pieza_siguiente)
    
    # Verificar si es game over (si no hay espacio para la nueva pieza)
    if not es_movimiento_valido(game_data):
        game_data["juego_activo"] = False
        messagebox.showinfo("Game Over", f"¡Juego terminado!\nPuntuación final: {game_data['puntos']}")
        
        # Habilitar el botón de jugar en la ventana principal
        game_data["boton_jugar"].config(state=tk.NORMAL)
        
        # Cerrar la ventana de juego después de mostrar el mensaje
        game_data["ventana_juego"].destroy()
        return  # Salir de la función para evitar actualizar el tablero
    
    # Actualizar el tablero
    actualizar_tablero(game_data)


def mostrar_menu_pausa(ventana_juego):
    """Muestra un menú de pausa con opciones para continuar, guardar o salir"""
    # Crear ventana modal para el menú de pausa
    menu_pausa = tk.Toplevel(ventana_juego)
    menu_pausa.title("PAUSA")
    menu_pausa.geometry("300x350")
    menu_pausa.resizable(False, False)
    menu_pausa.config(bg="#1a1a2e")
    menu_pausa.transient(ventana_juego)  # Hace que sea una ventana hija
    menu_pausa.grab_set()  # Modal - bloquea interacción con ventana padre
    
    # Centrar en la pantalla
    posicionar_ventana(menu_pausa, 300, 350)
    
    # Título del menú
    label_pausa = tk.Label(
        menu_pausa,
        text="PAUSA",
        bg="#1a1a2e",
        fg="white",
        font=("Press Start 2P", 18, "bold")
    )
    label_pausa.pack(pady=20)
    
    # Botón continuar
    boton_continuar = tk.Button(
        menu_pausa,
        text="CONTINUAR",
        bg="#4ecca3", fg="#1a1a2e",
        font=FUENTE_RETRO,
        width=12, height=2,
        command=menu_pausa.destroy,  # Simplemente cierra el menú para continuar
        relief=tk.GROOVE
    )
    boton_continuar.pack(pady=15)
    boton_continuar.bind("<Enter>", lambda e: boton_continuar.config(bg="#6be0bc"))
    boton_continuar.bind("<Leave>", lambda e: boton_continuar.config(bg="#4ecca3"))
    
    # Botón guardar partida
    boton_guardar = tk.Button(
        menu_pausa,
        text="GUARDAR",
        bg="#ffd369", fg="#1a1a2e",
        font=FUENTE_RETRO,
        width=12, height=2,
        command=lambda: guardar_partida(menu_pausa),
        relief=tk.GROOVE
    )
    boton_guardar.pack(pady=15)
    boton_guardar.bind("<Enter>", lambda e: boton_guardar.config(bg="#ffe085"))
    boton_guardar.bind("<Leave>", lambda e: boton_guardar.config(bg="#ffd369"))
    
    # Botón salir
    boton_salir = tk.Button(
        menu_pausa,
        text="SALIR",
        bg="#e84545", fg="white",
        font=FUENTE_RETRO,
        width=12, height=2,
        command=lambda: salir_partida(ventana_juego, menu_pausa),
        relief=tk.GROOVE
    )
    boton_salir.pack(pady=15)
    boton_salir.bind("<Enter>", lambda e: boton_salir.config(bg="#ff6b6b"))
    boton_salir.bind("<Leave>", lambda e: boton_salir.config(bg="#e84545"))


def posicionar_ventana(ventana, ancho, alto):
    """Centra una ventana en la pantalla"""
    # Obtener dimensiones de la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    
    # Calcular posición x,y para la ventana
    x = (ancho_pantalla / 2) - (ancho / 2)
    y = (alto_pantalla / 2) - (alto / 2)
    
    # Establecer geometría
    ventana.geometry(f"{ancho}x{alto}+{int(x)}+{int(y)}")


def guardar_partida(ventana_menu):
        puntos_nuevos = longitud(lineas_completas) * 100
        game_data["puntos"] += puntos_nuevosrdar
        agebox.showinfo("Guardar", "¡Partida guardada correctamente!")
        # Actualizar el contador de puntos
        game_data["label_puntos"].config(text=f"PUNTOS: {game_data['puntos']}")
    
    # Generar una nueva piezago, ventana_menu):
    pieza_actual, pieza_siguiente = game_data["pieza_siguiente"], iniciar_nuevas_piezas()[0]
    game_data["pieza_actual"] = pieza_actualr", "¿Estás seguro que deseas salir?\nPerderás el progreso no guardado.")
    game_data["pieza_siguiente"] = pieza_siguiente
    game_data["rotacion"] = 0)
    game_data["x"] = 5destroy()
    game_data["y"] = 0uardado_Nuevo():
    with open("Código/guardado.txt", "x") as archivo:
    # Mostrar la siguiente piezainicial\n")
    mostrar_siguiente_pieza(game_data["frame_siguiente"], pieza_siguiente)
    
    # Verificar si es game over (si no hay espacio para la nueva pieza)
    if not es_movimiento_valido(game_data):        game_data["juego_activo"] = False        messagebox.showinfo("Game Over", f"¡Juego terminado!\nPuntuación final: {game_data['puntos']}")        # Actualizar el tablero    actualizar_tablero(game_data)def mostrar_menu_pausa(ventana_juego):    """Muestra un menú de pausa con opciones para continuar, guardar o salir"""    # Crear ventana modal para el menú de pausa    menu_pausa = tk.Toplevel(ventana_juego)    menu_pausa.title("PAUSA")    menu_pausa.geometry("300x350")    menu_pausa.resizable(False, False)    menu_pausa.config(bg="#1a1a2e")    menu_pausa.transient(ventana_juego)  # Hace que sea una ventana hija    menu_pausa.grab_set()  # Modal - bloquea interacción con ventana padre        # Centrar en la pantalla    posicionar_ventana(menu_pausa, 300, 350)        # Título del menú    label_pausa = tk.Label(        menu_pausa,        text="PAUSA",        bg="#1a1a2e",        fg="white",        font=("Press Start 2P", 18, "bold")    )    label_pausa.pack(pady=20)        # Botón continuar    boton_continuar = tk.Button(        menu_pausa,        text="CONTINUAR",        bg="#4ecca3", fg="#1a1a2e",        font=FUENTE_RETRO,        width=12, height=2,        command=menu_pausa.destroy,  # Simplemente cierra el menú para continuar        relief=tk.GROOVE    )    boton_continuar.pack(pady=15)    boton_continuar.bind("<Enter>", lambda e: boton_continuar.config(bg="#6be0bc"))    boton_continuar.bind("<Leave>", lambda e: boton_continuar.config(bg="#4ecca3"))        # Botón guardar partida    boton_guardar = tk.Button(        menu_pausa,        text="GUARDAR",        bg="#ffd369", fg="#1a2e",        font=FUENTE_RETRO,        width=12, height=2,        command=lambda: guardar_partida(menu_pausa),        relief=tk.GROOVE    )    boton_guardar.pack(pady=15)    boton_guardar.bind("<Enter>", lambda e: boton_guardar.config(bg="#ffe085"))    boton_guardar.bind("<Leave>", lambda e: boton_guardar.config(bg="#ffd369"))        # Botón salir    boton_salir = tk.Button(        menu_pausa,        text="SALIR",        bg="#e84545", fg="white",        font=FUENTE_RETRO,        width=12, height=2,        command=lambda: salir_partida(ventana_juego, menu_pausa),        relief=tk.GROOVE    )    boton_salir.pack(pady=15)    boton_salir.bind("<Enter>", lambda e: boton_salir.config(bg="#ff6b6b"))    boton_salir.bind("<Leave>", lambda e: boton_salir.config(bg="#e84545"))def posicionar_ventana(ventana, ancho, alto):    """Centra una ventana en la pantalla"""    # Obtener dimensiones de la pantalla    ancho_pantalla = ventana.winfo_screenwidth()    alto_pantalla = ventana.winfo_screenheight()        # Calcular posición x,y para la ventana    x = (ancho_pantalla / 2) - (ancho / 2)    y = (alto_pantalla / 2) - (alto / 2)        # Establecer geometría    ventana.geometry(f"{ancho}x{alto}+{int(x)}+{int(y)}")def guardar_partida(ventana_menu):    """Guarda el estado actual de la partida"""    # Aquí implementarías la lógica para guardar    messagebox.showinfo("Guardar", "¡Partida guardada correctamente!")    ventana_menu.destroy()def salir_partida(ventana_juego, ventana_menu):    """Cierra la partida actual y vuelve al menú principal"""    confirmacion = messagebox.askyesno("Salir", "¿Estás seguro que deseas salir?\nPerderás el progreso no guardado.")    if confirmacion:        ventana_menu.destroy()        ventana_juego.destroy()def crear_Archivo_de_Guardado_Nuevo():    with open("Código/guardado.txt", "x") as archivo:        archivo.write("Guardado inicial\n")if __name__ == "__main__":    iniciar_juego()