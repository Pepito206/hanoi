import subprocess
import sys
from subprocess import DEVNULL # Para ocultar la salida de 'pip show'
import time

# Lista de dependencias que se pueden desinstalar con pip.
DEPENDENCIAS_PIP = [
    "Pillow",  # Para el manejo de imágenes (PIL)
    # "pygame", # Ejemplo: si usaras pygame
    # "numpy",  # Ejemplo: si usaras numpy
]

# Lista de todas las librerías que tu proyecto usa.
LIBRERIAS_PROYECTO = [
    "Pillow",  # Para el manejo de imágenes (PIL)
    # "time",   # Ejemplo de módulo estándar
    # "math",   # Ejemplo de módulo estándar
    # "os",     # Ejemplo de módulo estándar
]

def verificar_instalacion(nombre_dependencia):
    """
    Verifica si una dependencia está instalada usando 'pip show'.
    Devuelve True si está instalada, False en caso contrario.
    """
    try:
        # Usamos DEVNULL para que la salida de pip show no se imprima en la consola si el paquete existe.
        # check_call lanzará CalledProcessError si el paquete no se encuentra (retorno no cero).
        subprocess.check_call(
            [sys.executable, "-m", "pip", "show", nombre_dependencia],
            stdout=DEVNULL,
            stderr=DEVNULL
        )
        return True # El paquete está instalado
    except subprocess.CalledProcessError:
        return False # El paquete no está instalado
    except FileNotFoundError:
        # Esto es por si pip no está disponible, aunque es un caso más raro si el script ya funciona.
        print("Error: El comando 'pip' no se encontró. Asegúrate de que Python y pip estén instalados y en el PATH.")
        return False

def desinstalar_dependencia(nombre_dependencia):
    """
    Verifica si la dependencia está instalada y, si es así, la desinstala.
    """
    if not verificar_instalacion(nombre_dependencia):
        print(f"\nLa dependencia '{nombre_dependencia}' no está instalada. No se requiere desinstalación.")
        return False # Indica que no se desinstaló nada o no era necesario

    try:
        print(f"\nLa dependencia '{nombre_dependencia}' está instalada. Intentando desinstalar...")
        # Se usa sys.executable para asegurar que se usa el pip del entorno correcto
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", nombre_dependencia, "-y"])
        print(f"¡'{nombre_dependencia}' desinstalada correctamente!")
        return True # Indica desinstalación exitosa
    except subprocess.CalledProcessError as e:
        # Este error podría ocurrir si 'pip uninstall' falla por alguna razón inesperada
        # (ej. problemas de permisos) aunque el paquete estaba previamente instalado.
        print(f"Error al intentar desinstalar '{nombre_dependencia}': {e}")
        return False
    except FileNotFoundError:
        # Aunque verificar_instalacion ya lo chequearía, es una salvaguarda.
        print("Error: El comando 'pip' no se encontró. Asegúrate de que Python y pip estén instalados y en el PATH.")
        return False

def mostrar_menu_desinstalacion():
    """
    Muestra las librerías del proyecto y luego el menú de desinstalación
    para las dependencias que se gestionan con pip.
    """
    print("\n--- Librerías Usadas por el Proyecto ---")
    if not LIBRERIAS_PROYECTO:
        print("No hay librerías especificadas para el proyecto.")
    else:
        for lib in LIBRERIAS_PROYECTO:
            if lib == "tkinter":
                print(f"- {lib} (Generalmente incluido con Python, no se desinstala con este script)")
            elif lib in DEPENDENCIAS_PIP:
                estado_instalacion = "(Instalada)" if verificar_instalacion(lib) else "(No instalada)"
                print(f"- {lib} (Gestionada por pip) {estado_instalacion}")
            else:
                print(f"- {lib} (Módulo estándar de Python o dependencia indirecta, no se desinstala con este script)")
    print("---------------------------------------")

    if not DEPENDENCIAS_PIP:
        print("\nNo hay dependencias listadas para desinstalar con pip.")
        return

    print("\n--- Menú de Desinstalación de Dependencias (con pip) ---")
    for i, dep in enumerate(DEPENDENCIAS_PIP):
        print(f"{i + 1}. Desinstalar {dep}")
    # Tu código modificado no tenía la opción "Desinstalar todas", así que la mantengo así.
    # Si la quieres de vuelta, me avisas.
    print(f"{len(DEPENDENCIAS_PIP) + 1}. Salir")
    print("-------------------------------------------------------")

    while True:
        try:
            opcion = input(f"Selecciona una opción para desinstalar: ")
            opcion_num = int(opcion)

            if 1 <= opcion_num <= len(DEPENDENCIAS_PIP):
                dependencia_a_desinstalar = DEPENDENCIAS_PIP[opcion_num - 1]
                desinstalar_dependencia(dependencia_a_desinstalar) # La función ahora maneja los mensajes

                # Preguntar si desea realizar otra operación
                while True:
                    continuar_input = 'n'
                    if continuar_input in ['s', 'n']:
                        break
                    print("Respuesta no válida. Ingresa 's' o 'n'.")
                
                if continuar_input == 'n':
                    print("Saliendo del desinstalador.")
                    break
                else: # Si es 's', se vuelve a mostrar el menú completo al inicio del bucle
                    print("\n--- Librerías Usadas por el Proyecto ---") # Re-imprimir para actualizar estado
                    if not LIBRERIAS_PROYECTO:
                        print("No hay librerías especificadas para el proyecto.")
                    else:
                        for lib_loop in LIBRERIAS_PROYECTO:
                            if lib_loop == "tkinter":
                                print(f"- {lib_loop} (Generalmente incluido con Python, no se desinstala con este script)")
                            elif lib_loop in DEPENDENCIAS_PIP:
                                estado_instalacion_loop = "(Instalada)" if verificar_instalacion(lib_loop) else "(No instalada)"
                                print(f"- {lib_loop} (Gestionada por pip) {estado_instalacion_loop}")
                            else:
                                print(f"- {lib_loop} (Módulo estándar de Python o dependencia indirecta, no se desinstala con este script)")
                    print("---------------------------------------")

                    print("\n--- Menú de Desinstalación de Dependencias (con pip) ---")
                    for i_loop, dep_loop in enumerate(DEPENDENCIAS_PIP):
                        print(f"{i_loop + 1}. Desinstalar {dep_loop}")
                    print(f"{len(DEPENDENCIAS_PIP) + 1}. Salir")
                    print("-------------------------------------------------------")
                    continue # Vuelve al inicio del bucle while para pedir nueva opción

            elif opcion_num == len(DEPENDENCIAS_PIP) + 1:
                time.sleep(2)
                print("Saliendo del desinstalador.")
                break
            else:
                print("Opción no válida. Por favor, intenta de nuevo.")
        except ValueError:
            print("Entrada no válida. Por favor, ingresa un número.")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            break

if __name__ == "__main__":
    mostrar_menu_desinstalacion()
