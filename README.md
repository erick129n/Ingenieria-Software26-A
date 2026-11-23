# Sistema de Gestión de Hotel

Aplicación de escritorio desarrollada en **Python** para la administración básica de un hotel, permitiendo gestionar clientes, habitaciones y reservaciones mediante persistencia en archivos de texto plano.

## Características principales

* **Gestión de Clientes:** Registro y consulta de información de huéspedes.
* **Gestión de Habitaciones:** Control de habitaciones disponibles y sus datos.
* **Gestión de Reservaciones:** Creación y administración de reservas vinculadas a clientes y habitaciones.
* **Persistencia local:** Almacenamiento de datos en archivos `.txt` dentro de la carpeta `Data/`.

## Tecnologías utilizadas

* **Lenguaje:** Python 3.x
* **Interfaz gráfica:** `[Ej. Tkinter / CustomTkinter / Consola]`
* **Almacenamiento:** Archivos de texto plano (`.txt`)

## Estructura del proyecto

```text
src/
├── Data/
│   ├── clientes.txt        # Registro de clientes
│   ├── habitaciones.txt    # Registro de habitaciones
│   └── reservaciones.txt   # Registro de reservaciones
├── App.py                  # Punto de entrada e interfaz principal
├── Archivo.py              # Manejo de lectura y escritura de archivos
├── Cliente.py              # Modelo de datos para Cliente
├── Habitacion.py           # Modelo de datos para Habitación
├── Reservacion.py          # Modelo de datos para Reservación
├── Registro.py             # Módulo auxiliar de registro
└── srcCliente.py           # Lógica adicional de clientes
