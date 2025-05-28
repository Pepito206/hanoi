import subprocess
import sys
import time # Importar time para time.sleep
from subprocess import DEVNULL # Para ocultar la salida de 'pip show'

# Lista de dependencias que se pueden instalar con pip.
DEPENDENCIAS_PIP = [
    "Pillow",  # Para el manejo de imágenes (PIL)
    # "pygame", # Ejemplo: si usaras pygame
    # "numpy",  # Ejemplo: si usaras numpy
]

# Lista de todas las librerías que tu proyecto usa y son gestionadas por pip.
LIBRERIAS_PROYECTO = [
    "Pillow",  # Para el manejo de imágenes (PIL)
    # "pygame",
    # "numpy",
]

def verificar_instalacion(nombre_dependencia):
    """
    Verifica si una dependencia está instalada usando 'pip show'.
    Devuelve True si está instalada, False en caso contrario.
    """
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "show", nombre_dependencia],
            stdout=DEVNULL,
            stderr=DEVNULL
        )
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        print("Error: El comando 'pip' no se encontró. Asegúrate de que Python y pip estén instalados y en el PATH.")
        return False

def instalar_dependencia(nombre_dependencia):
    """
    Verifica si la dependencia ya está instalada y, si no, la instala.
    Devuelve True si la instalación fue exitosa o si ya estaba instalada, False si hubo un error.
    """
    if verificar_instalacion(nombre_dependencia):
        print(f"\nLa dependencia '{nombre_dependencia}' ya está instalada.")
        return True # Ya está instalada, se considera un éxito para este flujo

    try:
        print(f"\nLa dependencia '{nombre_dependencia}' no está instalada. Intentando instalar...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", nombre_dependencia])
        print(f"¡'{nombre_dependencia}' instalada correctamente!")
        return True # Instalación exitosa
    except subprocess.CalledProcessError as e:
        print(f"Error al intentar instalar '{nombre_dependencia}': {e}")
        return False
    except FileNotFoundError:
        print("Error: El comando 'pip' no se encontró. Asegúrate de que Python y pip estén instalados y en el PATH.")
        return False

def mostrar_menu_instalacion():
    """
    Muestra las librerías del proyecto y luego el menú de instalación
    para las dependencias que se gestionan con pip.
    """
    print("\n--- Librerías Requeridas por el Proyecto (gestionadas por pip) ---")
    if not LIBRERIAS_PROYECTO:
        print("No hay librerías especificadas para el proyecto.")
    else:
        for lib in LIBRERIAS_PROYECTO:
            estado_instalacion = "(Instalada)" if verificar_instalacion(lib) else "(No instalada)"
            print(f"- {lib} {estado_instalacion}")
    print("-----------------------------------------------------------------")

    if not DEPENDENCIAS_PIP:
        print("\nNo hay dependencias listadas para instalar con pip.")
        return

    print("\n--- Menú de Instalación de Dependencias (con pip) ---")
    for i, dep in enumerate(DEPENDENCIAS_PIP):
        print(f"{i + 1}. Instalar {dep}")
    # La opción "Instalar TODAS" ha sido eliminada.
    print(f"{len(DEPENDENCIAS_PIP) + 1}. Salir") # La opción Salir ahora es len + 1
    print("----------------------------------------------------")

    while True:
        try:
            opcion = input(f"Selecciona una opción para instalar: ")
            opcion_num = int(opcion)

            if 1 <= opcion_num <= len(DEPENDENCIAS_PIP): # Opción para instalar una dependencia individual
                dependencia_a_instalar = DEPENDENCIAS_PIP[opcion_num - 1]
                instalar_dependencia(dependencia_a_instalar)
                
                print("\nInstalación procesada.")
                time.sleep(2) # Pausa antes de salir
                print("Saliendo del instalador.")
                break # Salir del bucle y del script

            # La opción "Instalar TODAS" (anteriormente len(DEPENDENCIAS_PIP) + 1) ha sido eliminada.
            # Ahora, len(DEPENDENCIAS_PIP) + 1 es la opción para "Salir".
            elif opcion_num == len(DEPENDENCIAS_PIP) + 1: # Salir
                time.sleep(2)
                print("Saliendo del instalador.")
                break
            else:
                print("Opción no válida. Por favor, intenta de nuevo.")
        except ValueError:
            print("Entrada no válida. Por favor, ingresa un número.")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            break

if __name__ == "__main__":
    mostrar_menu_instalacion()
