# Sistema de Gestión de Hotel

Aplicación de escritorio desarrollada en **Python** para la administración básica de un hotel, permitiendo gestionar clientes, habitaciones y reservaciones mediante persistencia en archivos de texto plano.

## Características principales

* **Gestión de Clientes:** Registro y consulta de información de huéspedes.
* **Gestión de Habitaciones:** Control de habitaciones disponibles y sus datos.
* **Gestión de Reservaciones:** Creación y administración de reservas vinculadas a clientes y habitaciones.
* **Persistencia local:** Almacenamiento de datos en archivos `.txt` dentro de la carpeta `Data/`.
# Ingeniería de Software — Repositorio de Proyectos

Bienvenido al repositorio de **Ingeniería de Software**. Este repositorio agrupa dos sistemas desarrollados en **Python**, diseñados para resolver problemáticas de gestión en distintas áreas de negocio: la administración de reservaciones de un hotel y el control operativo de un taller mecánico.

---

## Contenido del Repositorio

| Proyecto | Descripción | Persistencia / Arquitectura | Punto de Entrada |
| :--- | :--- | :--- | :--- |
| **1. Gestión de Hotel** | Sistema de administración de habitaciones, huéspedes y reservaciones. | Archivos de texto plano (`.txt`) | `src/App.py` |
| **2. Gestión de Taller Mecánico** | Sistema modular para control de usuarios, vehículos, refacciones y órdenes de servicio. | Base de datos relacional + Patrón N-Capas (MVC) | `src2/main.py` |

---

## Proyecto 1: Sistema de Gestión de Hotel

### Descripción
Aplicación enfocada en la administración fundamental de un hotel. Permite gestionar la cartera de clientes, controlar la disponibilidad de habitaciones y procesar las reservaciones de los huéspedes.

### Características Principales
* **Gestión de Clientes:** Registro, modificación y consulta de información de huéspedes.
* **Control de Habitaciones:** Registro de tipos de habitación, precios y disponibilidad.
* **Procesamiento de Reservas:** Asignación de habitaciones a clientes con fechas específicas.
* **Persistencia Local:** Manejo continuo de datos almacenados en formato `.txt`.

### Estructura de Archivos (`src/`)
```text
src/
├── Data/
│   ├── clientes.txt        # Registro local de clientes
│   ├── habitaciones.txt    # Registro local de habitaciones
│   └── reservaciones.txt   # Registro local de reservas
├── App.py                  # Archivo principal / Interfaz
├── Archivo.py              # Módulo de lectura/escritura de archivos
├── Cliente.py              # Clase / Modelo Cliente
├── Habitacion.py           # Clase / Modelo Habitación
├── Reservacion.py          # Clase / Modelo Reservación
├── Registro.py             # Lógica auxiliar de registro
└── srcCliente.py           # Módulo de funciones adicionales
```

---

## Proyecto 2: Sistema de Gestión de Taller Mecánico

### Descripción
Sistema modular de arquitectura robusta por capas (Modelos, Vistas, Persistencia y Utilidades) orientado a la administración completa de un taller automotriz.

### Características Principales
* **Autenticación y Perfiles:** Inicio de sesión (`loggin_window.py`) y roles de usuario.
* **Clientes y Vehículos:** Registro de clientes y vinculación con sus respectivos vehículos.
* **Inventario de Piezas:** Catálogo de refacciones con control de costos y existencias.
* **Órdenes de Reparación:** Gestión de servicios (`repair.py` y `detRepair.py`), asociando mano de obra y piezas.
* **Sistema de Trazabilidad (Logging):** Auditoría y seguimiento de eventos en `utils/logs/app.log`.

### Estructura de Archivos (`src2/`)
```text
src2/
├── databases/              # Capa de Acceso a Datos (CRUD)
│   ├── dbUsuario.py        # Consultas de usuarios
│   ├── db_cliente.py       # Consultas de clientes
│   ├── db_pieza.py         # Consultas de inventario
│   ├── db_repair.py        # Consultas de órdenes de reparación
│   └── db_vehiculo.py      # Consultas de vehículos
├── models/                 # Clases de Dominio (Entidades)
│   ├── cliente.py
│   ├── detRepair.py
│   ├── piece.py
│   ├── repair.py
│   ├── usuario.py
│   └── vehiculo.py
├── utils/                  # Herramientas y Logging
│   ├── base.py
│   ├── logger.py
│   └── logs/app.log
├── views/                  # Interfaz Gráfica de Usuario (GUI)
│   ├── loggin_window.py    # Pantalla de Login
│   ├── main_window.py      # Ventana Principal
│   └── Pages/              # Módulos y vistas individuales
│       ├── client_page.py
│       ├── piece_page.py
│       ├── repair_page.py
│       ├── user_page.py
│       └── vehicle_page.py
└── main.py                 # Punto de entrada principal
```

---

## Instalación y Configuración General

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/Ingenieria-de-Software.git
cd Ingenieria-de-Software
```

### 2. Crear un Entorno Virtual
```bash
# En Windows:
python -m venv venv
venv\Scripts\activate

# En Linux/Mac:
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias (si aplica)
```bash
pip install -r requirements.txt
```

---

## Ejecución de los Proyectos

* **Para ejecutar el Sistema del Hotel:**
  ```bash
  python src/App.py
  ```

* **Para ejecutar el Sistema del Taller Mecánico:**
  ```bash
  python src2/main.py
  ```

---

## Autor

* **Erick Manuel González Carrillo**
