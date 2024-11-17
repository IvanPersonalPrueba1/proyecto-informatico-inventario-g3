-- Crear usuario para la aplicación
CREATE USER IF NOT EXISTS 'app_user'@'localhost' IDENTIFIED BY 'secure_password';

-- Dar permisos al usuario sobre la base de datos
GRANT ALL PRIVILEGES ON gestion_inventario.* TO 'app_user'@'localhost';

-- Aplicar cambios
FLUSH PRIVILEGES;
