from backend.models.database import db

class Stock(db.Model):
    __tablename__ = 'stock'

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, product_name, quantity, user_id):
        self.product_name = product_name
        self.quantity = quantity
        self.user_id = user_id

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "user_id": self.user_id,
        }

    def update_stock(self, quantity_change):
        """
        Modifica la cantidad de stock del producto. 
        Puede ser positiva (incremento) o negativa (decremento).
        """
        try:
            self.quantity += quantity_change
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error updating stock: {e}")


