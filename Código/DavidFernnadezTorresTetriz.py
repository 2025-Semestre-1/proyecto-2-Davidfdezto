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
    """Función para reemplazar append"""
    return lista + [elemento]  # Crear una nueva lista con el elemento añadido

def iniciar_juego():
    ventana = tk.Tk()
    ventana.title("Tetris") 
    ventana.geometry("400x600")
    ventana.resizable(False, False)
    ventana.config(bg="#1a1a2e")  # Azul marino oscuro
    
    # Cargar y mostrar el logo de Tetris
    img = Image.open("logo.png")
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
        bg="#4ecca3", fg="#1a2e2e",
        font=FUENTE_RETRO,
        width=10, height=2,
        command=lambda: jugar(ventana, boton_jugar),
        relief=tk.GROOVE
    )
    boton_jugar.pack(pady=20)
    boton_jugar.bind("<Enter>", lambda e: boton_jugar.config(bg="#6be0bc"))
    boton_jugar.bind("<Leave>", lambda e: boton_jugar.config(bg="#4ecca3"))
    
    # Botón para cargar partida
    boton_cargar = tk.Button(
        ventana,
        text="CARGAR",
        bg="#9b59b6", fg="white",
        font=FUENTE_RETRO,
        width=10, height=2,
        command=lambda: mostrar_partidas_guardadas(ventana, boton_jugar),
        relief=tk.GROOVE
    )
    boton_cargar.pack(pady=20)
    boton_cargar.bind("<Enter>", lambda e: boton_cargar.config(bg="#a569c7"))
    boton_cargar.bind("<Leave>", lambda e: boton_cargar.config(bg="#9b59b6"))
    
    # Botón para salir
    boton_salir = tk.Button(
        ventana,
        text="SALIR",
        bg="#e84545", fg="white",
        font=FUENTE_RETRO,
        width=10, height=2,
        command=ventana.destroy,
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

    # Centrar la ventana
    posicionar_ventana(ventana_estadisticas, 600, 700)

    # Título
    label_estadisticas = tk.Label(
        ventana_estadisticas,
        text="ESTADÍSTICAS DEL JUEGO",
        bg="#1a1a2e", fg="white",
        font=FUENTE_RETRO   
    )
    label_estadisticas.pack(pady=20)
    
    # Frame para el texto con scrollbar
    frame_texto = tk.Frame(ventana_estadisticas, bg="#1a1a2e")
    frame_texto.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
    
    # Scrollbar para el texto
    scrollbar_texto = tk.Scrollbar(frame_texto)
    scrollbar_texto.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Texto de estadísticas
    texto_estadisticas = tk.Text(
        frame_texto,
        bg="#1a1a2e", fg="white",
        font=("Press Start 2P", 10),
        width=50, height=25, 
        wrap=tk.WORD,
        yscrollcommand=scrollbar_texto.set
    )
    texto_estadisticas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar_texto.config(command=texto_estadisticas.yview)
    
    # Cargar y mostrar estadísticas
    try:
        archivo_indice = "indiceJuego.txt"
        
        if not os.path.exists(archivo_indice):
            texto_estadisticas.insert(tk.END, "No hay partidas registradas aún.\n\n")
            texto_estadisticas.insert(tk.END, "¡Juega algunas partidas para ver tus estadísticas!")
        else:
            # Leer el archivo de índice
            with open(archivo_indice, "r") as archivo:
                lineas = archivo.readlines()
            
            if not lineas:
                texto_estadisticas.insert(tk.END, "No hay partidas registradas aún.\n\n")
                texto_estadisticas.insert(tk.END, "¡Juega algunas partidas para ver tus estadísticas!")
            else:
                texto_estadisticas.insert(tk.END, "HISTORIAL DE PARTIDAS\n")
                texto_estadisticas.insert(tk.END, "(En orden cronológico)\n")
                texto_estadisticas.insert(tk.END, "="*50 + "\n\n")
                
                contador = 1
                
                # Procesar cada línea del índice
                for linea in lineas:
                    linea = linea.strip()
                    if linea:  # Ignorar líneas vacías
                        try:
                            # Formato: nombre_jugador|nombre_archivo|puntos|fecha
                            partes = linea.split("|")
                            if longitud(partes) >= 4:
                                nombre_jugador = partes[0]
                                puntos = partes[2]
                                fecha = partes[3]
                                
                                # Agregar al texto
                                texto_estadisticas.insert(tk.END, f"{contador}. {nombre_jugador}\n")
                                texto_estadisticas.insert(tk.END, f"   Puntos: {puntos}\n")
                                texto_estadisticas.insert(tk.END, f"   Fecha: {fecha}\n")
                                texto_estadisticas.insert(tk.END, "-" * 30 + "\n\n")
                                
                                contador += 1
                        except Exception as e:
                            print(f"Error al procesar línea: {linea}, Error: {e}")
                            continue
                
                # Agregar resumen al final
                texto_estadisticas.insert(tk.END, "\n" + "="*50 + "\n")
                texto_estadisticas.insert(tk.END, f"TOTAL DE PARTIDAS: {contador - 1}\n")
                
                # Calcular puntuación más alta
                puntuacion_maxima = 0
                jugador_mejor = ""
                
                # Volver a leer para encontrar la mejor puntuación
                for linea in lineas:
                    linea = linea.strip()
                    if linea:
                        try:
                            partes = linea.split("|")
                            if longitud(partes) >= 4:
                                puntos_actual = int(partes[2])
                                if puntos_actual > puntuacion_maxima:
                                    puntuacion_maxima = puntos_actual
                                    jugador_mejor = partes[0]
                        except:
                            continue
                
                if jugador_mejor:
                    texto_estadisticas.insert(tk.END, f"MEJOR PUNTUACIÓN: {puntuacion_maxima} pts\n")
                    texto_estadisticas.insert(tk.END, f"CONSEGUIDA POR: {jugador_mejor}\n")
    
    except Exception as e:
        texto_estadisticas.insert(tk.END, f"Error al cargar estadísticas: {str(e)}")
    
    # Deshabilitar edición del texto
    texto_estadisticas.config(state=tk.DISABLED)
    
    # Botón para cerrar la ventana de estadísticas
    boton_cerrar = tk.Button(
        ventana_estadisticas,
        text="CERRAR",
        bg="#e84545", fg="white",
        font=FUENTE_RETRO,
        width=12, height=2,
        command=ventana_estadisticas.destroy,
        relief=tk.GROOVE
    )
    boton_cerrar.pack(pady=20)
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
    """Lee la matriz desde un archivo de texto y detecta obstáculos como '+'"""
    try:
        # Intentar abrir el archivo (probando diferentes nombres)
        archivo_encontrado = False
        matriz = []
        hay_obstaculos = False
        
        for nombre_archivo in ["matriz.txt", "Matriz.txt", "matriz", "Matriz"]:
            try:
                ruta_completa = f"Código/{nombre_archivo}"
                print(f"Intentando abrir: {ruta_completa}")
                with open(ruta_completa, "r") as archivo:
                    lineas = archivo.readlines()
                    archivo_encontrado = True
                    print(f"Archivo encontrado: {ruta_completa}")
                    break
            except FileNotFoundError:
                continue
        
        if not archivo_encontrado:
            print("No se encontró el archivo de matriz, creando matriz por defecto")
            # Crear matriz por defecto 20x10 sin obstáculos internos
            for i in range(20):
                fila = []
                for j in range(10):
                    fila = agregar(fila, ".")  # Solo espacios libres
                matriz = agregar(matriz, fila)
            return matriz
            
        # Procesar cada línea del archivo
        for linea in lineas:
            linea = linea.strip()  # Quitar espacios y saltos de línea
            if not linea:  # Ignorar líneas vacías
                continue
                
            # Si la línea contiene comas, separar por comas
            if "," in linea:
                elementos = linea.split(",")
            else:
                # Si no hay comas, tratar cada carácter como un elemento
                elementos = list(linea)
            
            fila = []
            for elemento in elementos:
                elemento_limpio = elemento.strip()
                
                # Detectar obstáculos (el carácter "+")
                if elemento_limpio == "+":
                    hay_obstaculos = True
                    print(f"Obstáculo detectado: '{elemento_limpio}'")
                    
                fila = agregar(fila, elemento_limpio)
            
            if fila:  # Solo agregar filas no vacías
                matriz = agregar(matriz, fila)

        print(f"Matriz cargada, dimensiones: {longitud(matriz)}x{longitud(matriz[0]) if matriz else 0}")
        print(f"¿Hay obstáculos detectados? {hay_obstaculos}")
        
        return matriz
        
    except Exception as e:
        print(f"Error al leer la matriz desde archivo: {e}")
        # Retornar matriz por defecto en caso de error
        matriz = []
        for i in range(20):
            fila = []
            for j in range(10):
                fila = agregar(fila, ".")  # Solo espacios libres
            matriz = agregar(matriz, fila)
        return matriz

def inicializar_tablero_fijo_con_matriz():
    """Inicializa el tablero fijo con los obstáculos de la matriz del archivo"""
    matriz_archivo = interpretar_matriz()
    
    if matriz_archivo and longitud(matriz_archivo) > 0:
        FILAS = longitud(matriz_archivo)
        COLUMNAS = longitud(matriz_archivo[0]) if longitud(matriz_archivo) > 0 else 10
        print(f"Inicializando tablero fijo con dimensiones: {FILAS}x{COLUMNAS}")
    else:
        FILAS, COLUMNAS = 20, 10
        matriz_archivo = None
        print("Usando dimensiones por defecto para tablero fijo: 20x10")
    
    # Crear tablero fijo
    tablero_fijo = []
    for i in range(FILAS):
        fila = []
        for j in range(COLUMNAS):
            # Verificar si hay obstáculo en esta posición según el archivo
            if matriz_archivo and i < longitud(matriz_archivo) and j < longitud(matriz_archivo[i]):
                celda_archivo = str(matriz_archivo[i][j]).strip()
                
                # Si es un obstáculo (+), marcarlo como fijo
                if celda_archivo == "+":
                    fila = agregar(fila, "#ff6b6b")  # Color rojo para obstáculos inamovibles
                    print(f"Obstáculo fijo colocado en posición [{i},{j}]")
                else:
                    fila = agregar(fila, None)  # Espacio libre
            else:
                fila = agregar(fila, None)  # Espacio libre por defecto
        tablero_fijo = agregar(tablero_fijo, fila)
    
    return tablero_fijo

def inicializar_tablero(frame_matriz):
    """Crea el tablero de juego como una matriz 2D de labels usando la matriz del archivo"""
    # Cargar la matriz desde archivo
    matriz_archivo = interpretar_matriz()
    
    if matriz_archivo and longitud(matriz_archivo) > 0:
        # Usar dimensiones de la matriz del archivo
        FILAS = longitud(matriz_archivo)
        COLUMNAS = longitud(matriz_archivo[0]) if longitud(matriz_archivo) > 0 else 10
        print(f"Usando matriz del archivo: {FILAS}x{COLUMNAS}")
    else:
        # Fallback a dimensiones estándar si no se puede cargar
        FILAS, COLUMNAS = 20, 10
        matriz_archivo = None
        print("Usando dimensiones estándar: 20x10")
    
    # Crear matriz vacía para los labels
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
            # Determinar color inicial basado en la matriz del archivo
            if matriz_archivo and i < longitud(matriz_archivo) and j < longitud(matriz_archivo[i]):
                celda_archivo = str(matriz_archivo[i][j]).strip()
                # Si es un obstáculo (+), usar color especial
                if celda_archivo == "+":
                    color_inicial = "#ff6b6b"  # Rojo para obstáculos
                    print(f"Obstáculo visual colocado en posición [{i},{j}]")
                else:
                    color_inicial = "#1a2a6d"  # Color normal
            else:
                color_inicial = "#1a2a6d"  # Color de fondo inicial
            
            # Crear label como celda
            celda = tk.Label(
                frame_matriz,
                bg=color_inicial,
                borderwidth=1,
                relief=tk.RAISED  # Da efecto 3D a las celdas
            )
            celda.grid(row=i, column=j, sticky="nsew", padx=0, pady=0)
            fila = agregar(fila, celda)  
        tablero = agregar(tablero, fila)  

    return tablero

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
    ],
    'U': [
        [[1, 0, 1],
         [1, 1, 1],
         [0, 0, 0]],
        [[0, 1, 1],
         [0, 1, 0],
         [0, 1, 1]],
        [[0, 0, 0],
         [1, 1, 1],
         [1, 0, 1]],
        [[1, 1, 0],
         [0, 1, 0],
         [1, 1, 0]]
    ],
    '+': [
        [[0, 1, 0],
         [1, 1, 1],
         [0, 1, 0]],
        [[0, 1, 0],
         [1, 1, 1],
         [0, 1, 0]],
        [[0, 1, 0],
         [1, 1, 1],
         [0, 1, 0]],
        [[0, 1, 0],
         [1, 1, 1],
         [0, 1, 0]]
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
    'Z': "#f00000",  # Rojo
    'U': "#ff00ff",  # Magenta
    '+': "#ff8800"   # Naranja brillante
}

def jugar(ventana, boton_jugar):
    # Pedir nombre del jugador antes de comenzar
    nombre_jugador = pedir_nombre_jugador()
    if not nombre_jugador:
        # Si el usuario cancela, no iniciamos el juego
        return
        
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
    
    # Etiqueta para nombre del jugador
    label_jugador = tk.Label(
        frame_info,
        text=f"JUGADOR: {nombre_jugador}",
        bg="#1a2a2e",
        fg="white",
        font=FUENTE_RETRO
    )
    label_jugador.pack(pady=10)
    
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
    
    # Botón de pausa
    boton_pausa = tk.Button(
        frame_info,
        text="PAUSA",
        bg="#ffd369", fg="#1a2e2e",
        font=FUENTE_RETRO,
        width=10, height=2,
        command=lambda: mostrar_menu_pausa(ventana_juego, game_data),
        relief=tk.GROOVE
    )
    boton_pausa.pack(pady=20)
    boton_pausa.bind("<Enter>", lambda e: boton_pausa.config(bg="#ffe085"))
    boton_pausa.bind("<Leave>", lambda e: boton_pausa.config(bg="#ffd369"))
    
    # Inicializar el tablero visual CON LA MATRIZ DEL ARCHIVO
    tablero = inicializar_tablero(frame_matriz)
    
    # Inicializar tablero fijo con obstáculos de la matriz del archivo
    tablero_fijo = inicializar_tablero_fijo_con_matriz()
    
    # Iniciar la pieza actual y su posición
    pieza_actual = random.choice(list(TETRIMINOS.keys()))
    pieza_siguiente = random.choice(list(TETRIMINOS.keys()))
    
    # Mostrar la siguiente pieza en el panel
    mostrar_siguiente_pieza(frame_siguiente, pieza_siguiente)
    
    # Variables de control del juego
    game_data = {
        "tablero": tablero,
        "tablero_fijo": tablero_fijo,  # Usar el tablero fijo inicializado con obstáculos del archivo
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
        "boton_jugar": boton_jugar,  # Guardar referencia al botón
        "nombre_jugador": nombre_jugador  # Guardar nombre del jugador
    }
    
    # Actualizar visualización inicial
    actualizar_tablero(game_data)
    
    # Configurar eventos de teclado
    ventana_juego.bind("<Left>", lambda event: mover_pieza(game_data, -1, 0))
    ventana_juego.bind("<Right>", lambda event: mover_pieza(game_data, 1, 0))
    ventana_juego.bind("<Down>", lambda event: mover_pieza(game_data, 0, 1))
    ventana_juego.bind("<space>", lambda event: rotar_pieza(game_data))
    ventana_juego.bind("<p>", lambda event: mostrar_menu_pausa(ventana_juego, game_data))  # Tecla P para pausa
    ventana_juego.focus_set()  # Dar foco a la ventana para capturar eventos de teclado
    
    # Iniciar bucle de caída automática
    ventana_juego.after(1000, lambda: caida_automatica(ventana_juego, game_data))


def posicionar_ventana(ventana, ancho, alto):
    """Centra una ventana de Tkinter en la pantalla."""
    ventana.update_idletasks()
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    x = (ancho_pantalla // 2) - (ancho // 2)
    y = (alto_pantalla // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def pedir_nombre_jugador():
    """Muestra una ventana para solicitar el nombre del jugador"""
    # Crear una ventana simple
    ventana_nombre = tk.Toplevel()
    ventana_nombre.title("Nombre de Jugador")
    ventana_nombre.geometry("400x200")
    ventana_nombre.config(bg="#1a2a2e")
    ventana_nombre.resizable(False, False)
    ventana_nombre.transient()  # Ventana modal
    
    # Centrar la ventana
    posicionar_ventana(ventana_nombre, 400, 200)
    
    # Etiqueta para instrucciones
    label = tk.Label(
        ventana_nombre,
        text="Ingresa tu nombre:",
        bg="#1a2a2e", fg="white",
        font=FUENTE_RETRO
    )
    label.pack(pady=20)
    
    # Campo para texto
    entrada = tk.Entry(
        ventana_nombre,
        font=FUENTE_RETRO,
        width=20
    )
    entrada.pack(pady=10)
    entrada.focus_set()  # Dar foco a la entrada
    
    # Variable para almacenar el nombre
    nombre = [None]  # Usamos una lista para poder modificarla desde funciones anidadas
    
    # Función para confirmar el nombre
    def confirmar():
        if entrada.get().strip():  # Verificar que no esté vacío
            nombre[0] = entrada.get().strip()
            ventana_nombre.destroy()
    
    # Botón para confirmar
    boton = tk.Button(
        ventana_nombre,
        text="COMENZAR",
        bg="#4ecca3", fg="#1a2e2e",
        font=FUENTE_RETRO,
        command=confirmar,
        relief=tk.GROOVE
    )
    boton.pack(pady=20)
    
    # Evento Enter para confirmar
    entrada.bind("<Return>", lambda event: confirmar())
    
    # Esperar hasta que se cierre la ventana
    ventana_nombre.wait_window()
    
    return nombre[0]


def mostrar_menu_pausa(ventana_juego, game_data):
    """Muestra un menú de pausa con opciones para continuar, guardar o salir"""
    # Pausar el juego
    game_data["juego_pausado"] = True
    
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
        bg="#1a2a2e",
        fg="white",
        font=("Press Start 2P", 18, "bold")
    )
    label_pausa.pack(pady=20)
    
    # Botón continuar
    boton_continuar = tk.Button(
        menu_pausa,
        text="CONTINUAR",
        bg="#4ecca3", fg="#1a2e2e",
        font=FUENTE_RETRO,
        width=12, height=2,
        command=lambda: continuar_juego(menu_pausa, game_data),
        relief=tk.GROOVE
    )
    boton_continuar.pack(pady=15)
    boton_continuar.bind("<Enter>", lambda e: boton_continuar.config(bg="#6be0bc"))
    boton_continuar.bind("<Leave>", lambda e: boton_continuar.config(bg="#4ecca3"))
    
    # Botón guardar partida
    boton_guardar = tk.Button(
        menu_pausa,
        text="GUARDAR",
        bg="#ffd369", fg="#1a2e2e",
        font=FUENTE_RETRO,
        width=12, height=2,
        command=lambda: guardar_partida(game_data, menu_pausa),
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
        command=lambda: salir_partida(game_data, menu_pausa),
        relief=tk.GROOVE
    )
    boton_salir.pack(pady=15)
    boton_salir.bind("<Enter>", lambda e: boton_salir.config(bg="#ff6b6b"))
    boton_salir.bind("<Leave>", lambda e: boton_salir.config(bg="#e84545"))


def continuar_juego(ventana_menu, game_data):
    """Continúa el juego después de la pausa"""
    game_data["juego_pausado"] = False
    ventana_menu.destroy()
    # Reactivar la caída automática
    game_data["ventana_juego"].after(1000, lambda: caida_automatica(game_data["ventana_juego"], game_data))


def guardar_partida(game_data, ventana_menu=None):
    """Guarda el estado actual de la partida en un archivo con el nombre del jugador"""
    try:
        # Crear directorio si no existe
        directorio_guardados = "partidas_guardadas"
        if not os.path.exists(directorio_guardados):
            os.makedirs(directorio_guardados)
        
        # Generar nombre de archivo con nombre del jugador y timestamp
        import time
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        nombre_jugador_seguro = ''.join(c if c.isalnum() else '_' for c in game_data["nombre_jugador"])
        nombre_archivo = f"{nombre_jugador_seguro}_{timestamp}.txt"
        ruta_archivo = f"{directorio_guardados}/{nombre_archivo}"
        
        # Crear archivo y guardar datos de la partida
        with open(ruta_archivo, "w") as archivo:
            archivo.write(f"Jugador: {game_data['nombre_jugador']}\n")
            archivo.write(f"Puntos: {game_data['puntos']}\n")
            archivo.write(f"Fecha: {time.strftime('%d/%m/%Y %H:%M:%S')}\n")
            archivo.write("Estado del tablero:\n")
            
            # Guardar el estado del tablero fijo
            if "tablero_fijo" in game_data:
                for i in range(longitud(game_data["tablero_fijo"])):
                    linea = ""
                    for j in range(longitud(game_data["tablero_fijo"][0])):
                        celda = game_data["tablero_fijo"][i][j]
                        linea += "X" if celda is not None else "."
                    archivo.write(linea + "\n")
            
            # Guardar info de la pieza actual
            archivo.write(f"Pieza actual: {game_data['pieza_actual']}\n")
            archivo.write(f"Rotación: {game_data['rotacion']}\n")
            archivo.write(f"Posición X: {game_data['x']}\n")
            archivo.write(f"Posición Y: {game_data['y']}\n")
            archivo.write(f"Siguiente pieza: {game_data['pieza_siguiente']}\n")
        
        # Registrar partida en el índice
        registrar_partida_en_indice(
            game_data["nombre_jugador"],
            nombre_archivo,
            game_data["puntos"]
        )
        
        messagebox.showinfo("Guardar", "¡Partida guardada correctamente!")
        
        # Cerrar ventana de menú si existe
        if ventana_menu:
            ventana_menu.destroy()
            
        return True
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar la partida: {str(e)}")
        return False


def registrar_partida_en_indice(nombre_jugador, nombre_archivo, puntos):
    """Registra la partida guardada en el archivo índice"""
    try:
        # Crear el archivo de índice si no existe
        archivo_indice = "indiceJuego.txt"
        with open(archivo_indice, "a") as indice:
            # Agregar entrada al índice
            import time
            fecha = time.strftime("%d/%m/%Y %H:%M:%S")
            indice.write(f"{nombre_jugador}|{nombre_archivo}|{puntos}|{fecha}\n")
            
    except Exception as e:
        print(f"Error al registrar partida en índice: {str(e)}")


def salir_partida(game_data, ventana_menu):
    """Cierra la partida actual y vuelve al menú principal"""
    confirmacion = messagebox.askyesno("Salir", "¿Estás seguro que deseas salir?\nPerderás el progreso no guardado.")
    if confirmacion:
        # Preguntar si desea guardar antes de salir
        guardar = messagebox.askyesno("Guardar y Salir", "¿Deseas guardar la partida antes de salir?")
        if guardar:
            guardado = guardar_partida(game_data)
            if not guardado:
                # Si hubo error al guardar, preguntar si aún quiere salir
                continuar = messagebox.askyesno("Error", "Hubo un error al guardar. ¿Deseas salir de todas formas?")
                if not continuar:
                    return
        
        ventana_menu.destroy()
        game_data["ventana_juego"].destroy()
        game_data["boton_jugar"].config(state=tk.NORMAL)


def mover_pieza(game_data, dx, dy):
    """Mueve la pieza actual en el tablero si es posible"""
    # Verificar si el juego está pausado
    if game_data.get("juego_pausado", False):
        return
    
    # Obtener datos actuales
    x = game_data["x"]
    y = game_data["y"]
    rotacion = game_data["rotacion"]
    pieza = TETRIMINOS[game_data["pieza_actual"]][rotacion]
    tablero_fijo = game_data["tablero_fijo"]

    # Calcular nueva posición
    nuevo_x = x + dx
    nuevo_y = y + dy

    # Comprobar colisiones
    if not hay_colision(tablero_fijo, pieza, nuevo_x, nuevo_y):
        game_data["x"] = nuevo_x
        game_data["y"] = nuevo_y
        actualizar_tablero(game_data)
        # Imprimir tablero después de cada movimiento
        imprimir_tablero_en_consola(game_data)
    else:
        # Si la colisión es hacia abajo, fijar la pieza
        if dy == 1:
            fijar_pieza(game_data)
            limpiar_lineas(game_data)
            # Generar nueva pieza
            nueva_pieza(game_data)
            actualizar_tablero(game_data)
            # Imprimir tablero después de fijar pieza
            imprimir_tablero_en_consola(game_data)

def hay_colision(tablero_fijo, pieza, x, y):
    """Verifica si la pieza colisiona con el tablero fijo o los bordes"""
    if not tablero_fijo or not pieza:
        return False
        
    filas = longitud(tablero_fijo)
    columnas = longitud(tablero_fijo[0]) if filas > 0 else 0
    
    for i in range(longitud(pieza)):
        for j in range(longitud(pieza[i])):
            if pieza[i][j] == 1:  # Solo verificar celdas ocupadas de la pieza
                pos_y = y + i
                pos_x = x + j
                
                # Verificar bordes del tablero
                if pos_x < 0 or pos_x >= columnas or pos_y >= filas:
                    return True
                
                # Permitir que la pieza aparezca en la parte superior (pos_y < 0)
                if pos_y >= 0:
                    # Verificar colisión con piezas fijas
                    if tablero_fijo[pos_y][pos_x] is not None:
                        return True
    
    return False

def fijar_pieza(game_data):
    """Fija la pieza actual en el tablero fijo"""
    x = game_data["x"]
    y = game_data["y"]
    rotacion = game_data["rotacion"]
    pieza = TETRIMINOS[game_data["pieza_actual"]][rotacion]
    color = COLORES_TETRIMINOS[game_data["pieza_actual"]]
    tablero_fijo = game_data["tablero_fijo"]
    
    if not tablero_fijo:
        return
    
    filas = longitud(tablero_fijo)
    columnas = longitud(tablero_fijo[0]) if filas > 0 else 0
    
    # Fijar cada celda de la pieza en el tablero fijo
    for i in range(longitud(pieza)):
        for j in range(longitud(pieza[i])):
            if pieza[i][j] == 1:  # Solo fijar celdas ocupadas
                pos_y = y + i
                pos_x = x + j
                # Solo fijar si está dentro de los límites del tablero
                if 0 <= pos_y < filas and 0 <= pos_x < columnas:
                    tablero_fijo[pos_y][pos_x] = color

def limpiar_lineas(game_data):
    """Elimina líneas completas y actualiza la puntuación"""
    tablero_fijo = game_data["tablero_fijo"]
    
    if not tablero_fijo:
        return
    
    filas = longitud(tablero_fijo)
    columnas = longitud(tablero_fijo[0]) if filas > 0 else 0
    
    nuevas_filas = []
    lineas_eliminadas = 0
    
    # Verificar cada fila
    for i in range(filas):
        fila = tablero_fijo[i]
        # Una línea está completa si todas las celdas tienen contenido (no None)
        linea_completa = True
        for celda in fila:
            if celda is None:
                linea_completa = False
                break
        
        if linea_completa:
            lineas_eliminadas += 1
            print(f"¡Línea {i} eliminada!")
        else:
            nuevas_filas = agregar(nuevas_filas, fila)
    
    # Agregar filas vacías al principio por cada línea eliminada
    for _ in range(lineas_eliminadas):
        fila_vacia = []
        for _ in range(columnas):
            fila_vacia = agregar(fila_vacia, None)
        nuevas_filas.insert(0, fila_vacia)
    
    # Actualizar el tablero fijo
    game_data["tablero_fijo"] = nuevas_filas
    
    # Actualizar puntuación
    if lineas_eliminadas > 0:
        puntos_ganados = lineas_eliminadas * 100
        game_data["puntos"] += puntos_ganados
        game_data["label_puntos"].config(text=f"PUNTOS: {game_data['puntos']}")
        print(f"¡{lineas_eliminadas} línea(s) eliminada(s)! +{puntos_ganados} puntos")

def nueva_pieza(game_data):
    """Genera una nueva pieza y verifica si hay espacio para colocarla"""
    # Cambiar pieza actual por la siguiente
    game_data["pieza_actual"] = game_data["pieza_siguiente"]
    game_data["pieza_siguiente"] = random.choice(list(TETRIMINOS.keys()))
    game_data["rotacion"] = 0
    
    # Posición inicial (centro superior)
    tablero_fijo = game_data["tablero_fijo"]
    if tablero_fijo:
        columnas = longitud(tablero_fijo[0])
        game_data["x"] = columnas // 2 - 1  # Centrar horizontalmente
    else:
        game_data["x"] = 4  # Posición por defecto
    
    game_data["y"] = 0
    
    # Actualizar visualización de siguiente pieza
    mostrar_siguiente_pieza(game_data["frame_siguiente"], game_data["pieza_siguiente"])
    
    # Verificar si la nueva pieza colisiona al aparecer (game over)
    pieza = TETRIMINOS[game_data["pieza_actual"]][0]
    if hay_colision(game_data["tablero_fijo"], pieza, game_data["x"], game_data["y"]):
        game_data["juego_activo"] = False
        print("¡GAME OVER!")
        messagebox.showinfo("Fin del juego", f"¡Juego terminado!\nPuntuación final: {game_data['puntos']}")
        
        # Registrar partida terminada en el índice
        registrar_partida_en_indice(
            game_data["nombre_jugador"],
            f"partida_terminada_{game_data['puntos']}.txt",
            game_data["puntos"]
        )
        
        game_data["ventana_juego"].destroy()
        game_data["boton_jugar"].config(state=tk.NORMAL)

def rotar_pieza(game_data):
    """Rota la pieza actual si es posible"""
    # Verificar si el juego está pausado
    if game_data.get("juego_pausado", False):
        return
    
    rotacion_actual = game_data["rotacion"]
    pieza_tipo = game_data["pieza_actual"]
    num_rotaciones = longitud(TETRIMINOS[pieza_tipo])
    nueva_rotacion = (rotacion_actual + 1) % num_rotaciones
    pieza = TETRIMINOS[pieza_tipo][nueva_rotacion]
    x = game_data["x"]
    y = game_data["y"]
    tablero_fijo = game_data["tablero_fijo"]
    
    if not hay_colision(tablero_fijo, pieza, x, y):
        game_data["rotacion"] = nueva_rotacion
        actualizar_tablero(game_data)
        # Imprimir tablero después de rotar
        imprimir_tablero_en_consola(game_data)

def caida_automatica(ventana_juego, game_data):
    """Función para la caída automática de las piezas"""
    try:
        # Verificar si el juego todavía está activo, la ventana existe y no está pausado
        if (ventana_juego.winfo_exists() and 
            game_data.get("juego_activo", False) and 
            not game_data.get("juego_pausado", False)):
            
            # Mover la pieza hacia abajo
            mover_pieza(game_data, 0, 1)
            
            # Programar la próxima caída
            ventana_juego.after(1000, lambda: caida_automatica(ventana_juego, game_data))
            
    except tk.TclError:
        # Si hay error al verificar la ventana (probablemente ya no existe)
        game_data["juego_activo"] = False
    except Exception as e:
        print(f"Error en caída automática: {e}")
        game_data["juego_activo"] = False

def imprimir_tablero_en_consola(game_data):
    """Imprime el estado actual del tablero en la consola de manera ordenada y visual"""
    print("\n" + "="*50)
    print(f"Jugador: {game_data['nombre_jugador']} | Puntos: {game_data['puntos']}")
    print("="*50)
    
    # Obtener datos del tablero
    tablero_fijo = game_data.get("tablero_fijo", [])
    if not tablero_fijo:
        print("Error: No hay tablero para mostrar")
        return
    
    filas = longitud(tablero_fijo)
    columnas = longitud(tablero_fijo[0]) if filas > 0 else 0
    
    if filas == 0 or columnas == 0:
        print("Error: Tablero vacío")
        return
    
    # Crear una copia del tablero fijo para visualización
    tablero_visual = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            if tablero_fijo[i][j] is not None:
                fila = agregar(fila, "■")  # Bloque fijo
            else:
                fila = agregar(fila, "·")  # Espacio vacío
        tablero_visual = agregar(tablero_visual, fila)
    
    # Agregar la pieza actual al tablero visual
    try:
        pieza = TETRIMINOS[game_data["pieza_actual"]][game_data["rotacion"]]
        for i in range(longitud(pieza)):
            for j in range(longitud(pieza[i])):
                if pieza[i][j] == 1:
                    y = game_data["y"] + i
                    x = game_data["x"] + j
                    if 0 <= y < filas and 0 <= x < columnas:
                        tablero_visual[y][x] = "□"  # Pieza en movimiento
    except Exception as e:
        print(f"Error al agregar pieza actual: {e}")
    
    # Imprimir el borde superior
    print("╔" + "══" * columnas + "╗")
    
    # Imprimir filas del tablero
    for fila in tablero_visual:
        linea = "║"
        for celda in fila:
            linea += celda + " "
        linea += "║"
        print(linea)
    
    # Imprimir el borde inferior
    print("╚" + "══" * columnas + "╝")
    print(f"Pieza actual: {game_data['pieza_actual']} | Siguiente: {game_data['pieza_siguiente']}")
    print("="*30)

def mostrar_partidas_guardadas(ventana_principal, boton_jugar):
    """Muestra una ventana con las partidas guardadas disponibles"""
    try:
        directorio_guardados = "partidas_guardadas"
        if not os.path.exists(directorio_guardados):
            messagebox.showinfo("Sin partidas", "No hay partidas guardadas disponibles.")
            return
        
        # Obtener lista de archivos de partidas
        archivos = [f for f in os.listdir(directorio_guardados) if f.endswith('.txt')]
        
        if not archivos:
            messagebox.showinfo("Sin partidas", "No hay partidas guardadas disponibles.")
            return
        
        # Crear ventana para mostrar partidas
        ventana_cargar = tk.Toplevel(ventana_principal)
        ventana_cargar.title("Cargar Partida")
        ventana_cargar.geometry("600x500")
        ventana_cargar.config(bg="#1a1a2e")
        ventana_cargar.resizable(False, False)
        ventana_cargar.transient(ventana_principal)
        
        # Centrar ventana
        posicionar_ventana(ventana_cargar, 600, 500)
        
        # Título
        label_titulo = tk.Label(
            ventana_cargar,
            text="PARTIDAS GUARDADAS",
            bg="#1a2a2e", fg="white",
            font=FUENTE_RETRO
        )
        label_titulo.pack(pady=20)
        
        # Frame para la lista de partidas
        frame_lista = tk.Frame(ventana_cargar, bg="#1a2a2e")
        frame_lista.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Scrollbar para la lista
        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox para mostrar partidas
        listbox_partidas = tk.Listbox(
            frame_lista,
            bg="#2c3e50", fg="white",
            font=("Press Start 2P", 10),
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar.set
        )
        listbox_partidas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox_partidas.yview)
        
        # Cargar información de partidas
        partidas_info = []
        for archivo in archivos:
            info = leer_info_partida(f"{directorio_guardados}/{archivo}")
            if info:
                partidas_info = agregar(partidas_info, (archivo, info))
                # Mostrar formato: "Jugador - Puntos - Fecha"
                listbox_partidas.insert(tk.END, f"{info['jugador']} - {info['puntos']} pts - {info['fecha']}")
        
        # Frame para botones
        frame_botones = tk.Frame(ventana_cargar, bg="#1a2a2e")
        frame_botones.pack(pady=20)
        
        # Botón cargar
        def cargar_partida_seleccionada():
            seleccion = listbox_partidas.curselection()
            if seleccion:
                archivo_seleccionado = partidas_info[seleccion[0]][0]
                ruta_archivo = f"{directorio_guardados}/{archivo_seleccionado}"
                cargar_partida(ruta_archivo, ventana_principal, boton_jugar)
                ventana_cargar.destroy()
            else:
                messagebox.showwarning("Selección", "Por favor selecciona una partida para cargar.")
        
        boton_cargar_partida = tk.Button(
            frame_botones,
            text="CARGAR",
            bg="#4ecca3", fg="#1a2e2e",
            font=FUENTE_RETRO,
            width=10, height=2,
            command=cargar_partida_seleccionada,
            relief=tk.GROOVE
        )
        boton_cargar_partida.pack(side=tk.LEFT, padx=10)
        boton_cargar_partida.bind("<Enter>", lambda e: boton_cargar_partida.config(bg="#6be0bc"))
        boton_cargar_partida.bind("<Leave>", lambda e: boton_cargar_partida.config(bg="#4ecca3"))
        
        # Botón eliminar
        def eliminar_partida_seleccionada():
            seleccion = listbox_partidas.curselection()
            if seleccion:
                archivo_seleccionado = partidas_info[seleccion[0]][0]
                confirmacion = messagebox.askyesno("Eliminar", "¿Estás seguro de eliminar esta partida?")
                if confirmacion:
                    try:
                        os.remove(f"{directorio_guardados}/{archivo_seleccionado}")
                        listbox_partidas.delete(seleccion[0])
                        partidas_info.pop(seleccion[0])
                        messagebox.showinfo("Eliminado", "Partida eliminada correctamente.")
                    except Exception as e:
                        messagebox.showerror("Error", f"Error al eliminar: {str(e)}")
            else:
                messagebox.showwarning("Selección", "Por favor selecciona una partida para eliminar.")
        
        boton_eliminar = tk.Button(
            frame_botones,
            text="ELIMINAR",
            bg="#e84545", fg="white",
            font=FUENTE_RETRO,
            width=10, height=2,
            command=eliminar_partida_seleccionada,
            relief=tk.GROOVE
        )
        boton_eliminar.pack(side=tk.LEFT, padx=10)
        boton_eliminar.bind("<Enter>", lambda e: boton_eliminar.config(bg="#ff6b6b"))
        boton_eliminar.bind("<Leave>", lambda e: boton_eliminar.config(bg="#e84545"))
        
        # Botón cerrar
        boton_cerrar = tk.Button(
            frame_botones,
            text="CERRAR",
            bg="#ffd369", fg="#1a2e2e",
            font=FUENTE_RETRO,
            width=10, height=2,
            command=ventana_cargar.destroy,
            relief=tk.GROOVE
        )
        boton_cerrar.pack(side=tk.LEFT, padx=10)
        boton_cerrar.bind("<Enter>", lambda e: boton_cerrar.config(bg="#ffe085"))
        boton_cerrar.bind("<Leave>", lambda e: boton_cerrar.config(bg="#ffd369"))
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al mostrar partidas: {str(e)}")


def leer_info_partida(ruta_archivo):
    """Lee la información básica de una partida guardada"""
    try:
        with open(ruta_archivo, "r") as archivo:
            lineas = archivo.readlines()
            info = {}
            for linea in lineas:
                if linea.startswith("Jugador:"):
                    info['jugador'] = linea.replace("Jugador:", "").strip()
                elif linea.startswith("Puntos:"):
                    info['puntos'] = linea.replace("Puntos:", "").strip()
                elif linea.startswith("Fecha:"):
                    info['fecha'] = linea.replace("Fecha:", "").strip()
            return info
    except Exception as e:
        print(f"Error al leer archivo {ruta_archivo}: {e}")
        return None


def cargar_partida(ruta_archivo, ventana_principal, boton_jugar):
    """Carga una partida desde archivo y reanuda el juego"""
    try:
        # Leer datos de la partida
        datos_partida = {}
        tablero_lineas = []
        leyendo_tablero = False
        
        with open(ruta_archivo, "r") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea.startswith("Jugador:"):
                    datos_partida['nombre_jugador'] = linea.replace("Jugador:", "").strip()
                elif linea.startswith("Puntos:"):
                    datos_partida['puntos'] = int(linea.replace("Puntos:", "").strip())
                elif linea.startswith("Estado del tablero:"):
                    leyendo_tablero = True
                elif linea.startswith("Pieza actual:"):
                    leyendo_tablero = False
                    datos_partida['pieza_actual'] = linea.replace("Pieza actual:", "").strip()
                elif linea.startswith("Rotación:"):
                    datos_partida['rotacion'] = int(linea.replace("Rotación:", "").strip())
                elif linea.startswith("Posición X:"):
                    datos_partida['x'] = int(linea.replace("Posición X:", "").strip())
                elif linea.startswith("Posición Y:"):
                    datos_partida['y'] = int(linea.replace("Posición Y:", "").strip())
                elif linea.startswith("Siguiente pieza:"):
                    datos_partida['pieza_siguiente'] = linea.replace("Siguiente pieza:", "").strip()
                elif leyendo_tablero and linea:
                    tablero_lineas = agregar(tablero_lineas, linea)
                    
        
        # Iniciar juego con datos cargados
        iniciar_juego_cargado(datos_partida, tablero_lineas, ventana_principal, boton_jugar)
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar partida: {str(e)}")


def iniciar_nuevas_piezas():
    """Inicializa una pieza actual y una siguiente pieza aleatoriamente"""
    pieza_actual = random.choice(list(TETRIMINOS.keys()))
    pieza_siguiente = random.choice(list(TETRIMINOS.keys()))
    return pieza_actual, pieza_siguiente

def mostrar_siguiente_pieza(frame_siguiente, tipo_pieza):
    """Muestra la siguiente pieza en el frame correspondiente"""
    # Limpiar el frame
    for widget in frame_siguiente.winfo_children():
        widget.destroy()
    
    # Obtener la pieza y su color
    pieza = TETRIMINOS[tipo_pieza][0]  # Primera rotación
    color = COLORES_TETRIMINOS[tipo_pieza]
    
    # Crear mini tablero para mostrar la pieza
    for i in range(longitud(pieza)):
        for j in range(longitud(pieza[i])):
            if pieza[i][j]:
                mini_celda = tk.Label(
                    frame_siguiente,
                    bg=color,
                    width=2,
                    height=1,
                    borderwidth=1,
                    relief=tk.RAISED
                )
                mini_celda.grid(row=i, column=j, padx=1, pady=1)

def actualizar_tablero(game_data):
    """Actualiza la visualización del tablero con la pieza actual y las piezas fijas"""
    tablero = game_data["tablero"]
    tablero_fijo = game_data["tablero_fijo"]
    pieza_actual = TETRIMINOS[game_data["pieza_actual"]][game_data["rotacion"]]
    color_pieza = COLORES_TETRIMINOS[game_data["pieza_actual"]]
    x = game_data["x"]
    y = game_data["y"]
    
    # Limpiar tablero visual y mostrar piezas fijas
    for i in range(longitud(tablero)):
        for j in range(longitud(tablero[i])):
            if i < longitud(tablero_fijo) and j < longitud(tablero_fijo[0]):
                if tablero_fijo[i][j] is not None:
                    # Mostrar pieza fija
                    tablero[i][j].config(bg=tablero_fijo[i][j])
                else:
                    # Mostrar espacio vacío
                    tablero[i][j].config(bg="#1a2a6d")
            else:
                # Mostrar espacio vacío si no hay datos del tablero fijo
                tablero[i][j].config(bg="#1a2a6d")
    
    # Mostrar pieza actual
    for i in range(longitud(pieza_actual)):
        for j in range(longitud(pieza_actual[i])):
            if pieza_actual[i][j] == 1:
                pos_y = y + i
                pos_x = x + j
                if 0 <= pos_y < longitud(tablero) and 0 <= pos_x < longitud(tablero[0]):
                    tablero[pos_y][pos_x].config(bg=color_pieza)

def iniciar_juego_cargado(datos_partida, tablero_lineas, ventana_principal, boton_jugar):
    """Inicia el juego con una partida cargada"""
    print("Cargando partida guardada...")
    messagebox.showinfo("Cargar", f"¡Partida de {datos_partida['nombre_jugador']} cargada!")
    boton_jugar.config(state=tk.DISABLED)
    
    # Crear ventana de juego (similar a la función jugar())
    ventana_juego = tk.Toplevel()
    ventana_juego.title("Tetris - Partida Cargada")
    ventana_juego.geometry("800x700")
    ventana_juego.resizable(False, False)
    ventana_juego.config(bg="#1a1a2e")
    
    # Crear layout dividido en dos secciones
    # Frame para la matriz de juego (izquierda)
    frame_matriz = tk.Frame(ventana_juego, bg="#1a2a2e", bd=4, relief=tk.GROOVE)
    frame_matriz.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)

    # Frame para información del juego (derecha)
    frame_info = tk.Frame(ventana_juego, bg="#1a2a2e", bd=4, relief=tk.GROOVE, width=300)
    frame_info.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH)
    
    # Crear elementos de la interfaz
    label_info = tk.Label(frame_info, text="INFORMACIÓN", bg="#1a2a2e", fg="white", font=FUENTE_RETRO)
    label_info.pack(pady=10)
    
    label_jugador = tk.Label(frame_info, text=f"JUGADOR: {datos_partida['nombre_jugador']}", bg="#1a2a2e", fg="white", font=FUENTE_RETRO)
    label_jugador.pack(pady=10)
    
    label_siguiente = tk.Label(frame_info, text="SIGUIENTE PIEZA", bg="#1a2a2e", fg="white", font=FUENTE_RETRO)
    label_siguiente.pack(pady=20)
    
    frame_siguiente = tk.Frame(frame_info, bg="#1a2a2e", bd=2, relief=tk.SUNKEN, width=150, height=150)
    frame_siguiente.pack(pady=10)
    
    label_puntos = tk.Label(frame_info, text=f"PUNTOS: {datos_partida['puntos']}", bg="#1a2a2e", fg="white", font=FUENTE_RETRO)
    label_puntos.pack(pady=20)
    
    # Inicializar tablero CON LA MATRIZ DEL ARCHIVO
    tablero = inicializar_tablero(frame_matriz)
    
    # Inicializar tablero fijo base con obstáculos del archivo
    tablero_fijo_base = inicializar_tablero_fijo_con_matriz()
    
    # Recrear tablero fijo combinando obstáculos del archivo con datos guardados
    FILAS = longitud(tablero_fijo_base)
    COLUMNAS = longitud(tablero_fijo_base[0])
    
    for i, linea in enumerate(tablero_lineas):
        if i < FILAS:  # Asegurar que no exceda las filas del tablero
            for j, char in enumerate(linea):
                if j < COLUMNAS and char == 'X':  # Piezas fijas guardadas
                    tablero_fijo_base[i][j] = "#808080"  # Color gris para piezas fijas
    
    # Mostrar siguiente pieza
    mostrar_siguiente_pieza(frame_siguiente, datos_partida['pieza_siguiente'])
    
    # Variables de control del juego con datos cargados
    game_data = {
        "tablero": tablero,
        "tablero_fijo": tablero_fijo_base,  # Usar el tablero que combina archivo + datos guardados
        "pieza_actual": datos_partida['pieza_actual'],
        "rotacion": datos_partida['rotacion'],
        "x": datos_partida['x'],
        "y": datos_partida['y'],
        "pieza_siguiente": datos_partida['pieza_siguiente'],
        "frame_siguiente": frame_siguiente,
        "puntos": datos_partida['puntos'],
        "label_puntos": label_puntos,
        "juego_activo": True,
        "ventana_juego": ventana_juego,
        "boton_jugar": boton_jugar,
        "nombre_jugador": datos_partida['nombre_jugador']
    }
    
    # Botón de pausa
    boton_pausa = tk.Button(
        frame_info, text="PAUSA", bg="#ffd369", fg="#1a2e2e", font=FUENTE_RETRO,
        width=10, height=2, command=lambda: mostrar_menu_pausa(ventana_juego, game_data), relief=tk.GROOVE
    )
    boton_pausa.pack(pady=20)
    boton_pausa.bind("<Enter>", lambda e: boton_pausa.config(bg="#ffe085"))
    boton_pausa.bind("<Leave>", lambda e: boton_pausa.config(bg="#ffd369"))
    
    # Actualizar visualización
    actualizar_tablero(game_data)
    
    # Configurar eventos de teclado
    ventana_juego.bind("<Left>", lambda event: mover_pieza(game_data, -1, 0))
    ventana_juego.bind("<Right>", lambda event: mover_pieza(game_data, 1, 0))
    ventana_juego.bind("<Down>", lambda event: mover_pieza(game_data, 0, 1))
    ventana_juego.bind("<space>", lambda event: rotar_pieza(game_data))
    ventana_juego.bind("<p>", lambda event: mostrar_menu_pausa(ventana_juego, game_data))
    ventana_juego.focus_set()
    
    # Iniciar bucle de caída automática
    ventana_juego.after(1000, lambda: caida_automatica(ventana_juego, game_data))


if __name__ == "__main__":
    iniciar_juego()