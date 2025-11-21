import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.models.google_llm import Gemini
from google.genai import types
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from mock_data.sample_data import find_product, get_inventory_status, MOCK_INVENTORY

load_dotenv()

print("🚀 Starting Inventory Agent (Mock)...")

def check_stock_level(product_name: str) -> str:
    """Check current stock levels for a product"""
    product = find_product(product_name)
    
    if not product:
        return f"❌ Product '{product_name}' not found in catalog."
    
    inventory = get_inventory_status(product['id'])
    
    if inventory:
        available_stock = inventory['stock'] - inventory['reserved']    
        
        # Determine status emoji and message
        if inventory['status'] == 'out_of_stock':
            status_emoji = "❌"
            status_msg = "Out of Stock"
        elif inventory['status'] == 'low_stock':
            status_emoji = "⚠️"
            status_msg = "Low Stock"
        else:
            status_emoji = "✅"
            status_msg = "In Stock"
        
        return f"""
{status_emoji} **{product['name']} - Stock Status**
📦 Current Stock: {inventory['stock']} units
🔒 Reserved: {inventory['reserved']} units
🛒 Available: {available_stock} units
📊 Status: {status_msg}
🔄 Reorder Level: {inventory['reorder_level']} units
📅 Next Restock: {inventory['next_restock']}
"""
    else:
        return f"❌ No inventory data found for {product['name']}"

def check_restock_schedule(product_name: str) -> str:
    """Check when a product will be restocked"""
    product = find_product(product_name)
    
    if not product:
        return f"❌ Product '{product_name}' not found."
    
    inventory = get_inventory_status(product['id'])
    
    if inventory:
        return f"""
📦 **{product['name']} - Restock Schedule**
📅 Next Restock: {inventory['next_restock']}
🔄 Reorder Level: {inventory['reorder_level']} units
📊 Current Stock: {inventory['stock']} units
💡 Status: Will reorder when stock drops below {inventory['reorder_level']} units
"""
    else:
        return f"❌ No restock information available for {product['name']}"

def get_low_stock_items() -> str:
    """Get list of items with low stock"""
    low_stock_items = []
    
    for product_id, inventory in MOCK_INVENTORY.items():
        if inventory['status'] in ['low_stock', 'out_of_stock']:
            # Use the find_product function to get product name
            product = None
            for test_name in ["iPhone 15 Pro", "Samsung Galaxy S24", "MacBook Pro 14\"", "Sony WH-1000XM5", "iPad Air"]:
                test_product = find_product(test_name)
                if test_product and test_product['id'] == product_id:
                    product = test_product
                    break
            
            if product:
                low_stock_items.append({
                    'name': product['name'],
                    'current_stock': inventory['stock'],
                    'status': inventory['status'],
                    'next_restock': inventory['next_restock']
                })
    
    if low_stock_items:
        items_text = "\n".join([
            f"  • {item['name']}: {item['current_stock']} units ({item['status'].replace('_', ' ').title()}) - Restock: {item['next_restock']}"
            for item in low_stock_items
        ])
        return f"⚠️ **Low Stock Alert** ⚠️\n\n{items_text}"
    else:
        return "✅ All items have sufficient stock levels."

# Create Inventory Agent
inventory_agent = LlmAgent(
    model=Gemini(
        model="gemini-1.5-flash", 
        api_key=os.environ.get("GOOGLE_API_KEY")
    ),
    name="inventory_agent",
    description="Manages inventory tracking, stock levels, and restocking schedules using mock data.",
    instruction="""
    You are an inventory management specialist using demonstration data.
    
    Your capabilities:
    • Check current stock levels and availability status
    • Provide restocking schedules and dates
    • Identify low stock and out-of-stock items
    
    Stock Status Meanings:
    ✅ In Stock: Plenty available
    ⚠️ Low Stock: Below reorder level
    ❌ Out of Stock: No units available
    
    Always provide clear stock status with emojis for better readability.
    Mention that this is demo inventory data.
    """,
    tools=[check_stock_level, check_restock_schedule, get_low_stock_items]
)

print("✅ Inventory Agent created!")

# Create A2A app
app = to_a2a(inventory_agent, port=8002)
agent = inventory_agent



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)


print("🌐 Inventory A2A server ready on port 8002")