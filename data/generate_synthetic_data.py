
import random

# Define categories for pricing
PRODUCT_CATEGORIES = {

    "Vegetable": (10, 50),
    "Spices": (50, 150),
    "Processed Food": (100, 500),
    "Fruits": (30, 100),
    "Grains": (20, 80)
}

def generate_synthetic_data(products, category=None):
    # If no category is specified, assign a random category
    if not category:
        category = random.choice(list(PRODUCT_CATEGORIES.keys()))
    
    price_range = PRODUCT_CATEGORIES.get(category, (50, 500))
    product_prices = {product: random.uniform(price_range[0], price_range[1]) for product in products}
    return product_prices

