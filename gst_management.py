import json
from flask import Flask, request, jsonify
from datetime import datetime
from decimal import Decimal

class Product:
    def __init__(self, name, price, category, discount=0):
        self.name = name
        self.price = float(price)
        self.category = category
        self.discount = float(discount)

    def apply_discount(self):
        discounted_price = self.price - (self.price * self.discount / 100)
        return discounted_price

    def __str__(self):
        return f"{self.name} ({self.category}) - ₹{self.price} (Discount: {self.discount}%)"

class GSTManagementSystem:
    def __init__(self, gst_rates):
        self.gst_rates = gst_rates
        self.products = []
        self.total_sales = 0

    def add_product(self, name, price, category, discount=0):
        if category not in self.gst_rates:
            return {"error": f"Invalid category: {category}. Please use one of the available categories."}
        new_product = Product(name, price, category, discount)
        self.products.append(new_product)
        return {"message": f"Product '{name}' added successfully."}

    def calculate_gst(self, price, category):
        gst_rate = self.gst_rates.get(category, 0)
        gst = price * (gst_rate / 100)
        return gst

    def generate_invoice(self):
        total_price = 0
        total_gst = 0
        invoice = []
        for product in self.products:
            discounted_price = product.apply_discount()
            gst = self.calculate_gst(discounted_price, product.category)
            total_gst += gst
            total_price += discounted_price + gst
            invoice.append({
                "name": product.name,
                "original_price": product.price,
                "discounted_price": round(discounted_price, 2),
                "gst": round(gst, 2),
                "category": product.category
            })
        self.total_sales += total_price
        return {
            "invoice": invoice,
            "total_gst": round(total_gst, 2),
            "total_amount": round(total_price, 2),
            "total_sales": round(self.total_sales, 2)
        }

    def show_products(self):
        if not self.products:
            return {"error": "No products available."}
        return {"products": [{
            "name": product.name,
            "price": product.price,
            "category": product.category,
            "discount": product.discount
        } for product in self.products]}

    def remove_product(self, name):
        for product in self.products:
            if product.name.lower() == name.lower():
                self.products.remove(product)
                return {"message": f"Product '{name}' removed successfully."}
        return {"error": f"Product '{name}' not found."}

    def search_product(self, name):
        matches = [product for product in self.products if name.lower() in product.name.lower()]
        if matches:
            return {"products": [{
                "name": product.name,
                "price": product.price,
                "category": product.category,
                "discount": product.discount
            } for product in matches]}
        return {"error": f"No products found with name '{name}'."}

app = Flask(__name__)

gst_rates = {
    'Electronics': 18,
    'Clothing': 12,
    'Food': 5,
    'Books': 0,
    'Furniture': 28
}

gst_system = GSTManagementSystem(gst_rates)

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    category = data.get('category')
    discount = data.get('discount', 0)
    if not name or not price or not category:
        return jsonify({"error": "Name, price, and category are required fields."}), 400
    return jsonify(gst_system.add_product(name, price, category, discount))

@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify(gst_system.show_products())

@app.route('/api/products/<string:name>', methods=['DELETE'])
def delete_product(name):
    return jsonify(gst_system.remove_product(name))

@app.route('/api/products/search/<string:name>', methods=['GET'])
def search_product(name):
    return jsonify(gst_system.search_product(name))

@app.route('/api/invoice', methods=['GET'])
def get_invoice():
    return jsonify(gst_system.generate_invoice())

@app.route('/api/sales', methods=['GET'])
def get_total_sales():
    return jsonify({"total_sales": round(gst_system.total_sales, 2)})

if __name__ == '__main__':
    app.run(debug=True)
