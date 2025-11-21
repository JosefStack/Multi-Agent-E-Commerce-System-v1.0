# Comprehensive mock data for all agents
MOCK_PRODUCTS = {
    "electronics": [
        {
            "id": 1,
            "name": "iPhone 15 Pro",
            "brand": "Apple",
            "price": 999.00,
            "category": "Smartphone",
            "description": "Latest iPhone with Titanium design and A17 Pro chip",
            "specifications": "128GB, 6.1\" Super Retina XDR, 48MP Main camera",
            "features": ["Face ID", "5G", "Ceramic Shield", "Emergency SOS"]
        },
        {
            "id": 2,
            "name": "Samsung Galaxy S24",
            "brand": "Samsung", 
            "price": 799.00,
            "category": "Smartphone",
            "description": "AI-powered smartphone with advanced camera system",
            "specifications": "256GB, 6.2\" Dynamic AMOLED, 50MP Main camera",
            "features": ["AI Photo Assist", "5G", "Gorilla Glass", "Wireless Charging"]
        },
        {
            "id": 3,
            "name": "MacBook Pro 14\"",
            "brand": "Apple",
            "price": 1999.00,
            "category": "Laptop", 
            "description": "Professional laptop for creators and developers",
            "specifications": "M3 Pro, 18GB RAM, 512GB SSD, 14.2\" Liquid Retina XDR",
            "features": ["Touch ID", "Thunderbolt 4", "Magic Keyboard", "Studio Mics"]
        }
    ],
    "audio": [
        {
            "id": 4,
            "name": "Sony WH-1000XM5",
            "brand": "Sony",
            "price": 399.00,
            "category": "Headphones",
            "description": "Industry-leading noise canceling wireless headphones",
            "specifications": "30hr battery, Voice control, Quick charging",
            "features": ["Noise Canceling", "Touch Controls", "Voice Assistant", "Hi-Res Audio"]
        }
    ],
    "tablets": [
        {
            "id": 5, 
            "name": "iPad Air",
            "brand": "Apple",
            "price": 599.00,
            "category": "Tablet",
            "description": "Powerful and versatile tablet for work and creativity",
            "specifications": "M1 chip, 64GB, 10.9\" Liquid Retina, 5G",
            "features": ["Touch ID", "Apple Pencil", "Magic Keyboard", "USB-C"]
        }
    ]
}

MOCK_INVENTORY = {
    1: {"stock": 8, "reserved": 2, "reorder_level": 5, "next_restock": "2024-11-25", "status": "low_stock"},
    2: {"stock": 31, "reserved": 5, "reorder_level": 10, "next_restock": "2024-12-01", "status": "in_stock"},
    3: {"stock": 22, "reserved": 3, "reorder_level": 8, "next_restock": "2024-11-30", "status": "in_stock"},
    4: {"stock": 67, "reserved": 12, "reorder_level": 20, "next_restock": "2024-12-05", "status": "in_stock"},
    5: {"stock": 0, "reserved": 0, "reorder_level": 5, "next_restock": "2024-11-28", "status": "out_of_stock"}
}

MOCK_SHIPPING_OPTIONS = {
    "standard": {"cost": 4.99, "days": 5, "carrier": "USPS", "description": "Economy shipping"},
    "expedited": {"cost": 12.99, "days": 2, "carrier": "FedEx", "description": "Faster delivery"},
    "overnight": {"cost": 24.99, "days": 1, "carrier": "UPS", "description": "Next day delivery"},
    "free": {"cost": 0.00, "days": 7, "carrier": "USPS", "description": "Free standard shipping"}
}

MOCK_TRACKING = {
    "TRK123456789": {
        "status": "delivered", 
        "location": "Customer's doorstep", 
        "timestamp": "2024-11-19 14:30:00",
        "estimated_delivery": "2024-11-19",
        "carrier": "UPS"
    },
    "TRK987654321": {
        "status": "in_transit", 
        "location": "Local distribution center", 
        "timestamp": "2024-11-19 10:15:00",
        "estimated_delivery": "2024-11-21", 
        "carrier": "FedEx"
    },
    "TRK456789123": {
        "status": "processing", 
        "location": "Warehouse", 
        "timestamp": "2024-11-18 16:45:00",
        "estimated_delivery": "2024-11-25",
        "carrier": "USPS"
    }
}

# Helper functions
def find_product(product_name):
    """Find product by name across all categories"""
    product_name_lower = product_name.lower()
    for category in MOCK_PRODUCTS.values():
        for product in category:
            if product_name_lower in product['name'].lower():
                return product
    return None

def search_products(query, category=None):
    """Search products by query and optional category"""
    results = []
    query_lower = query.lower()
    
    for cat_name, products in MOCK_PRODUCTS.items():
        if category and category.lower() != cat_name.lower():
            continue
            
        for product in products:
            if (query_lower in product['name'].lower() or 
                query_lower in product['description'].lower() or
                query_lower in product['brand'].lower()):
                results.append(product)
    
    return results

def get_inventory_status(product_id):
    """Get inventory status for a product"""
    return MOCK_INVENTORY.get(product_id)

def get_shipping_option(method):
    """Get shipping option details"""
    return MOCK_SHIPPING_OPTIONS.get(method.lower())

def track_package(tracking_number):
    """Track a package"""
    return MOCK_TRACKING.get(tracking_number.upper())