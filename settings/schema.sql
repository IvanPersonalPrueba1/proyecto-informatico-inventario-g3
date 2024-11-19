-- Crear tabla stock
CREATE TABLE stock (
    producto_id INT NOT NULL PRIMARY KEY,
    cantidad INT NOT NULL DEFAULT 0,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
);
