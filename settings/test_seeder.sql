-- Insertar datos iniciales en usuarios
INSERT INTO usuarios (username, password, rol) VALUES
('admin', '12345', 'admin'),
('usuario1', 'password1', 'usuario');

-- Obtener los IDs de los usuarios creados
SET @admin_id = (SELECT id FROM usuarios WHERE username = 'admin');
SET @usuario1_id = (SELECT id FROM usuarios WHERE username = 'usuario1');

-- Insertar datos iniciales en categorías asociadas a usuarios
INSERT INTO categorias (nombre, descripcion, usuario_id) VALUES
('Electrónica', 'Dispositivos electrónicos y gadgets', @admin_id),
('Ropa', 'Vestimenta y accesorios', @usuario1_id);

-- Obtener los IDs de las categorías creadas
SET @categoria_electronica_id = (SELECT id FROM categorias WHERE nombre = 'Electrónica');
SET @categoria_ropa_id = (SELECT id FROM categorias WHERE nombre = 'Ropa');

-- Insertar datos iniciales en productos asociados a usuarios y categorías
INSERT INTO productos (nombre, precio, categoria_id, usuario_id) VALUES
('Smartphone', 699.99, @categoria_electronica_id, @admin_id),
('Camisa', 29.99, @categoria_ropa_id, @usuario1_id);