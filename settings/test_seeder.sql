-- Insertar datos iniciales en proveedores
INSERT INTO proveedores (nombre, informacion_contacto, id_usuario) VALUES
('Proveedor Alpha', 'contacto.alpha@example.com', 2),
('Proveedor Beta', 'contacto.beta@example.com', 2),
('Proveedor Gamma', 'contacto.gamma@example.com', 2),
('Proveedor Delta', 'contacto.delta@example.com', 2);

INSERT INTO proveedores_productos (id_proveedor, id_producto) VALUES
(1, 1),  -- Proveedor Alpha suministra Producto A
(2, 2),  -- Proveedor Beta suministra Producto B
(3, 3),  -- Proveedor Gamma suministra Producto C
(4, 4);  -- Proveedor Delta suministra Producto D



-- Insertar datos de prueba en productos
INSERT INTO productos (nombre, precio, categoria_id, id_usuario) VALUES
('Producto A', 100, 1, 2),
('Producto B', 200, 1, 2),
('Producto C', 300, 2, 2),
('Producto D', 400, 2, 2);

-- Insertar datos en la tabla stock
INSERT INTO stock (product_id, quantity, user_id, product_name) VALUES
(1, 100, 1, 'Laptop'),
(2, 200, 1, 'Smartphone'),
(3, 300, 1, 'T-Shirt'),
(4, 150, 1, 'Jeans'),
(5, 80, 1, 'Novel'),
(6, 50, 2, 'Textbook'),
(7, 60, 2, 'Chair'),
(8, 30, 2, 'Desk'),
(9, 40, 1, 'Mouse'),
(10, 70, 1, 'Keyboard');


