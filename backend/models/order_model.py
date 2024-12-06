from backend.models.database import db

class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50), default="pendiente", nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    def __init__(self, user_id, total, status="pendiente"):
        self.user_id = user_id
        self.total = total
        self.status = status

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error saving order: {e}")

    @staticmethod
    def get_all_orders():
        try:
            orders = Order.query.all()
            return [
                {
                    "order_id": order.order_id,
                    "user_id": order.user_id,
                    "total": float(order.total),
                    "status": order.status,
                    "created_at": order.created_at,
                }
                for order in orders
            ]
        except Exception as e:
            print(f"Error fetching orders: {e}")
            return []

