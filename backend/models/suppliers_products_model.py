from app import db

class SupplierProduct(db.Model):
    __tablename__ = 'suppliers_products'
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id', ondelete='CASCADE'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), primary_key=True)

    def __init__(self, supplier_id, product_id):
        self.supplier_id = supplier_id
        self.product_id = product_id
