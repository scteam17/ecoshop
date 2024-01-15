from flask import redirect, render_template, url_for, flash, request, session
from shop import db, app , search
from .models import Brand, Category ,Addproduct
from .forms import Addproducts




def brands():
    brands = Brand.query.join(Addproduct,(Brand.id ==Addproduct.brand_id)).all()
    return brands

def categories():
    categories = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    return categories


@app.route('/')
def home():
    page = request.args.get('page',1,type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).paginate(page=page,per_page=8)
    return render_template('products/index.html', products=products, brands=brands(),categories=categories())


#search
@app.route('/result')
def result():
    searchword = request.args.get('q')
    products = Addproduct.query.msearch(searchword, fields=['name','desc'], limit=3)
    return render_template('products/result.html',products=products)

@app.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)
    return render_template('/products/single_page.html',product=product,brands=brands(),categories=categories())


#the drop down in nav bar for brands
@app.route('/brands/<int:id>')
def get_brand():
    get_d = Brand.query.filter_by(id=id).first_or_404()
    page = request.args.get('page',1,type=int)
    brand = Addproduct.query.filter_by(brand=get_d).paginate(page=page,per_page=12)
    
    return render_template('products/index.html',brand=brand,categories=categories(),brands=brands(),get_d=get_d)

#the drop down for nav bar for categories
@app.route('/categories/<int:id>')
def get_category(id):
    page = request.args.get('page',1,type=int)
    get_cat = Category.query.filter_by(id=id).first_of_404()
    get_cat_prod = Addproduct.query.filtr_by(category=get_cat).paginate(page=page,per_page=12)
    return render_template('products/index.html', get_cat_prod=get_cat_prod, categories=categories(),brands=brands(),get_cat=get_cat)

# Add Brand
@app.route('/addbrand', methods=['Get','Post'])
def addbrand():
    if request.method=='POST':
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The Brand {getbrand} was added to your database', 'sucessess')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', brands='brands')


#----------------------------------------
# Add Category
@app.route('/addcategory', methods=['Get','Post'])
def addcategory():
    if request.method=='POST':
        getcategory = request.form.get('category')
        category = Category(name=getcategory)
        db.session.add(category)
        flash(f'The Brand {getcategory} was added to your database', 'sucessess')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html')



@app.route('/updatebrand/<int:id>', methods=['GET','POST'])
def updatebrand(id):
    if 'email' not in session:
       flash("Please login first", 'danger')
       return redirect(url_for('login'))
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method=='POST':
        updatebrand.name = brand
        flash(f'Your brand has been updated','success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html', title="Update brand page",updatebrand=updatebrand)


@app.route('/updatecat/<int:id>', methods=['GET','POST'])
def updatecategory(id):
    if 'email' not in session:
       flash("Please login first", 'danger')
       return redirect(url_for('login'))
    updatecategory = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method=='POST':
        updatecategory.name = category
        flash(f'Your category has been updated','success')
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template('products/updatebrand.html', title="Update catagory page",updatecategory = updatecategory)




#_______________________________________________M___________________________________
@app.route('/addproduct', methods=['POST','GET'])
def addproduct():
    if 'email' not in session:
        flash("Please login first", 'danger')
        return redirect(url_for('login'))
    
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method=='POST':
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.desc.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        

        addpro = Addproduct(name=name, 
                             price=price, 
                             discount=discount, 
                             stock=stock,
                             colors=colors,
                             desc=desc,
                             brand_id=brand,
                             category_id=category,
                             image1=None,
                             image2=None,
                             image3=None) 
        db.session.add(addpro)
        flash(f'The product {name} has been added to your database','success')
        db.session.commit()

        return redirect(url_for('admin'))
    

    return render_template('products/addproduct.html', 
                           title='Add product page', form=form,
                           brands=brands, categories=categories)



@app.route('/updateproducts/<int:id>',methods=['GET','POST'])
def updateproduct(id):
    form = Addproducts(request.form)
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')
    form = Addproducts(request.form)
    if request.method == 'POST':
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.brand_id = brand
        product.category_id = category
        product.colors = form.colors.data
        product.desc = form.desc.data
        db.session.commit()
        flash(f'You product has been updated','success')
        return redirect('admin')

    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.desc.data = product.desc



    return render_template('products/updateproduct.html', form=form,
                           brands=brands,
                           categores=categories,
                           product=product)



@app.route('/deletebrand/<int:id>',methods=['POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method=='POST':
        db.session.delete(brand)
        db.session.commit()
        flash(f'The brand {brand.name} was deleted from your database', 'success')
        return redirect(url_for('brands'))
    flash(f'The brand {brand.name} cant be deleted')
    return redirect(url_for('admin'))



@app.route('/deletecategory/<int:id>',methods=['POST'])
def deletecategory(id):
    category = Category.query.get_or_404(id)
    if request.method=='POST':
        db.session.delete(category)
        db.session.commit()
        flash(f'The category {category.name} was deleted from your database', 'success')
        return redirect(url_for('categories'))
    flash(f'The category {category.name} cant be deleted')
    return redirect(url_for('admin'))


@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method=='POST':
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} was deleted from your record', 'success')
        return redirect(url_for('admin'))
    flash(f"Can't delete the product ",'danger')
    return redirect(url_for('admin'))

