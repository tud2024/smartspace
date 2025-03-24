@app.route('/category/<int:category_id>/product/<int:product_id>')
def product_page(category_id, product_id):
    category = Category.query.get(category_id)
    product = Product.query.get(product_id)
    return render_template('index.html', category=category, product=product)

