# proyecto-informatico-inventario-g3
<<<<<<< HEAD
Este repositorio contiene el desarrollo del Sistema de Gestión de Inventario para el Grupo 3 de la materia Proyecto Informático 2024. El proyecto está basado en una arquitectura cliente-servidor y tiene como objetivo proporcionar un sistema completo para gestionar productos, stock, proveedores, y órdenes de compra.
=======

Este repositorio contiene el desarrollo del Sistema de Gestión de Inventario para el Grupo 3 de la materia Proyecto Informático 2024. El proyecto está basado en una arquitectura cliente-servidor y tiene como objetivo proporcionar un sistema completo para gestionar productos, stock, proveedores, y órdenes de compra.

## Requisitos

Se requieren los siguientes programas para la ejecución del proyecto:

- [Python 3.x](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- [Xampp](https://www.apachefriends.org/es/download.html)


## Instalación

### 1. Clonar el repositorio

Abrir una terminal y ejecutar el comando:

```bash
git clone https://github.com/IvanPersonalPrueba1/proyecto-informatico-inventario-g3.git
```

### 2. Navegar al directorio backend del proyecto

```bash
cd .\proyecto-informatico-inventario-g3\backend\
```

### 3. Crear un entorno virtual

En **Windows**:

```bash
py -3 -m venv .venv
```

NOTA: Si se produce un error al ejecutar el comando anterior, puede utilizarse alternativamente otra herramienta para la creación del entorno virtual, siguiendo estos pasos:
```bash
# sólo si el comando anterior produce un error
pip install virtualenv
virtualenv .venv
```

En **macOS/Linux**:

```bash
python3 -m venv .venv
```

### 4. Activar el entorno virtual

En **Windows**:

```bash
.venv\Scripts\activate
```

NOTA: Si se produce un error al ejecutar el comando anterior, abrir VSC en modo Administrador y ejecutar el siguiente comando para activar los permisos en Windows:

```bash
# sólo si el comando anterior produce un error
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
.venv\Scripts\activate
```

En **macOS/Linux**:

```bash
source .venv/bin/activate
```

### 5. Instalar las dependencias

Las dependencias necesarias se encuentran en el archivo `requirements.txt` dentro de la carpeta settings:

```bash
pip install -r .\settings\requirements.txt
```

### 6. Inicializar la base de datos (estructura, usuario, datos de prueba)

Los archivos de inicialización de la base de datos se encuentran en la carpeta settings

```
├── settings/
│       └── create_db.sql
│       └── create_user.sql
|       └── schema.sql

```
- `create_db.sql/`: Contiene las sentencias SQL necesarias para la creación de la base de datos.
- `create_user.sql/`: Contiene las sentencias SQL necesarias para la creación de un usuario con acceso a la base de datos.
- `schema.sql/`: Contiene la definición de las tablas necesarias en la base de datos. 

Para realizar la inicialización, se puede copiar el contenido de cada archivo y ejecutarlo directamente en la pestaña SQL de phpMyAdmin (o una herramienta similar que se utilice). Los archivos de creación se deben ejecutar desde la pestaña SQL dentro del servidor, mientras que el archivo de insersión de datos de prueba se debe ejecutar desde la pestaña SQL de la base de datos ya creada.  

Alternativamente, se pueden ejecutar los scripts desde la línea de comandos:

```bash
cd settings
mysql --default-character-set=utf8mb4 -u root -p -e "source create_bd.sql"
mysql --default-character-set=utf8mb4 -u root -p -e "source create_user.sql"
mysql --default-character-set=utf8mb4 -u root -p -e "source schema.sql"
```
Explicación del comando:
- `mysql`: Corresponde al ejecutable mysql.exe. Debe estar configurado correctamente como variable de entorno del sistema, de lo contrario no será reconocido. (Equipo->Propiedades->Configuración Avanzada del Sistema->Variables de entorno, agregar a la variable Path la ruta donde se ubica el archivo, ej: C:\xampp\mysql\bin\mysql.exe).
- `--default-character-set=utf8mb4`: especifica el juego de caracteres (necesario para evitar errores al insertar datos de prueba con caracteres especiales).
- `-u root`: el flag -u indica que a continuación se encuentra el nombre de usuario que debe utilizarse para la operación. En este ejemplo, el usuario es root. 
- `-p`: flag para indicar que el usuario tiene contraseña. Se debe completar luego de ejecutar el comando.
- `-e "source nombre_archivo.sql"`: indica el archivo que se desea ejecutar (ruta relativa al directorio settings).

NOTA: se requiere contar con un usuario `root` para ejecutar correctamente los comandos anteriores.


### 7. Crear un archivo con las variables de entorno

En la carpeta bakend del proyecto, crear un archivo `.env` con el siguiente contenido

```
DB_HOST=localhost          
DB_PORT=3306               
DB_USER=gestion_inv_user   
DB_PASSWORD=clave_app     
DB_NAME=gestion_inventario 
PORT=5000                  
HOST=localhost              

```

La configuración en este archivo debe coincidir con la utilizada para crear la base de datos y el usuario. Los valores del ejemplo son los mismos que se definen en los scripts de inicialización en SQL. Cuando el proyecto se despliegue en un servicio en la nube, se definirán valores específicos para esta configuración y el proyecto ya queda preparado para actualizar dichos valores.

Iniciar la aplicación Xamp, presionar start en los servicios Apache y MySQL


### 8. Ejecutar el proyecto

```bash
python main.py
```

Una vez iniciada la aplicación, acceder desde un navegador a la ruta `http://127.0.0.1:5000/`, y debe observarse la respuesta `{"message": "test ok"}`


## Estructura del Proyecto

```
backend
├── .venv/
├── api/
│   ├── db/
│   │   └── db_config.py  # Configuración de la conexión a la base de datos
│   ├── models/
│   │   ├── categories.py  # Modelo para las categorías de productos
│   │   ├── orders.py      # Modelo para las órdenes de compra
│   │   ├── products.py    # Modelo para los productos
│   │   ├── reports.py     # Modelo para la generación de reportes
│   │   ├── stock.py       # Modelo para el manejo de inventario
│   │   ├── supplier.py    # Modelo para los proveedores
│   │   └── user.py        # Modelo para los usuarios
│   ├── routes/
│   │   ├── categories.py  # Rutas para la gestión de categorías
│   │   ├── orders.py      # Rutas para la gestión de órdenes
│   │   ├── products.py    # Rutas para la gestión de productos
│   │   ├── reports.py     # Rutas para la generación de reportes
│   │   ├── stock.py       # Rutas para el manejo de inventario
│   │   ├── supplier.py    # Rutas para la gestión de proveedores
│   │   └── user.py        # Rutas para la gestión de usuarios
│   ├── utils/
│   │   └── security.py   # Funciones de seguridad y autenticación
│   ├── __init__.py
│   └── settings/
│       ├── create_db.sql     # Script para crear la base de datos
│       ├── create_user.sql   # Script para crear usuarios en la base de datos
│       ├── requirements.txt  # Dependencias del proyecto
│       └── schema.sql        # Definición del esquema de la base de datos     
└── main.py      
```

- `.venv/`: Entorno virtual (esta carpeta está en `.gitignore` y no debe ser incluida en el repositorio).
- `api/`: Carpeta principal del código fuente de la aplicación.
- `db/`: Carpeta de configuración de la conexión a la base de datos. Implementa la función get_db_connection(), que debe importarse en cada archivo que requiera realizar una consulta a la base de datos.
- `models/`: Carpeta de definición de modelos. Habitualmente cada archivo en esta carpeta se nombra de la misma forma que el recurso correspondiente. Implementa una clase con el nombre del recurso, con todas las operaciones asociadas al mismo, incluyendo la interacción con la base de datos.
- `routes/`: Carpeta de definición de rutas. Habitualmente cada archivo en esta carpeta se nombra de la misma forma que el recurso correspondiente. Debe importar el modelo al que hace referencia (y los relacionados, si es necesario). Define las rutas asociadas al recurso e invoca los métodos implementados en la clase asociada. Se utilizan bloques try-except para gestionar las posibles excepciones y evitar que se detenga el servidor.
- `settings/`: Carpeta de configuraciones y archivos de inicialización del proyecto. Puede incluir, por ejemplo, un archivo requirements.txt para la instalación de dependencias de python, archivos de scripts SQL para la inicialización de bases de datos y tablas.
- `__init__.py`:Archivo principal del módulo api. Se encarga de inicializar la aplicación Flask, configurar CORS para permitir solicitudes entre dominios, definir una ruta básica (/) para probar el estado del servidor y registrar las rutas definidas en la carpeta routes/. 
- `main.py`: Archivo de inicio de la aplicación
- `requirements.txt`: Archivo que contiene las dependencias del proyecto.


```
frontend
├── assets/
│   └── video/
│       └── Untitled video - Made with Clipchamp.mp4  # Video utilizado en el proyecto
├── css/
│   ├── styles_general.css   # Estilos generales del proyecto
│   ├── styles_login.css     # Estilos específicos para la página de inicio de sesión
│   └── styles_register.css  # Estilos específicos para la página de registro
├── js/
│   ├── common/
│   │   └── common.js        # Funciones comunes reutilizables en el proyecto
│   └── users/
│       ├── categories.js    # Lógica JavaScript para la gestión de categorías
│       ├── dashboard.js     # Lógica JavaScript para el tablero principal
│       ├── login.js         # Lógica JavaScript para el inicio de sesión
│       ├── orders.js        # Lógica JavaScript para la gestión de órdenes
│       ├── products.js      # Lógica JavaScript para la gestión de productos
│       ├── register.js      # Lógica JavaScript para el registro de usuarios
│       ├── reports.js       # Lógica JavaScript para la generación de reportes
│       ├── stock2.js        # Lógica JavaScript para el manejo de inventarios
│       └── supplier.js      # Lógica JavaScript para la gestión de proveedores
├── public/
│   ├── categories.html      # Página de gestión de categorías
│   ├── dashboard.html       # Página principal del tablero
│   ├── login.html           # Página de inicio de sesión
│   ├── orders.html          # Página de gestión de órdenes
│   ├── products.html        # Página de gestión de productos
│   ├── reports.html         # Página de generación de reportes
│   ├── stock.html           # Página de gestión de inventarios
│   └── supplier.html        # Página de gestión de proveedores
└── register.html             
```

- `assets/video/`: Contiene archivos multimedia que se utilizan en el proyecto.
- `css/`: Carpeta que almacena los archivos CSS del proyecto, organizados según su propósito.
- `common/`: Funciones comunes y reutilizables en múltiples partes del proyecto.
- `users/`: Scripts JavaScript específicos para diferentes funcionalidades.
- `public/`: Carpeta que contiene los archivos HTML accesibles directamente. Cada archivo HTML está asociado con una funcionalidad específica como categorías, productos, inventarios, etc.
- `register.html`: Página de registro de usuarios 
>>>>>>> 2975d8ef325b7e17c037b638ba794de935614a97
