# Torres de Hanói

- Instalacion (#Instalación)

# Instalación
Primero, instalar las dependencias, ya sea manual o de forma automática desde el archivo `instalar_dependencias.py`.

- Forma manual:
Abrimos la terminal (Ctrl + J) y ejecutamos el siguiente comando:
`*"pip install Pillow"*`

- Forma del programa:
Ejecutamos el archivo `instalar_dependencias.py`.
Después de ejecutar, en la terminal, si no tenemos descargado Pillow, seleccionamos la opción 1.

![image](https://github.com/user-attachments/assets/4696919e-423c-478a-880c-c430a8fdb92e)

Después, pulsamos Enter y se nos ejecutará automáticamente la descarga de la librería.

![image](https://github.com/user-attachments/assets/21a5cba1-181e-4b62-aade-12068f67b39d)

- Después, vamos a ejecutar el `__main__.py` y se nos abrirá una interfaz.

![image](https://github.com/user-attachments/assets/a2cf6ce9-30f8-435c-a777-3387ce5d4aa1)

# Reglas
Donde podemos elegir los discos que queramos y empezar a jugar.
En la parte inferior central de la pantalla se nos mostrarán las reglas, las cuales son:
1) Pasar los discos de la torre A a la torre C.
2) No podemos colocar un disco grande sobre un disco pequeño.
3) Al hacer clic en una torre, se elige el disco de arriba, resaltado con un borde amarillo, y las torres con unos colores específicos:
    - Azul: deselecciona el disco.
    - Verde: el movimiento es válido.
    - Rojo: no se puede realizar el movimiento.

# Interfaz
A la hora de iniciar el juego, se muestra la siguiente interfaz, la cual aparece de la siguiente forma:

![image](https://github.com/user-attachments/assets/99cbfdeb-3696-4a08-9d95-44c3e0fe71b3)

Podemos mover los discos de una torre a otra siguiendo las reglas, mostrándonos la secuencia de movimientos.

![image](https://github.com/user-attachments/assets/f2b06107-ddd1-4b07-aec9-e155c3797b8a)

Luego, tenemos unos botones que tienen diferente función:

![image](https://github.com/user-attachments/assets/d9991811-39ac-4fad-ab87-252ffa1b8ff2)

# Funcionalidad
*(Nota: Se ha corregido la numeración de esta lista para que sea secuencial)*
1) Resolver automáticamente
Según la velocidad de cada movimiento, se resolverá de forma automática en el menor número de movimientos posible.
Entre menos velocidad, la máquina resuelve más rápido el juego.

![image](https://github.com/user-attachments/assets/3a47343a-4352-4aa9-a3fe-1c4307a7725d)
![image](https://github.com/user-attachments/assets/dbea87ef-5f1a-48db-90c0-f8345ec71334)

2) Reinicio de juego
Reinicia el juego que estaba por defecto.

![image](https://github.com/user-attachments/assets/96ff0fac-7716-4bc7-9e99-dc008afd5964)

3) Árbol (formato texto)
Muestra una solución paso a paso de cómo realizar el juego en la menor cantidad de movimientos.

![image](https://github.com/user-attachments/assets/de5a3f70-d131-4dd8-8b19-e80b2af1d0e9)

Esto se abre en pantalla emergente, por lo que se puede agrandar, minimizar e incluso salir de la pantalla emergente y no se cierra el juego.

4) Árbol (formato grafo)
Nos muestra un grafo según el color y sus posibles movimientos.

![image](https://github.com/user-attachments/assets/c7d89321-376a-4f05-b802-d1a66ed79ed3)

Esto se abre en pantalla emergente, por lo que se puede agrandar, minimizar e incluso salir de la pantalla emergente y no se cierra el juego.

5) Menú principal
Si queremos devolvernos al menú principal, podemos tocar el botón o la tecla (ESC).

![image](https://github.com/user-attachments/assets/c1630007-4de2-48cf-bbdd-38a7bb18a61e)

Donde podemos volver a elegir la cantidad de discos.

![image](https://github.com/user-attachments/assets/88aeed44-388a-4252-a5de-bd9b10d0cbd8)

- A la hora de completar el juego, nos muestra en una pantalla emergente los discos, cantidad de movimientos y su complejidad algorítmica.

![image](https://github.com/user-attachments/assets/d3dcee44-d56d-4507-9706-85ecbcea12f2)

# Notas:
Al cerrar la aplicación principal, también se cerrarán todas las pestañas o ventanas emergentes.

![image](https://github.com/user-attachments/assets/135771bd-87fd-47c7-947a-86e689e94960)
![image](https://github.com/user-attachments/assets/41055cbe-3ea0-4d5c-88c3-b4d72c57e378)

# Para eliminar la librería
Si deseamos eliminar la librería, ingresamos al archivo `desinstalar_dependencias.py` y lo ejecutamos.

![image](https://github.com/user-attachments/assets/f36074ca-ef0b-4821-8154-6c1ccbc07e76)

Nos mostrará el estado de la librería (Instalada o No instalada).

![image](https://github.com/user-attachments/assets/35336d35-39b0-4e2c-8473-1f2918152489)

Seleccionamos la opción 1 si queremos eliminar la librería.

![image](https://github.com/user-attachments/assets/8fc84b6e-ee0b-4a37-83e8-951146617f20)

# Errores
Pueden llegar a ocurrir errores; los más comunes son las librerías repetidas o desinstalar algo que no está instalado.

![image](https://github.com/user-attachments/assets/a4ef2290-f213-4678-82b8-4783fdd3a257)

Hay otros códigos de error registrados por Inteligencia Artificial que al momento no han ocurrido, por lo que no hay guía de cómo solucionarlos.

# Fin
Esto sería el manual de usuario.

Integrantes:
- Héctor Alejandro Garcés
- Luis Alejandro Martínez
- Juan Daniel Bravo








