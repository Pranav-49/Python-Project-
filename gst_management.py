class Product:
    def __init__(self, name, price, category, discount=0):
        self.name = name
        self.price = price
        self.category = category
        self.discount = discount

    def apply_discount(self):
        discounted_price = self.price - (self.price * self.discount / 100)
        return discounted_price

    def __str__(self):
        return f"{self.name} ({self.category}) - ₹{self.price} (Discount: {self.discount}%)"

class GSTManagementSystem:
    def __init__(self, gst_rates):
        self.gst_rates = gst_rates  # gst_rates is a dictionary with categories and their respective GST rates
        self.products = []
        self.total_sales = 0

    def add_product(self, name, price, category, discount=0):
        if category not in self.gst_rates:
            print(f"Invalid category: {category}. Please use one of the available categories.")
            return
        new_product = Product(name, price, category, discount)
        self.products.append(new_product)
        print(f"Product '{name}' added successfully.")

    def calculate_gst(self, price, category):
        gst_rate = self.gst_rates.get(category, 0)
        gst = price * (gst_rate / 100)
        return gst

    def generate_invoice(self):
        total_price = 0
        total_gst = 0
        print("\nInvoice:")
        print("-" * 50)
        for product in self.products:
            discounted_price = product.apply_discount()
            gst = self.calculate_gst(discounted_price, product.category)
            total_gst += gst
            total_price += discounted_price + gst
            print(f"{product.name} - ₹{product.price} (Discounted: ₹{discounted_price}) + GST: ₹{gst:.2f}")
        
        print("-" * 50)
        print(f"Total GST: ₹{total_gst:.2f}")
        print(f"Total Amount (Including GST): ₹{total_price:.2f}")
        self.total_sales += total_price
        print(f"Total Sales (Including GST): ₹{self.total_sales:.2f}")
        print("-" * 50)

    def show_products(self):
        if not self.products:
            print("No products available.")
        else:
            print("Available Products:")
            for product in self.products:
                print(product)

    def remove_product(self, name):
        found = False
        for product in self.products:
            if product.name.lower() == name.lower():
                self.products.remove(product)
                print(f"Product '{name}' removed successfully.")
                found = True
                break
        if not found:
            print(f"Product '{name}' not found.")

    def search_product(self, name):
        found = False
        for product in self.products:
            if name.lower() in product.name.lower():
                print(f"Found: {product}")
                found = True
        if not found:
            print(f"No products found with name '{name}'.")

def main():
    print("Welcome to the GST Management System")
    
    # GST rates for different categories (in %)
    gst_rates = {
        'Electronics': 18,
        'Clothing': 12,
        'Food': 5,
        'Books': 0,
        'Furniture': 28
    }

    gst_system = GSTManagementSystem(gst_rates)

    while True:
        print("\n1. Add Product")
        print("2. Show Products")
        print("3. Generate Invoice")
        print("4. Remove Product")
        print("5. Search Product")
        print("6. Show Total Sales")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter product name: ")
            price = float(input("Enter product price: ₹"))
            category = input("Enter product category (Electronics, Clothing, Food, Books, Furniture): ")
            discount = float(input("Enter discount on product (0% for no discount): "))
            gst_system.add_product(name, price, category, discount)

        elif choice == '2':
            gst_system.show_products()

        elif choice == '3':
            gst_system.generate_invoice()

        elif choice == '4':
            name = input("Enter product name to remove: ")
            gst_system.remove_product(name)

        elif choice == '5':
            name = input("Enter product name to search: ")
            gst_system.search_product(name)

        elif choice == '6':
            print(f"Total Sales (Including GST): ₹{gst_system.total_sales:.2f}")

        elif choice == '7':
            print("Exiting the system.")
            break

        else:
            print("Invalid choice! Please enter a valid option.")

if __name__ == "__main__":
    main()
