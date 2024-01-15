from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, DecimalField,StringField, TextAreaField, validators

class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = DecimalField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', [validators.DataRequired()])
    desc = TextAreaField('Description', [validators.DataRequired()])
    colors = TextAreaField('Colors',[validators.DataRequired()])

    image1 = FileField("Image 1", )
    image2 = FileField("Image 2", )
    image3 = FileField("Image 3", )