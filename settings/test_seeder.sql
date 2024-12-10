INSERT INTO users (username, password) VALUES
('user1', 'password123'),
('user2', 'password123'),
('user3', 'password123'),
('user4', 'password123'),
('user5', 'password123'),
('user6', 'password123'),
('user7', 'password123'),
('user8', 'password123'),
('user9', 'password123'),
('user10', 'password123');



INSERT INTO categories (name, descripcion, user_id) VALUES
('Electronics', 'Various electronic items', 1),
('Groceries', 'Daily grocery items', 2),
('Clothing', 'Men and women clothing', 3),
('Books', 'Books and magazines', 4),
('Toys', 'Children toys', 5),
('Furniture', 'Home and office furniture', 6),
('Beauty', 'Beauty and personal care', 7),
('Sports', 'Sports and outdoor items', 8),
('Automotive', 'Automotive parts and accessories', 9),
('Garden', 'Gardening tools and plants', 10);


INSERT INTO products (name, price, category_id, user_id) VALUES
('Laptop', 999.99, 1, 1),
('Smartphone', 699.99, 1, 2),
('Milk', 1.99, 2, 3),
('Bread', 2.49, 2, 4),
('T-Shirt', 19.99, 3, 5),
('Jeans', 49.99, 3, 6),
('Novel', 12.99, 4, 7),
('Magazine', 5.99, 4, 8),
('Action Figure', 15.99, 5, 9),
('Board Game', 29.99, 5, 10);


INSERT INTO stock (product_id, product_name, quantity, user_id) VALUES
(1, 'Laptop', 50, 1),
(2, 'Smartphone', 100, 2),
(3, 'Milk', 200, 3),
(4, 'Bread', 150, 4),
(5, 'T-Shirt', 80, 5),
(6, 'Jeans', 60, 6),
(7, 'Novel', 120, 7),
(8, 'Magazine', 90, 8),
(9, 'Action Figure', 70, 9),
(10, 'Board Game', 40, 10);


INSERT INTO suppliers (name_supplier, phone, mail, user_id) VALUES
('Supplier 1', '1234567890', 'supplier1@example.com', 1),
('Supplier 2', '0987654321', 'supplier2@example.com', 2),
('Supplier 3', '1234509876', 'supplier3@example.com', 3),
('Supplier 4', '0987601234', 'supplier4@example.com', 4),
('Supplier 5', '5678901234', 'supplier5@example.com', 5),
('Supplier 6', '4321098765', 'supplier6@example.com', 6),
('Supplier 7', '9876543210', 'supplier7@example.com', 7),
('Supplier 8', '6789012345', 'supplier8@example.com', 8),
('Supplier 9', '3456789012', 'supplier9@example.com', 9),
('Supplier 10', '8901234567', 'supplier10@example.com', 10);


INSERT INTO suppliers_products (supplier_id, product_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);
