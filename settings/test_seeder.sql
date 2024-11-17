-- Insertar datos iniciales en categorias
INSERT INTO categorias (nombre, descripcion) VALUES
('Electrónica', 'Dispositivos electrónicos y gadgets'),
('Ropa', 'Vestimenta y accesorios');

-- Insertar datos iniciales en productos
INSERT INTO productos (nombre, precio, categoria_id) VALUES
('Smartphone', 699.99, 1),
('Camisa', 29.99, 2);

-- Insertar usuario administrador de prueba
INSERT INTO usuarios (username, password, rol) VALUES
('admin', '12345', 'admin');
