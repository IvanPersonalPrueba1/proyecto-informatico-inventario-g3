-- Insertar usuarios
INSERT INTO users (username, password) VALUES 
('user1', '123'),
('user2', '123');

-- Insertar categorías
INSERT INTO categories (name, descripcion, user_id) VALUES 
('Electronics', 'Devices and gadgets', 1),
('Furniture', 'Household items', 1),
('Books', 'Various kinds of books', 2),
('Clothing', 'Apparel and accessories', 2);

-- Insertar productos
INSERT INTO products (name, price, category_id, user_id) VALUES 
('Smartphone', 699.99, 1, 1),
('Table', 150.00, 2, 1),
('Novel', 20.50, 3, 2),
('T-shirt', 15.00, 4, 2);

-- Insertar stock
INSERT INTO stock (product_id, quantity, user_id) VALUES 
(1, 50, 1),
(2, 10, 1),
(3, 30, 2),
(4, 100, 2);

-- Insertar proveedores
INSERT INTO suppliers (name_supplier, phone, mail, user_id) VALUES 
('Tech Supplier', '123-456-7890', 'tech@supplier.com', 1),
('Furniture Co.', '234-567-8901', 'info@furniture.com', 1),
('Book World', '345-678-9012', 'support@bookworld.com', 2),
('Fashion Hub', '456-789-0123', 'contact@fashionhub.com', 2);

-- Insertar productos-proveedores
INSERT INTO suppliers_products (supplier_id, product_id, user_id) VALUES 
(1, 1, 1),
(2, 2, 1),
(3, 3, 2),
(4, 4, 2);

-- Insertar órdenes de compra
INSERT INTO purchase_orders (order_date, received_date, status, user_id) VALUES 
('2024-12-01', '2024-12-05', 'completed', 1),
('2024-12-02', NULL, 'pending', 1),
('2024-12-03', '2024-12-07', 'completed', 2),
('2024-12-04', NULL, 'pending', 2);

-- Insertar productos en órdenes
INSERT INTO order_products (order_id, product_id, quantity) VALUES 
(1, 1, 10),
(1, 2, 5),
(3, 3, 7),
(4, 4, 12);
