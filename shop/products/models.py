from shop import db, app
from datetime import datetime


class Addproduct(db.Model):
    __searchable__ = ['name', 'desc']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    discount = db.Column(db.Integer,default=0)
    stock = db.Column(db.Integer, nullable=False)
    colors = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'),
        nullable=False)
    brand = db.relationship('Brand',
        backref=db.backref('brands', lazy=True))

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
        nullable=False)
    category = db.relationship('Category',
        backref=db.backref('posts', lazy=True))

    # TODO: CHANGE THE IMAGE NULLABLE TO FALSE
    image1 = db.Column(db.String(150), nullable=True, default='image.jpg')
    image2 = db.Column(db.String(150), nullable=True, default='image.jpg')
    image3 = db.Column(db.String(150), nullable=True, default='image.jpg')



    def __repr__(self):
        return '<Addproduct %r>' % self.name




class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    

with app.app_context():
    db.create_all()