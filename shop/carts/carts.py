from flask import redirect, render_template, url_for, flash, request, session
from shop import db, app 
from shop.products.models import Addproduct
from shop.products.routes import brands,categories



def Merge(dict1,dict2):
    if isinstance(dict1,list) and isinstance(dict2,list):
        return dict1+dict2
    elif isinstance(dict1,dict) and isinstance(dict2,dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False



@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        colors = request.form.get('colors')
        product = Addproduct.query.filter_by(id=product_id).first()
        if product_id and quantity and colors and request.method=='POST':
            DictItems = {
                product_id:{
                    'name': product.name,
                    'price': product.price,
                    'discount': product.discount,
                    'color': colors,
                    'quantity': quantity,
                    'image': product.image1
                }
            }
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    print('this product is in the cart')
                else:
                    session['Shoppingcart'] = Merge( session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)
    



@app.route('/carts')
def getCart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <=0:
        return  redirect(url_for('home'))
    subtotal = 0
    grandtotal = 0
    for key, product in session['Shoppingcart'].items():
        discount = (product['discount']/100) * int(product['quantity'])
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        tax = ("%.2f" %(.06 * float(subtotal)))
        grandtotal = float("%.2f" %(1.06 * subtotal))
    return render_template('products/carts.html',tax=tax ,grandtotal=grandtotal,
                           brands=brands(),categories=categories())





@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <=0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))


@app.route('/clearcart')
def clearcart():
    try:
        session.pop('Shoppingcart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)



# NO ACTUAL LOGIC FOR PAYMENT
@app.route('/buyproducts')
def buyproducts():
    try:
        if 'logged_in' in session:
            session.pop('Shoppingcart', None)
            flash(f'you have bought the product successfully','success')
            return redirect(url_for('home'))
    
        flash(f'please login first','danger')
        return redirect(url_for('home'))

    except Exception as e:
        print(e)