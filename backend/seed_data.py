import json

SAMPLE_PRODUCTS = [
    {
        "id": 1,
        "name": "UltraBook Pro 15",
        "category": "Laptops",
        "price": 1299.99,
        "description": "High-performance lightweight laptop with a 15-inch 4K display, Intel Core i7 processor, 16GB RAM, and 512GB SSD.",
        "features": json.dumps([
            "15-inch 4K UHD Display",
            "Intel Core i7 13th Gen",
            "16GB DDR5 RAM",
            "512GB NVMe SSD",
            "12-hour battery life",
            "Backlit Keyboard"
        ]),
        "availability": "In Stock",
        "stock_quantity": 15,
        "discount_percentage": 10.0
    },
    {
        "id": 2,
        "name": "SonicWave Wireless Headphones",
        "category": "Audio",
        "price": 199.99,
        "description": "Premium over-ear wireless headphones with active noise cancellation and crystal-clear sound quality.",
        "features": json.dumps([
            "Active Noise Cancellation (ANC)",
            "30-hour battery life",
            "Bluetooth 5.2",
            "Built-in HD Microphone",
            "Foldable design with carrying case"
        ]),
        "availability": "In Stock",
        "stock_quantity": 42,
        "discount_percentage": 15.0
    },
    {
        "id": 3,
        "name": "FitPulse Smartwatch 4",
        "category": "Wearables",
        "price": 149.50,
        "description": "Waterproof fitness smartwatch featuring continuous heart rate monitoring, built-in GPS, and sleep analysis.",
        "features": json.dumps([
            "50m Water Resistance (5 ATM)",
            "Heart Rate & SpO2 Tracking",
            "Built-in GPS",
            "7-day battery life",
            "20+ Sports Modes"
        ]),
        "availability": "In Stock",
        "stock_quantity": 28,
        "discount_percentage": 0.0
    },
    {
        "id": 4,
        "name": "Apex 4K Action Camera",
        "category": "Cameras",
        "price": 299.00,
        "description": "Ultra-compact 4K action camera with hyper-smooth image stabilization and dual color screens.",
        "features": json.dumps([
            "4K Ultra HD Video at 60fps",
            "Dual LCD Touchscreens",
            "Waterproof up to 10 meters without case",
            "Electronic Image Stabilization (EIS)",
            "Wi-Fi and Voice Control"
        ]),
        "availability": "Low Stock",
        "stock_quantity": 3,
        "discount_percentage": 5.0
    },
    {
        "id": 5,
        "name": "MechKeys RGB Keyboard",
        "category": "Accessories",
        "price": 89.99,
        "description": "Tactile mechanical gaming keyboard with customizable per-key RGB backlighting and durable aluminum frame.",
        "features": json.dumps([
            "Custom Tactile Mechanical Switches",
            "Per-Key RGB Lighting",
            "Detachable USB-C Cable",
            "Full Anti-Ghosting & N-Key Rollover",
            "Aluminum Top Frame"
        ]),
        "availability": "In Stock",
        "stock_quantity": 50,
        "discount_percentage": 0.0
    },
    {
        "id": 6,
        "name": "AirStride Running Shoes",
        "category": "Footwear",
        "price": 119.95,
        "description": "Lightweight and breathable running shoes designed for long-distance comfort and superior shock absorption.",
        "features": json.dumps([
            "Responsive Cushioned Midsole",
            "Breathable Mesh Upper",
            "High-Traction Rubber Outsole",
            "Reflective Safety Elements",
            "Available in sizes 7 to 12"
        ]),
        "availability": "In Stock",
        "stock_quantity": 20,
        "discount_percentage": 20.0
    },
    {
        "id": 7,
        "name": "SoundBox Portable Speaker",
        "category": "Audio",
        "price": 79.99,
        "description": "Rugged waterproof portable Bluetooth speaker delivering 360-degree immersive sound and deep bass.",
        "features": json.dumps([
            "IP67 Dustproof & Waterproof",
            "12 Hours Continuous Playtime",
            "Wireless Stereo Pairing",
            "Integrated Carrying Loop"
        ]),
        "availability": "Out of Stock",
        "stock_quantity": 0,
        "discount_percentage": 0.0
    },
    {
        "id": 8,
        "name": "LeatherCraft Urban Backpack",
        "category": "Bags",
        "price": 89.00,
        "description": "Stylish genuine leather backpack with dedicated padded laptop compartment and water-resistant lining.",
        "features": json.dumps([
            "100% Genuine Leather",
            "Fits up to 15.6-inch Laptops",
            "Hidden Anti-Theft Back Pocket",
            "Water-Resistant Internal Lining",
            "Ergonomic Padded Shoulder Straps"
        ]),
        "availability": "In Stock",
        "stock_quantity": 12,
        "discount_percentage": 10.0
    },
    {
        "id": 9,
        "name": "TabPro 11 Tablet",
        "category": "Tablets",
        "price": 499.99,
        "description": "11-inch high-resolution tablet with vibrant OLED display, quad speakers, and active stylus pen support.",
        "features": json.dumps([
            "11-inch 120Hz OLED Display",
            "Active Stylus Pen Support",
            "128GB Storage (Expandable)",
            "Quad Dolby Atmos Speakers",
            "10-hour battery life"
        ]),
        "availability": "In Stock",
        "stock_quantity": 8,
        "discount_percentage": 5.0
    },
    {
        "id": 10,
        "name": "ProPhone 15 5G",
        "category": "Smartphones",
        "price": 999.00,
        "description": "Flagship 5G smartphone featuring a pro-grade triple lens camera, all-day battery life, and 6.7-inch AMOLED display.",
        "features": json.dumps([
            "5G Ultra-Wideband Support",
            "6.7-inch 120Hz AMOLED Display",
            "Triple 48MP Camera System",
            "All-Day Intelligent Battery",
            "Fast Wireless Charging"
        ]),
        "availability": "In Stock",
        "stock_quantity": 35,
        "discount_percentage": 0.0
    }
]
