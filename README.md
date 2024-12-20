# proyecto-informatico-inventario-g3
Este repositorio contiene el desarrollo del Sistema de Gestión de Inventario para el Grupo 3 de la materia Proyecto Informático 2024. El proyecto está basado en una arquitectura cliente-servidor y tiene como objetivo proporcionar un sistema completo para gestionar productos, stock, proveedores, y órdenes de compra.

clonar repositorio

creamos la base de datos, utilizando los comandos dentro de la carpeta SETTINGS
1. create_db
2. create_user
3. schema

es muy importante que los datos conincidan con las variables globales del archivo ".env"

iniciamos xampp


---


crearmos entorno virtual python

"comando python entorno virtual"

crear archivo ".env" en la carpeta backend con las variables globales, ejemplo
"""
    DB_HOST=localhost          
    DB_PORT=3306               
    DB_USER=gestion_inv_user   
    DB_PASSWORD=clave_app     
    DB_NAME=gestion_inventario 
    PORT=5000                  
    HOST=localhost
"""
activamos entorno virtual

.\.venv\Scripts\activate

instalamos requerimientos

pip install -r .\settings\requirements.txt

corremos archivo main, en la carpeta backend

python main.py

---

