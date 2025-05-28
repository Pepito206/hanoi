from menu import PantallaMenuPrincipal
from juego import PantallaJuego
import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Text, Scrollbar, Canvas as tkCanvas
from PIL import Image, ImageTk
import time
import math

class ControladorApp(tk.Tk):
    def __init__(self):
        super().__init__() # Llama al constructor de tk.Tk
        self.title("Torres de Hanói - Visualización") # Título de la ventana principal
        self.geometry("1920x1080") # Tamaño inicial de la ventana principal

        self.frame_actual = None # Referencia al frame (pantalla) actualmente visible
        self.mostrar_pantalla_menu() # Muestra la pantalla del menú al iniciar

    # Muestra la pantalla del menú principal
    def mostrar_pantalla_menu(self):
        if self.frame_actual: # Si hay un frame actual, lo destruye
            self.frame_actual.destroy()
        # Crea y empaqueta el nuevo frame del menú
        self.frame_actual = PantallaMenuPrincipal(self, self)
        self.frame_actual.pack(fill=tk.BOTH, expand=True)
        self.title("Torres de Hanói - Menú Principal") # Actualiza el título de la ventana

    # Muestra la pantalla del juego
    def mostrar_pantalla_juego(self, numero_discos):
        if self.frame_actual:
            self.frame_actual.destroy()
        # Crea y empaqueta el nuevo frame del juego, pasando el número de discos
        self.frame_actual = PantallaJuego(self, self, numero_discos)
        self.frame_actual.pack(fill=tk.BOTH, expand=True)
        self.title(f"Torres de Hanói - Jugando con {numero_discos} discos") # Actualiza el título

# Punto de entrada principal de la aplicación
