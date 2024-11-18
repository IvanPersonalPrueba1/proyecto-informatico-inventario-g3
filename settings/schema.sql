-- Crear tabla stock
CREATE TABLE stock (
    id INT AUTO_INCREMENT PRIMARY KEY,    
    producto_id INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 0,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
);
