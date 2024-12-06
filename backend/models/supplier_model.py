from app import db

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key=True)
    name_supplier = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    mail = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, name_supplier, phone, mail, user_id):
        self.name_supplier = name_supplier
        self.phone = phone
        self.mail = mail
        self.user_id = user_id
