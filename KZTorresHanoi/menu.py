import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Text, Scrollbar, Canvas as tkCanvas
from PIL import Image, ImageTk
import time
import math

class PantallaMenuPrincipal(ttk.Frame):
    def __init__(self, master, controlador):
        super().__init__(master, padding="30 20 30 20") # Llama al constructor de la clase padre (ttk.Frame) con más padding vertical
        self.master = master  # Ventana principal o contenedor padre
        self.controlador = controlador # Instancia del controlador de la aplicación
        self.discos_seleccionados = tk.IntVar(value=3) # Variable de Tkinter para almacenar el número de discos, inicializada en 3

        # --- Estilización de la interfaz ---
        estilo = ttk.Style() # Crea una instancia de Style para personalizar widgets
        
        # Fuente base
        fuente_base = "Segoe UI"
        fuente_base_alternativa = "Arial"

        # Configura el estilo para el frame principal del menú
        estilo.configure("MenuPrincipal.TFrame", background="#2c3e50") 
        
        # Configura el estilo para las etiquetas en el menú
        estilo.configure("MenuPrincipal.TLabel", background="#2c3e50", foreground="#ecf0f1", font=(fuente_base, 12, "normal"))
        
        # Configura el estilo para la etiqueta del título
        estilo.configure("Titulo.TLabel", background="#2c3e50", foreground="#ffffff", font=(fuente_base, 28, "bold"))
        
        # Configura el estilo para la etiqueta del subtítulo
        estilo.configure("Subtitulo.TLabel", background="#2c3e50", foreground="#bdc3c7", font=(fuente_base, 16))
        
        # Configura el estilo para los Radiobotones de selección de discos
        estilo.configure("BotonDisco.TRadiobutton", 
                         background="#2c3e50", 
                         foreground="#ecf0f1", 
                         font=(fuente_base, 11), 
                         padding=(10, 5), 
                         indicatordiameter=18) # Diámetro del indicador del radiobutton
        estilo.map("BotonDisco.TRadiobutton",
                   background=[('active', "#34495e"), ('selected', '#2c3e50')], # Mantiene fondo al seleccionar para que el texto resalte
                   foreground=[('selected', '#5dade2'), ('active', '#ffffff')],
                   indicatorcolor=[('selected', '#5dade2'), ('active', '#bdc3c7')])

        # Configura el estilo para el botón de inicio
        estilo.configure("Inicio.TButton", 
                         font=(fuente_base, 15, "bold"), 
                         padding=(20, 12), # Más padding para un botón más grande
                         background="#27ae60", 
                         foreground="#34495e",
                         relief=tk.FLAT,
                         borderwidth=0)
        estilo.map("Inicio.TButton", 
                   background=[('active', '#2ecc71'), ('pressed', '#1abc9c')],
                   relief=[('pressed', tk.SUNKEN), ('!pressed', tk.FLAT)])
        
        # Configura el estilo para la etiqueta de instrucciones
        estilo.configure("Instrucciones.TLabel", 
                         background="#2c3e50", 
                         foreground="#95a5a6", 
                         font=(fuente_base, 10), 
                         justify=tk.LEFT,
                         wraplength=450) # Ajusta el ancho del texto antes de saltar línea

        self.configure(style="MenuPrincipal.TFrame") # Aplica el estilo al frame actual
        
        # Configura cómo se expanden las filas de la cuadrícula (grid)
        # Se da más peso a las filas con contenido principal para centrarlo verticalmente
        self.grid_rowconfigure(0, weight=2)  # Título
        self.grid_rowconfigure(1, weight=1)  # Subtítulo
        self.grid_rowconfigure(2, weight=1)  # Etiqueta selección discos
        self.grid_rowconfigure(3, weight=1)  # Botones discos
        self.grid_rowconfigure(4, weight=1)  # Separador 1
        self.grid_rowconfigure(5, weight=2)  # Botón Iniciar
        self.grid_rowconfigure(6, weight=1)  # Separador 2
        self.grid_rowconfigure(7, weight=3)  # Instrucciones (más espacio abajo)
        self.grid_rowconfigure(8, weight=1)  # Espacio inferior
        
        # Configura cómo se expande la columna de la cuadrícula
        self.grid_columnconfigure(0, weight=1)

        # --- Creación de Widgets (elementos de la interfaz) ---
        etiqueta_titulo = ttk.Label(self, text="Torres de Hanói", style="Titulo.TLabel")
        etiqueta_titulo.grid(row=0, column=0, pady=(30, 5)) 

        etiqueta_subtitulo = ttk.Label(self, text="Visualización de Árbol Binario", style="Subtitulo.TLabel")
        etiqueta_subtitulo.grid(row=1, column=0, pady=(0, 25))

        etiqueta_seleccion_discos = ttk.Label(self, text="Selecciona el número de discos:", style="MenuPrincipal.TLabel")
        etiqueta_seleccion_discos.grid(row=2, column=0, pady=(15, 8))

        # Frame para los botones de selección de discos
        frame_botones_discos = ttk.Frame(self, style="MenuPrincipal.TFrame")
        frame_botones_discos.grid(row=3, column=0, pady=8)

        # Crea los radiobotones para seleccionar el número de discos (3 a 6)
        for i, num_discos_opcion in enumerate([3, 4, 5, 6]):
            boton_radio = ttk.Radiobutton(frame_botones_discos, 
                                          text=str(num_discos_opcion), 
                                          value=num_discos_opcion, 
                                          variable=self.discos_seleccionados, 
                                          style="BotonDisco.TRadiobutton")
            boton_radio.pack(side=tk.LEFT, padx=12, pady=5) 
            if num_discos_opcion == 3: 
                boton_radio.invoke() 
        
        # Separador
        separador1 = ttk.Separator(self, orient='horizontal')
        separador1.grid(row=4, column=0, sticky='ew', pady=25, padx=50)

        # Botón para iniciar el juego
        boton_iniciar = ttk.Button(self, text="Iniciar Juego", command=self.iniciar_juego, style="Inicio.TButton")
        boton_iniciar.grid(row=5, column=0, pady=20) 
        
        # Separador
        separador2 = ttk.Separator(self, orient='horizontal')
        separador2.grid(row=6, column=0, sticky='ew', pady=25, padx=50)

        # Texto de las instrucciones
        texto_instrucciones = (
            "Instrucciones (en el juego):\n"
            "• El objetivo es mover todos los discos a la torre derecha (Torre C).\n"
            "• No se puede colocar un disco grande sobre uno más pequeño.\n"
            "• Haz clic en una torre para seleccionar un disco, luego en otra para colocarlo.\n"
            "• Usa los controles del juego para resolver automáticamente o reiniciar.\n"
            "• Visualiza la estructura de solución con los botones de árbol.\n"
            "• Presiona ESC para volver al menú principal."
        )
        etiqueta_instrucciones = ttk.Label(self, text=texto_instrucciones, style="Instrucciones.TLabel")
        etiqueta_instrucciones.grid(row=7, column=0, pady=(15, 30), padx=20, sticky="n")
        
    # Método llamado cuando se presiona el botón "Iniciar Juego"
    def iniciar_juego(self):
        num_discos = self.discos_seleccionados.get() # Obtiene el número de discos seleccionado
        self.controlador.mostrar_pantalla_juego(num_discos) # Llama al controlador para cambiar de pantalla

# Clase para la pantalla del juego
