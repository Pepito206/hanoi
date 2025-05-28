import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Text, Scrollbar, Canvas as tkCanvas
from PIL import Image, ImageTk
import time
import math

class PantallaJuego(ttk.Frame):
    def __init__(self, master, controlador, numero_discos_inicial):
        super().__init__(master, padding="10")
        self.master = master 
        self.controlador = controlador 
        
        self.numero_discos_var = tk.IntVar(value=numero_discos_inicial) # Variable Tkinter para el número de discos en juego
        self.torres_logicas = [[], [], []] # Representación lógica de las torres y los discos en ellas
        self.items_canvas_discos_por_torre = [[], [], []] # Almacena los IDs de los discos (objetos del canvas) por torre
        self.items_canvas_bases_torres = [] # Almacena los IDs de las bases de las torres (objetos del canvas)
        self.postes_torres_coords = [] # Almacena coordenadas y dimensiones de los postes de las torres
        self.contador_movimientos_interno = 0 # Contador interno para la animación de la solución
        self.contador_movimientos_mostrado = 0 # Contador de movimientos que se muestra al usuario
        self.velocidad_animacion_ms = 500 # Velocidad de la animación en milisegundos
        self.resolviendo_automaticamente = False # Bandera para indicar si la solución automática está en curso

        # Colores para los discos (Rojo, Naranja, Amarillo, Verde, Azul, Índigo, Violeta)
        self.colores_discos = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#9400D3"]
        self.contorno_disco_defecto = "black" # Color del contorno del disco por defecto
        self.contorno_disco_seleccionado = "yellow" # Color del contorno del disco seleccionado
        self.relleno_torre_movimiento_valido = "lightgreen" # Color de la base de la torre para un movimiento válido
        self.relleno_torre_movimiento_invalido = "salmon" # Color de la base de la torre para un movimiento inválido
        self.relleno_torre_origen_resaltada = "lightblue" # Color de la base de la torre de origen seleccionada
        self.relleno_base_torre_defecto = "saddlebrown" # Color por defecto de la base de la torre

        self.valor_disco_sujetado = None # Valor del disco que el usuario está "sujetando"
        self.id_canvas_disco_sujetado = None # ID del objeto del canvas del disco sujetado
        self.indice_torre_origen = None # Índice de la torre de donde se tomó el disco
        self.etiqueta_estado_modo_manual = None # Etiqueta para mostrar mensajes en el modo manual

        self.ventana_arbol_texto = None # Referencia a la ventana del árbol de texto
        self.ventana_arbol_grafico = None # Referencia a la ventana del árbol gráfico

        # --- Colores para la visualización del árbol de texto ---
        self.colores_arbol_texto = {
            "subproblema": "blue",
            "accion_general": "darkgreen", 
            "encabezado": "purple",
            # Las etiquetas específicas de los discos se generan dinámicamente
        }

        # --- Colores para la visualización del árbol gráfico ---
        self.color_linea_arbol_grafico = "gray40" 
        self.color_texto_nodo_arbol_grafico = "black"
        self.color_defecto_nodo_arbol_grafico = "lightgray" 

        # --- Distribución de la Interfaz (Layout) ---
        frame_controles_superiores = ttk.Frame(self) # Frame para los controles en la parte superior
        frame_controles_superiores.pack(side=tk.TOP, fill=tk.X, pady=(0,5))

        # Frame para los controles del juego (botones, etc.)
        frame_controles_juego = ttk.LabelFrame(frame_controles_superiores, text="Controles del Juego", padding="10")
        frame_controles_juego.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.etiqueta_numero_discos = ttk.Label(frame_controles_juego, text=f"Discos: {self.numero_discos_var.get()}")
        self.etiqueta_numero_discos.pack(side=tk.LEFT, padx=5)

        self.boton_resolver = ttk.Button(frame_controles_juego, text="Resolver Automáticamente", command=self.iniciar_resolucion_automatica)
        self.boton_resolver.pack(side=tk.LEFT, padx=5)

        self.boton_reiniciar = ttk.Button(frame_controles_juego, text="Reiniciar Juego", command=self.reiniciar_juego_desde_boton)
        self.boton_reiniciar.pack(side=tk.LEFT, padx=5)

        self.boton_ver_arbol_texto = ttk.Button(frame_controles_juego, text="Árbol (Texto)", command=self.alternar_visualizacion_arbol_texto)
        self.boton_ver_arbol_texto.pack(side=tk.LEFT, padx=5)
        
        self.boton_ver_arbol_grafico = ttk.Button(frame_controles_juego, text="Árbol (Gráfico)", command=self.alternar_visualizacion_arbol_grafico)
        self.boton_ver_arbol_grafico.pack(side=tk.LEFT, padx=5)

        self.boton_volver_menu = ttk.Button(frame_controles_juego, text="Volver al Menú (ESC)", command=self.ir_a_menu)
        self.boton_volver_menu.pack(side=tk.LEFT, padx=5)
        
        # Frame para el control de velocidad
        frame_velocidad = ttk.Frame(frame_controles_superiores) 
        frame_velocidad.pack(side=tk.LEFT, padx=10)
        ttk.Label(frame_velocidad, text="Velocidad (ms):").pack(side=tk.LEFT)
        self.escala_velocidad = ttk.Scale(frame_velocidad, from_=100, to=1000, orient=tk.HORIZONTAL, command=self.actualizar_velocidad)
        self.escala_velocidad.set(self.velocidad_animacion_ms)
        self.escala_velocidad.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Etiqueta para mostrar el estado del modo manual
        self.etiqueta_estado_modo_manual = ttk.Label(self, text="Modo Manual: Seleccione torre de origen.", anchor="center")
        self.etiqueta_estado_modo_manual.pack(side=tk.TOP, fill=tk.X, pady=2)

        # Dimensiones del canvas del juego
        self.alto_canvas = 350 
        self.ancho_canvas = 550 
        # Creación del canvas donde se dibujarán las torres y discos
        self.canvas_juego = tkCanvas(self, width=self.ancho_canvas, height=self.alto_canvas, bg="lightgrey", relief=tk.SUNKEN, borderwidth=1)
        self.canvas_juego.pack(pady=5, fill=tk.BOTH, expand=True)
        self.canvas_juego.bind("<Button-1>", self.al_hacer_clic_en_canvas) # Asocia el clic del ratón a un método

        # Frame para la información del juego (movimientos, etc.)
        frame_informacion = ttk.LabelFrame(self, text="Información del Juego", padding="10")
        frame_informacion.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        self.etiqueta_movimientos = ttk.Label(frame_informacion, text="Movimientos: 0")
        self.etiqueta_movimientos.pack(side=tk.LEFT, padx=10)

        self.etiqueta_info_arbol = ttk.Label(frame_informacion, text="") # Etiqueta para información del árbol (nodos, altura)
        self.etiqueta_info_arbol.pack(side=tk.LEFT, padx=10)
        
        # Frame para el área de texto que muestra la secuencia de movimientos
        self.frame_area_texto_movimientos = ttk.LabelFrame(self, text="Secuencia de Movimientos", padding="5")
        self.frame_area_texto_movimientos.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, pady=5)
        
        self.area_texto_movimientos = tk.Text(self.frame_area_texto_movimientos, height=6, width=70, wrap=tk.WORD, state=tk.DISABLED)
        barra_desplazamiento_movs = ttk.Scrollbar(self.frame_area_texto_movimientos, command=self.area_texto_movimientos.yview)
        self.area_texto_movimientos.config(yscrollcommand=barra_desplazamiento_movs.set)
        barra_desplazamiento_movs.pack(side=tk.RIGHT, fill=tk.Y)
        self.area_texto_movimientos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Asocia la tecla ESC para volver al menú
        self.master.bind('<Escape>', lambda evento: self.ir_a_menu()) 

        self.reiniciar_juego(numero_discos_inicial) # Inicializa el juego

    # Método para volver al menú principal
    def ir_a_menu(self):
        if self.resolviendo_automaticamente: # Si la solución automática está en curso
            # Pregunta al usuario si desea detenerla
            if not messagebox.askyesno("Volver al Menú", "La solución automática está en curso. ¿Desea detenerla y volver al menú?"):
                return # Si no, no hace nada
            self.resolviendo_automaticamente = False # Detiene la bandera de resolución
        
        # Cierra las ventanas de los árboles si están abiertas
        if self.ventana_arbol_texto: 
            try: self.ventana_arbol_texto.destroy()
            except tk.TclError: pass # Ignora error si la ventana ya no existe
            self.ventana_arbol_texto = None
        if self.ventana_arbol_grafico:
            try: self.ventana_arbol_grafico.destroy()
            except tk.TclError: pass
            self.ventana_arbol_grafico = None
            
        self.master.unbind('<Escape>') # Desvincula la tecla ESC
        self.controlador.mostrar_pantalla_menu() # Llama al controlador para cambiar a la pantalla de menú

    # Actualiza la velocidad de la animación según el valor de la escala
    def actualizar_velocidad(self, valor_escala):
        self.velocidad_animacion_ms = int(float(valor_escala))

    # Dibuja las torres (postes y bases) en el canvas
    def dibujar_torres(self):
        # Elimina los elementos de torre anteriores del canvas
        self.canvas_juego.delete("poste_torre", "id_base_torre") 
        self.postes_torres_coords.clear() # Limpia la lista de coordenadas de postes
        self.items_canvas_bases_torres.clear() # Limpia la lista de IDs de bases
        
        ancho_poste = 10
        alto_poste = self.alto_canvas * 0.7 
        alto_base = 20
        y_base = self.alto_canvas - 20 # Posición Y de la parte superior de la base

        # Dibuja cada una de las 3 torres
        for i in range(3):
            x_centro_torre = (self.ancho_canvas / 3) * (i + 0.5) # Calcula el centro X de la torre
            # Crea la base de la torre
            id_base = self.canvas_juego.create_rectangle(
                x_centro_torre - self.ancho_canvas / 9, y_base, x_centro_torre + self.ancho_canvas / 9, y_base + alto_base,
                fill=self.relleno_base_torre_defecto, tags=(f"id_base_torre_{i}", "id_base_torre") 
            )
            self.items_canvas_bases_torres.append(id_base)

            # Crea el poste de la torre
            poste = self.canvas_juego.create_rectangle(
                x_centro_torre - ancho_poste / 2, y_base - alto_poste,
                x_centro_torre + ancho_poste / 2, y_base,
                fill="burlywood", tags="poste_torre" 
            )
            self.postes_torres_coords.append((x_centro_torre, y_base, alto_poste)) # Guarda información del poste

    # Dibuja los discos en sus posiciones actuales en las torres
    def dibujar_discos(self):
        self.canvas_juego.delete("disco") # Elimina todos los discos anteriores del canvas
        for i in range(3): self.items_canvas_discos_por_torre[i].clear() # Limpia las listas de IDs de discos

        alto_disco = max(15, self.alto_canvas * 0.05) # Altura de cada disco
        ancho_max_total_discos = (self.ancho_canvas / 3) * 0.8 # Ancho máximo disponible para el disco más grande
        valor_max_disco_actual = self.numero_discos_var.get() # Número de discos en el juego actual
        # Ancho mínimo para el disco más pequeño (disco 1)
        ancho_min_disco = ancho_max_total_discos / (valor_max_disco_actual if valor_max_disco_actual > 1 else 2)
        ancho_min_disco = max(20, ancho_min_disco) # Asegura un ancho mínimo visible

        # Incremento de ancho por cada unidad de tamaño del disco
        if valor_max_disco_actual > 1:
            incremento_ancho_disco = (ancho_max_total_discos - ancho_min_disco) / (valor_max_disco_actual - 1)
        else:
            incremento_ancho_disco = 0 

        if not self.postes_torres_coords: return # Si no hay postes dibujados, no hacer nada

        # Itera sobre cada torre lógica
        for indice_torre, contenido_torre in enumerate(self.torres_logicas):
            x_centro_poste, y_base_poste, _ = self.postes_torres_coords[indice_torre] # Obtiene datos del poste
            # Itera sobre cada disco en la pila de la torre actual
            for indice_disco_en_pila, valor_tamano_disco in enumerate(contenido_torre):
                # Calcula el ancho del disco actual
                ancho_disco_actual = ancho_min_disco + (valor_tamano_disco - 1) * incremento_ancho_disco
                # Calcula las coordenadas (x1, y1, x2, y2) del rectángulo del disco
                x1 = x_centro_poste - ancho_disco_actual / 2
                y1 = y_base_poste - (indice_disco_en_pila + 1) * alto_disco
                x2 = x_centro_poste + ancho_disco_actual / 2
                y2 = y_base_poste - indice_disco_en_pila * alto_disco
                # Obtiene el color del disco
                indice_color = (valor_tamano_disco - 1) % len(self.colores_discos)
                color_disco = self.colores_discos[indice_color]
                
                contorno_color = self.contorno_disco_defecto
                ancho_contorno = 1
                
                # Crea el rectángulo del disco en el canvas
                id_canvas_disco = self.canvas_juego.create_rectangle(x1, y1, x2, y2, 
                                                                fill=color_disco, 
                                                                outline=contorno_color, 
                                                                width=ancho_contorno,
                                                                tags="disco")
                self.items_canvas_discos_por_torre[indice_torre].append(id_canvas_disco) # Guarda el ID del disco

    # Método llamado por el botón "Reiniciar Juego"
    def reiniciar_juego_desde_boton(self):
        self.reiniciar_juego(self.numero_discos_var.get())

    # Lógica principal para reiniciar el juego
    def reiniciar_juego(self, numero_discos_a_establecer):
        if self.resolviendo_automaticamente: # No permitir reiniciar si se está resolviendo
            messagebox.showwarning("En progreso", "La solución automática está en curso. No se puede reiniciar ahora.")
            return

        self.numero_discos_var.set(numero_discos_a_establecer) # Establece el número de discos
        self.etiqueta_numero_discos.config(text=f"Discos: {self.numero_discos_var.get()}") 

        self.canvas_juego.delete("all") # Limpia todo el canvas
        self.dibujar_torres() # Dibuja las torres

        n_discos = self.numero_discos_var.get()
        # Inicializa la torre 0 con todos los discos en orden descendente
        self.torres_logicas = [[i for i in range(n_discos, 0, -1)], [], []] 
        
        self.dibujar_discos() # Dibuja los discos en su estado inicial

        # Resetea contadores y etiquetas
        self.contador_movimientos_interno = 0
        self.contador_movimientos_mostrado = 0
        self.etiqueta_movimientos.config(text=f"Movimientos: {self.contador_movimientos_mostrado}")
        
        # Limpia el área de texto de movimientos
        self.area_texto_movimientos.config(state=tk.NORMAL)
        self.area_texto_movimientos.delete(1.0, tk.END)
        self.area_texto_movimientos.config(state=tk.DISABLED)

        # Actualiza la información del árbol
        nodos_movimientos_arbol = (2**n_discos) - 1
        altura_arbol = n_discos
        self.etiqueta_info_arbol.config(text=f"Para {n_discos} discos: Movs/Nodos: {nodos_movimientos_arbol}, Altura Árbol: {altura_arbol}")
        
        # Habilita los botones
        self.boton_resolver.config(state=tk.NORMAL) 
        self.boton_reiniciar.config(state=tk.NORMAL)
        self.boton_ver_arbol_texto.config(state=tk.NORMAL)
        self.boton_ver_arbol_grafico.config(state=tk.NORMAL)
        self.boton_volver_menu.config(state=tk.NORMAL)
        self.resolviendo_automaticamente = False # Asegura que la bandera de resolución esté desactivada
        self._limpiar_estado_movimiento_manual_y_resaltados() # Limpia cualquier estado del modo manual
        
        # Cierra las ventanas de los árboles si están abiertas
        if self.ventana_arbol_texto: 
            try: self.ventana_arbol_texto.destroy()
            except tk.TclError: pass
            self.ventana_arbol_texto = None
        if self.ventana_arbol_grafico:
            try: self.ventana_arbol_grafico.destroy()
            except tk.TclError: pass
            self.ventana_arbol_grafico = None

    # Limpia el estado del modo manual (disco sujetado, resaltados)
    def _limpiar_estado_movimiento_manual_y_resaltados(self):
        # Restaura el contorno del disco que estaba sujetado
        if self.id_canvas_disco_sujetado:
            try:
                self.canvas_juego.itemconfig(self.id_canvas_disco_sujetado, outline=self.contorno_disco_defecto, width=1)
            except tk.TclError: # El item podría haber sido eliminado
                pass 
        self.valor_disco_sujetado = None
        self.id_canvas_disco_sujetado = None
        self.indice_torre_origen = None
        
        # Restaura el color de las bases de las torres
        for id_item_base in self.items_canvas_bases_torres:
            try:
                self.canvas_juego.itemconfig(id_item_base, fill=self.relleno_base_torre_defecto)
            except tk.TclError: # La ventana/canvas podría estar cerrándose
                pass

        # Restaura el mensaje de la etiqueta de estado del modo manual
        if self.etiqueta_estado_modo_manual:
            self.etiqueta_estado_modo_manual.config(text="Modo Manual: Seleccione torre de origen.")
            
    # Actualiza el resaltado de las torres para indicar movimientos válidos/inválidos
    def _actualizar_resaltado_torres(self):
        if self.valor_disco_sujetado is None: # Si no hay disco seleccionado, restaura todas las torres
            for i, id_base in enumerate(self.items_canvas_bases_torres):
                try:
                    self.canvas_juego.itemconfig(id_base, fill=self.relleno_base_torre_defecto)
                except tk.TclError: pass
            return

        # Si hay un disco seleccionado, resalta las torres según las reglas
        for i, id_base in enumerate(self.items_canvas_bases_torres):
            try:
                if i == self.indice_torre_origen: # Torre de origen
                    self.canvas_juego.itemconfig(id_base, fill=self.relleno_torre_origen_resaltada)
                else: # Torre de destino potencial
                    # Movimiento válido si la torre destino está vacía o el disco superior es más grande
                    if not self.torres_logicas[i] or self.valor_disco_sujetado < self.torres_logicas[i][-1]:
                        self.canvas_juego.itemconfig(id_base, fill=self.relleno_torre_movimiento_valido) 
                    else: # Movimiento inválido
                        self.canvas_juego.itemconfig(id_base, fill=self.relleno_torre_movimiento_invalido) 
            except tk.TclError: pass


    # Maneja los clics del ratón en el canvas del juego (para el modo manual)
    def al_hacer_clic_en_canvas(self, evento):
        if self.resolviendo_automaticamente: # No permitir interacción si se está resolviendo
            messagebox.showinfo("Solución en Curso", "La solución automática está en ejecución. No se puede interactuar manualmente.")
            return

        # Determina en qué torre se hizo clic basándose en la coordenada X del evento
        indice_torre_clicada = -1
        ancho_tercio_torre = self.ancho_canvas / 3
        if evento.x < ancho_tercio_torre: indice_torre_clicada = 0
        elif evento.x < 2 * ancho_tercio_torre: indice_torre_clicada = 1
        else: indice_torre_clicada = 2

        if indice_torre_clicada == -1: return # Si el clic fue fuera de las áreas de las torres
        nombres_torres = ['A', 'B', 'C'] # Nombres para los mensajes

        # --- Lógica para tomar un disco ---
        if self.valor_disco_sujetado is None: 
            if self.torres_logicas[indice_torre_clicada]: # Si la torre clicada tiene discos
                self.valor_disco_sujetado = self.torres_logicas[indice_torre_clicada][-1] # Toma el valor del disco superior
                self.indice_torre_origen = indice_torre_clicada
                
                # Resalta el disco seleccionado
                if self.items_canvas_discos_por_torre[self.indice_torre_origen]:
                    self.id_canvas_disco_sujetado = self.items_canvas_discos_por_torre[self.indice_torre_origen][-1]
                    self.canvas_juego.itemconfig(self.id_canvas_disco_sujetado, outline=self.contorno_disco_seleccionado, width=2)

                self.etiqueta_estado_modo_manual.config(text=f"Disco {self.valor_disco_sujetado} seleccionado de Torre {nombres_torres[self.indice_torre_origen]}. Elija destino.")
                self._actualizar_resaltado_torres() # Actualiza el resaltado de las torres
            else: # Si se hizo clic en una torre vacía
                messagebox.showinfo("Torre Vacía", f"La Torre {nombres_torres[indice_torre_clicada]} está vacía. No se puede tomar un disco.")
                self.etiqueta_estado_modo_manual.config(text="Modo Manual: Seleccione torre de origen.")
        
        # --- Lógica para colocar el disco sujetado ---
        else: 
            indice_torre_destino = indice_torre_clicada
            
            # Restaura el contorno del disco que estaba sujetado (antes de moverlo o anular)
            if self.id_canvas_disco_sujetado:
                try:
                    self.canvas_juego.itemconfig(self.id_canvas_disco_sujetado, outline=self.contorno_disco_defecto, width=1)
                except tk.TclError: pass 

            # Si se hace clic en la misma torre de origen, se anula la selección
            if indice_torre_destino == self.indice_torre_origen: 
                self.etiqueta_estado_modo_manual.config(text=f"Anulada selección de disco {self.valor_disco_sujetado}. Seleccione torre de origen.")
                self._limpiar_estado_movimiento_manual_y_resaltados() 
                return

            # Verifica la regla del juego: ¿se puede colocar el disco sujetado en la torre destino?
            if not self.torres_logicas[indice_torre_destino] or self.valor_disco_sujetado < self.torres_logicas[indice_torre_destino][-1]:
                # Movimiento válido
                valor_disco_a_mover = self.torres_logicas[self.indice_torre_origen].pop() # Quita el disco de la torre origen (lógica)
                # Quita el ID del canvas del disco de la lista de la torre origen
                if self.items_canvas_discos_por_torre[self.indice_torre_origen]:
                    id_canvas_disco_movido = self.items_canvas_discos_por_torre[self.indice_torre_origen].pop()

                self.torres_logicas[indice_torre_destino].append(valor_disco_a_mover) # Añade el disco a la torre destino (lógica)

                self.contador_movimientos_mostrado += 1 # Incrementa el contador de movimientos
                self.etiqueta_movimientos.config(text=f"Movimientos: {self.contador_movimientos_mostrado}")
                
                # Registra el movimiento en el área de texto
                descripcion_movimiento = f"Mover disco {valor_disco_a_mover} de Torre {nombres_torres[self.indice_torre_origen]} a Torre {nombres_torres[indice_torre_destino]} (Manual)"
                if self.area_texto_movimientos.winfo_exists(): # Verifica si el widget aún existe
                    self.area_texto_movimientos.config(state=tk.NORMAL)
                    self.area_texto_movimientos.insert(tk.END, f"{self.contador_movimientos_mostrado}. {descripcion_movimiento}\n")
                    self.area_texto_movimientos.config(state=tk.DISABLED); self.area_texto_movimientos.see(tk.END) # Auto-scroll

                self._limpiar_estado_movimiento_manual_y_resaltados() # Limpia el estado de selección
                self.dibujar_discos() # Redibuja todos los discos para reflejar el movimiento

                # Comprueba si se ha ganado el juego
                n_discos_juego = self.numero_discos_var.get()
                # Se gana si todos los discos están en la última torre (índice 2)
                if len(self.torres_logicas[2]) == n_discos_juego and not self.torres_logicas[0] and not self.torres_logicas[1]:
                    messagebox.showinfo("¡Has Ganado!", f"¡Felicidades! Has resuelto las Torres de Hanói con {n_discos_juego} discos en {self.contador_movimientos_mostrado} movimientos, y su complejidad temporal es: O(2^{n_discos_juego})")
                    self.etiqueta_estado_modo_manual.config(text="¡Juego completado! Reinicia para jugar de nuevo.")
            else: # Movimiento inválido
                # Guarda información para el mensaje antes de limpiar el estado
                valor_disco_sujetado_original = self.valor_disco_sujetado
                nombre_torre_origen_original = "origen" 
                if self.indice_torre_origen is not None and self.indice_torre_origen < len(nombres_torres):
                     nombre_torre_origen_original = nombres_torres[self.indice_torre_origen]
                
                nombre_torre_destino_para_msg = "destino" 
                if indice_torre_destino < len(nombres_torres):
                    nombre_torre_destino_para_msg = nombres_torres[indice_torre_destino]

                self._limpiar_estado_movimiento_manual_y_resaltados() # Limpia el estado (deselecciona el disco)

                # Muestra el mensaje de movimiento inválido en la etiqueta de estado
                self.etiqueta_estado_modo_manual.config(
                    text=f"Movimiento Inválido. Disco {valor_disco_sujetado_original} (de {nombre_torre_origen_original}) no puede ir a {nombre_torre_destino_para_msg}. Disco devuelto y deseleccionado."
                )

    # Inicia la secuencia de resolución automática
    def iniciar_resolucion_automatica(self):
        if self.resolviendo_automaticamente: return # Si ya se está resolviendo, no hacer nada
        self._limpiar_estado_movimiento_manual_y_resaltados() # Limpia cualquier selección manual
        self.reiniciar_juego(self.numero_discos_var.get()) # Reinicia el juego al estado inicial
        self.resolviendo_automaticamente = True # Activa la bandera de resolución
        # Deshabilita botones mientras se resuelve
        for boton in [self.boton_resolver, self.boton_reiniciar, self.boton_ver_arbol_texto, self.boton_ver_arbol_grafico, self.boton_volver_menu]:
            boton.config(state=tk.DISABLED)
        self.etiqueta_estado_modo_manual.config(text="Solución automática en progreso...")
        # Registra el inicio de la solución en el área de texto
        self.area_texto_movimientos.config(state=tk.NORMAL)
        self.area_texto_movimientos.insert(tk.END, f"Iniciando solución automática para {self.numero_discos_var.get()} discos...\n---------------------------------------\n")
        self.area_texto_movimientos.config(state=tk.DISABLED); self.area_texto_movimientos.see(tk.END)
        
        n_discos = self.numero_discos_var.get()
        self.contador_movimientos_interno = 0; self.contador_movimientos_mostrado = 0 # Resetea contadores
        self.etiqueta_movimientos.config(text=f"Movimientos: {self.contador_movimientos_mostrado}")
        
        # Llama a la función recursiva para resolver Hanói
        self.resolver_hanoi_recursivo(n_discos, 0, 2, 1) # Mover n discos de torre 0 a torre 2, usando torre 1 como auxiliar
        
        # Calcula el tiempo total estimado y programa la finalización
        tiempo_total_ms = ((2**n_discos) - 1) * self.velocidad_animacion_ms + self.velocidad_animacion_ms 
        self.master.after(tiempo_total_ms, self.finalizar_resolucion_automatica)

    # Se ejecuta cuando la animación de la solución automática ha terminado
    def finalizar_resolucion_automatica(self):
        if not self.resolviendo_automaticamente: return # Si ya se detuvo, no hacer nada
        self.resolviendo_automaticamente = False # Desactiva la bandera
        # Rehabilita los botones
        for boton in [self.boton_resolver, self.boton_reiniciar, self.boton_ver_arbol_texto, self.boton_ver_arbol_grafico, self.boton_volver_menu]:
            boton.config(state=tk.NORMAL)
        self._limpiar_estado_movimiento_manual_y_resaltados() # Limpia el estado manual
        
        # Registra la finalización en el área de texto
        self.area_texto_movimientos.config(state=tk.NORMAL)
        self.area_texto_movimientos.insert(tk.END, f"---------------------------------------\nSolución automática completada en {self.contador_movimientos_mostrado} movimientos.\n")
        self.area_texto_movimientos.config(state=tk.DISABLED); self.area_texto_movimientos.see(tk.END)
        
        # Muestra un mensaje de completado si la ventana del juego aún existe
        if self.canvas_juego.winfo_exists():
             messagebox.showinfo("Completado", f"Solución para {self.numero_discos_var.get()} discos completada en {self.contador_movimientos_mostrado} movimientos y su complejidad temporal es: O(2^{self.numero_discos_var.get()})")

    # Algoritmo recursivo para resolver las Torres de Hanói
    def resolver_hanoi_recursivo(self, n_discos_en_paso, torre_origen, torre_destino, torre_auxiliar):
        #""//-- la complejidad --//""#
        # La complejidad temporal de este algoritmo es O(2^n), donde n es n_discos_en_paso.
        # Esto se debe a que para resolver el problema para n discos, se hacen dos llamadas recursivas 
        # para n-1 discos, más una operación constante (mover el disco más grande).
        # La relación de recurrencia es T(n) = 2*T(n-1) + 1, que se resuelve a 2^n - 1 movimientos.
        # Cada movimiento (realizar_movimiento_animado) toma un tiempo que, aunque incluye la animación
        # y actualización de la GUI, se considera constante en términos del análisis algorítmico fundamental
        # del número de pasos recursivos.
        # La complejidad espacial es O(n) debido a la profundidad máxima de la pila de llamadas recursivas.
        #""//-- la complejidad --//""#
        if n_discos_en_paso == 0 or not self.resolviendo_automaticamente: return # Caso base o si se detuvo la solución

        # Mover n-1 discos de origen a auxiliar, usando destino como auxiliar
        self.resolver_hanoi_recursivo(n_discos_en_paso - 1, torre_origen, torre_auxiliar, torre_destino)
        
        if not self.resolviendo_automaticamente: return # Comprobar de nuevo si se detuvo
        
        # Programar el movimiento del disco n_discos_en_paso de origen a destino
        retraso_ms = self.contador_movimientos_interno * self.velocidad_animacion_ms
        self.master.after(retraso_ms, lambda f=torre_origen, t=torre_destino: self.realizar_movimiento_animado(f, t))
        self.contador_movimientos_interno += 1 # Incrementa el contador para el siguiente retraso

        # Mover n-1 discos de auxiliar a destino, usando origen como auxiliar
        self.resolver_hanoi_recursivo(n_discos_en_paso - 1, torre_auxiliar, torre_destino, torre_origen)

    # Realiza un movimiento de disco animado (lógica y visualización)
    def realizar_movimiento_animado(self, indice_origen, indice_destino):
        if not self.resolviendo_automaticamente: # Si se detuvo la solución
            # Si el botón de resolver no está normal, significa que la solución fue interrumpida
            if not self.boton_resolver['state'] == tk.NORMAL: self.finalizar_resolucion_automatica() 
            return
        
        # Comprobación de seguridad: no mover de una torre vacía
        if not self.torres_logicas[indice_origen]:
            print(f"Advertencia: Intento de mover desde torre vacía ({indice_origen}) durante animación. Solución detenida.")
            self.finalizar_resolucion_automatica(); return
        
        disco_movido = self.torres_logicas[indice_origen].pop() # Quita el disco de la torre origen (lógica)
        # Quita el ID del canvas del disco (aunque dibujar_discos lo maneja, esto es para consistencia)
        if self.items_canvas_discos_por_torre[indice_origen]:
            self.items_canvas_discos_por_torre[indice_origen].pop()

        # Comprobación de error lógico en el algoritmo (no debería ocurrir)
        if self.torres_logicas[indice_destino] and disco_movido > self.torres_logicas[indice_destino][-1]:
            print(f"Error LÓGICO en algoritmo: Movimiento inválido intentado - disco {disco_movido} sobre {self.torres_logicas[indice_destino][-1]}")
            self.torres_logicas[indice_origen].append(disco_movido); # Revierte el estado lógico
            self.finalizar_resolucion_automatica(); return
        
        self.torres_logicas[indice_destino].append(disco_movido) # Añade el disco a la torre destino (lógica)

        self.contador_movimientos_mostrado += 1 # Incrementa el contador de movimientos
        self.etiqueta_movimientos.config(text=f"Movimientos: {self.contador_movimientos_mostrado}")
        nombres_torres = ['A', 'B', 'C']
        descripcion_movimiento = f"Mover disco {disco_movido} de Torre {nombres_torres[indice_origen]} a Torre {nombres_torres[indice_destino]}"
        # Registra el movimiento en el área de texto
        if self.area_texto_movimientos.winfo_exists():
            self.area_texto_movimientos.config(state=tk.NORMAL)
            self.area_texto_movimientos.insert(tk.END, f"{self.contador_movimientos_mostrado}. {descripcion_movimiento}\n")
            self.area_texto_movimientos.config(state=tk.DISABLED); self.area_texto_movimientos.see(tk.END)
        
        self.dibujar_discos() # Redibuja todos los discos para reflejar el movimiento
        if self.master.winfo_exists(): self.master.update_idletasks() # Actualiza la interfaz

    # Función auxiliar para obtener la etiqueta de texto para el color de un disco
    def obtener_etiqueta_color_disco_texto(self, numero_disco):
        return f"color_disco_{numero_disco}"

    # Genera recursivamente las líneas del árbol de Hanói en formato de texto con etiquetas de color
    def _generar_arbol_hanoi_texto_recursivo(self, n_discos_subproblema, origen, destino, auxiliar, nombres_torres, sangria=""):
        lineas_etiquetadas = []
        # Etiqueta de color para el disco que se mueve en la acción principal de este subproblema
        etiqueta_movimiento_disco_actual = self.obtener_etiqueta_color_disco_texto(n_discos_subproblema)

        if n_discos_subproblema == 1: # Caso base: mover el disco 1 (el más pequeño del subproblema actual)
            etiqueta_disco_1 = self.obtener_etiqueta_color_disco_texto(1) # Siempre es el disco 1 en este contexto
            lineas_etiquetadas.append((f"{sangria}Mover disco 1 de {nombres_torres[origen]} a {nombres_torres[destino]}", etiqueta_disco_1))
            return lineas_etiquetadas
        
        # Subproblema 1: Mover n-1 discos de origen a auxiliar
        lineas_etiquetadas.append((f"{sangria}Subproblema: Mover {n_discos_subproblema-1} discos de {nombres_torres[origen]} a {nombres_torres[auxiliar]} usando {nombres_torres[destino]}:", "subproblema"))
        lineas_etiquetadas.extend(self._generar_arbol_hanoi_texto_recursivo(n_discos_subproblema - 1, origen, auxiliar, destino, nombres_torres, sangria + "  "))
        
        # Acción Principal: Mover el disco n_discos_subproblema de origen a destino
        lineas_etiquetadas.append((f"{sangria}Acción Principal: Mover disco {n_discos_subproblema} de {nombres_torres[origen]} a {nombres_torres[destino]}", etiqueta_movimiento_disco_actual))
        
        # Subproblema 2: Mover n-1 discos de auxiliar a destino
        lineas_etiquetadas.append((f"{sangria}Subproblema: Mover {n_discos_subproblema-1} discos de {nombres_torres[auxiliar]} a {nombres_torres[destino]} usando {nombres_torres[origen]}:", "subproblema"))
        lineas_etiquetadas.extend(self._generar_arbol_hanoi_texto_recursivo(n_discos_subproblema - 1, auxiliar, destino, origen, nombres_torres, sangria + "  "))
        return lineas_etiquetadas

    # Muestra u oculta la ventana con la visualización del árbol de solución en formato de texto
    def alternar_visualizacion_arbol_texto(self): 
        if self.resolviendo_automaticamente:
            messagebox.showinfo("Ocupado", "La solución automática está en curso. Intente después.")
            return
        # Si la ventana ya existe, la cierra
        if self.ventana_arbol_texto and self.ventana_arbol_texto.winfo_exists():
            self.ventana_arbol_texto.destroy(); self.ventana_arbol_texto = None; return

        # Crea una nueva ventana Toplevel
        self.ventana_arbol_texto = Toplevel(self.master)
        n_discos_juego_actual = self.numero_discos_var.get() # Número total de discos en el juego
        self.ventana_arbol_texto.title(f"Árbol de Solución (Texto) para {n_discos_juego_actual} Discos")
        self.ventana_arbol_texto.geometry("700x500") 
        
        area_texto = Text(self.ventana_arbol_texto, wrap=tk.WORD, font=("Courier New", 10))
        barra_despl_y = Scrollbar(self.ventana_arbol_texto, command=area_texto.yview)
        barra_despl_x = Scrollbar(self.ventana_arbol_texto, command=area_texto.xview, orient=tk.HORIZONTAL)
        area_texto.config(yscrollcommand=barra_despl_y.set, xscrollcommand=barra_despl_x.set)
        barra_despl_y.pack(side=tk.RIGHT, fill=tk.Y); barra_despl_x.pack(side=tk.BOTTOM, fill=tk.X)
        area_texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configura las etiquetas de color fijas
        for nombre_etiqueta, color in self.colores_arbol_texto.items():
            area_texto.tag_config(nombre_etiqueta, foreground=color)
            if nombre_etiqueta == "encabezado": 
                 area_texto.tag_config(nombre_etiqueta, font=("Courier New", 10, "bold"))
        
        # Configura dinámicamente las etiquetas de color para cada disco
        for i, color_disco_actual in enumerate(self.colores_discos):
            num_disco = i + 1
            nombre_etiqueta_disco = self.obtener_etiqueta_color_disco_texto(num_disco)
            area_texto.tag_config(nombre_etiqueta_disco, foreground=color_disco_actual, font=("Courier New", 10, "bold"))

        nombres_torres_arbol = ['A', 'B', 'C']
        lineas_encabezado_arbol = [
            (f"Árbol de Recursión (Texto) para {n_discos_juego_actual} Discos", "encabezado"),
            (f"Objetivo: Mover {n_discos_juego_actual} discos de Torre A a Torre C, usando Torre B.", "encabezado"),
            (f"Movimientos totales: {2**n_discos_juego_actual - 1}.", "encabezado"),
            ("---------------------------------------\n", "encabezado")
        ]
        for linea, etiqueta in lineas_encabezado_arbol:
            area_texto.insert(tk.END, linea + "\n", etiqueta)
        
        area_texto.insert(tk.END, "\n") # Espacio después del encabezado

        # Genera e inserta las líneas del árbol con sus respectivas etiquetas de color
        lineas_arbol_con_etiquetas = self._generar_arbol_hanoi_texto_recursivo(n_discos_juego_actual, 0, 2, 1, nombres_torres_arbol)
        for linea, etiqueta in lineas_arbol_con_etiquetas: 
            area_texto.insert(tk.END, linea + "\n", etiqueta)
            
        area_texto.config(state=tk.DISABLED) # Hace el área de texto no editable
        self.ventana_arbol_texto.lift(); self.ventana_arbol_texto.focus_force() # Trae la ventana al frente y le da foco
        self.ventana_arbol_texto.protocol("WM_DELETE_WINDOW", self._al_cerrar_ventana_arbol_texto) # Maneja el cierre de la ventana

    # Callback para cuando se cierra la ventana del árbol de texto
    def _al_cerrar_ventana_arbol_texto(self):
        if self.ventana_arbol_texto:
            self.ventana_arbol_texto.destroy(); self.ventana_arbol_texto = None
            
    # Dibuja recursivamente los nodos y aristas del árbol gráfico
    def _dibujar_nodo_arbol_grafico_recursivo(self, canvas_arbol, n_discos_nodo, x, y, factor_espaciado_horizontal, espaciado_vertical, nivel, profundidad_maxima):
        # n_discos_nodo es el número que se muestra en el nodo, representa el disco movido por la acción principal de este subproblema
        if n_discos_nodo == 0: # No debería ocurrir si se llama correctamente
            return

        radio_nodo = self.radio_nodo_arbol_actual 
        fuente_nodo = self.fuente_nodo_arbol_actual 
        
        color_nodo = self.color_defecto_nodo_arbol_grafico # Color por defecto
        # El número en el nodo (n_discos_nodo) es el tamaño del disco que se mueve en la "Acción Principal" de este nodo
        if 0 < n_discos_nodo <= len(self.colores_discos):
            color_nodo = self.colores_discos[n_discos_nodo - 1] # Usa el color real del disco
        
        color_texto = self.color_texto_nodo_arbol_grafico
        color_linea = self.color_linea_arbol_grafico

        # Dibuja el óvalo del nodo y el texto dentro
        canvas_arbol.create_oval(x - radio_nodo, y - radio_nodo, x + radio_nodo, y + radio_nodo, fill=color_nodo, outline="black")
        canvas_arbol.create_text(x, y, text=str(n_discos_nodo), fill=color_texto, font=fuente_nodo)

        # Si no es una acción final (mover disco 1), tiene hijos
        if n_discos_nodo > 1: 
            y_hijo = y + espaciado_vertical
            # Los hijos manejarán subproblemas de n_discos_nodo - 1 discos
            desplazamiento_x_hijo = (2**(n_discos_nodo - 2)) * factor_espaciado_horizontal if (n_discos_nodo - 2) >=0 else factor_espaciado_horizontal/2
            x_hijo_izquierdo = x - desplazamiento_x_hijo
            x_hijo_derecho = x + desplazamiento_x_hijo

            # Dibuja las líneas a los hijos
            canvas_arbol.create_line(x, y + radio_nodo, x_hijo_izquierdo, y_hijo - radio_nodo, fill=color_linea, width=1) 
            canvas_arbol.create_line(x, y + radio_nodo, x_hijo_derecho, y_hijo - radio_nodo, fill=color_linea, width=1) 
            
            # Llamadas recursivas para los hijos
            self._dibujar_nodo_arbol_grafico_recursivo(canvas_arbol, n_discos_nodo - 1, x_hijo_izquierdo, y_hijo, factor_espaciado_horizontal, espaciado_vertical, nivel + 1, profundidad_maxima)
            self._dibujar_nodo_arbol_grafico_recursivo(canvas_arbol, n_discos_nodo - 1, x_hijo_derecho, y_hijo, factor_espaciado_horizontal, espaciado_vertical, nivel + 1, profundidad_maxima)

    # Muestra u oculta la ventana con la visualización del árbol de solución gráfico
    def alternar_visualizacion_arbol_grafico(self):
        if self.resolviendo_automaticamente:
            messagebox.showinfo("Ocupado", "La solución automática está en curso. Intente después.")
            return

        if self.ventana_arbol_grafico and self.ventana_arbol_grafico.winfo_exists():
            self.ventana_arbol_grafico.destroy(); self.ventana_arbol_grafico = None; return

        self.ventana_arbol_grafico = Toplevel(self.master)
        n_discos_juego_actual = self.numero_discos_var.get() # Número total de discos
        self.ventana_arbol_grafico.title(f"Árbol Gráfico para {n_discos_juego_actual} Discos")
        
        # Parámetros para el dibujo del árbol (ajustados para ser más pequeños)
        self.radio_nodo_arbol_actual = 10  
        self.fuente_nodo_arbol_actual = ("Arial", 8, "bold") 
        desplazamiento_y_inicial = 25           
        espaciado_vertical_entre_niveles = 50 
        expansion_horizontal_nodo_hoja = self.radio_nodo_arbol_actual * 2.2 

        ancho_frame_canvas = 1440
        alto_frame_canvas = 650
        self.ventana_arbol_grafico.geometry(f"{ancho_frame_canvas+1}x{alto_frame_canvas+50}") # Tamaño de la ventana

        etiqueta_info_arbol_graf = ttk.Label(self.ventana_arbol_grafico, 
                                   text=f"Árbol de Recursión para {n_discos_juego_actual} Discos. Altura: {n_discos_juego_actual}, Nodos: {2**n_discos_juego_actual - 1}",
                                   font=("Arial", 10))
        etiqueta_info_arbol_graf.pack(pady=5)

        contenedor_canvas = ttk.Frame(self.ventana_arbol_grafico)
        contenedor_canvas.pack(fill=tk.BOTH, expand=True)
        canvas_arbol_actual = tkCanvas(contenedor_canvas, bg="white") # Canvas para dibujar el árbol
        barra_despl_h = ttk.Scrollbar(contenedor_canvas, orient=tk.HORIZONTAL, command=canvas_arbol_actual.xview)
        barra_despl_v = ttk.Scrollbar(contenedor_canvas, orient=tk.VERTICAL, command=canvas_arbol_actual.yview)
        canvas_arbol_actual.configure(xscrollcommand=barra_despl_h.set, yscrollcommand=barra_despl_v.set)
        barra_despl_h.pack(side=tk.BOTTOM, fill=tk.X); barra_despl_v.pack(side=tk.RIGHT, fill=tk.Y)
        canvas_arbol_actual.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        profundidad_max_arbol = n_discos_juego_actual # La profundidad del árbol es el número total de discos
        
        # Calcula el ancho y alto requeridos para el canvas del árbol
        ancho_requerido_canvas = (2**(profundidad_max_arbol -1)) * expansion_horizontal_nodo_hoja + (2 * self.radio_nodo_arbol_actual) 
        alto_requerido_canvas = desplazamiento_y_inicial + profundidad_max_arbol * espaciado_vertical_entre_niveles + self.radio_nodo_arbol_actual

        # Establece la región de scroll del canvas
        ancho_real_canvas = max(ancho_frame_canvas - 20, ancho_requerido_canvas + 20) # Añade un poco de padding
        alto_real_canvas = max(alto_frame_canvas - 20, alto_requerido_canvas + 20) 
        canvas_arbol_actual.configure(scrollregion=(0, 0, ancho_real_canvas, alto_real_canvas))
        
        x_raiz = ancho_real_canvas / 2 # Posición X de la raíz del árbol
        
        # Llamada inicial para dibujar el árbol (el nodo raíz representa el problema de mover n_discos_juego_actual)
        self._dibujar_nodo_arbol_grafico_recursivo(canvas_arbol_actual, n_discos_juego_actual, 
                                            x_raiz, desplazamiento_y_inicial, 
                                            expansion_horizontal_nodo_hoja, 
                                            espaciado_vertical_entre_niveles, 
                                            0, profundidad_max_arbol)

        self.ventana_arbol_grafico.lift(); self.ventana_arbol_grafico.focus_force()
        self.ventana_arbol_grafico.protocol("WM_DELETE_WINDOW", self._al_cerrar_ventana_arbol_grafico)

    # Callback para cuando se cierra la ventana del árbol gráfico
    def _al_cerrar_ventana_arbol_grafico(self):
        if self.ventana_arbol_grafico:
            self.ventana_arbol_grafico.destroy(); self.ventana_arbol_grafico = None

# Clase controladora principal de la aplicación
