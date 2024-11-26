-- -- Crear usuario para la aplicación
-- CREATE USER IF NOT EXISTS 'gestion_inv_user'@'localhost' IDENTIFIED BY 'clave_app';

-- -- Dar permisos al usuario sobre la base de datos
-- GRANT ALL PRIVILEGES ON gestion_inventario.* TO 'gestion_inv_user'@'localhost';

-- -- Aplicar cambios
-- FLUSH PRIVILEGES;

-- Crear usuario para la aplicación
CREATE USER IF NOT EXISTS 'gestion_inv_user'@'localhost' IDENTIFIED BY 'clave_app';

-- Dar permisos al usuario sobre la base de datos
GRANT ALL PRIVILEGES ON gestion_inventario.* TO 'gestion_inv_user'@'localhost';

-- Aplicar cambios
FLUSH PRIVILEGES;