const API_BASE_URL = "http://localhost:8000";

// Local fallback dataset if backend connection is unavailable
const FALLBACK_PRODUCTS = [
  {
    id: 1,
    name: "UltraBook Pro 15",
    category: "Laptops",
    price: 1299.99,
    description: "High-performance lightweight laptop with a 15-inch 4K display, Intel Core i7 processor, 16GB RAM, and 512GB SSD.",
    features: ["15-inch 4K UHD Display", "Intel Core i7 13th Gen", "16GB DDR5 RAM", "512GB NVMe SSD", "12-hour battery life"],
    availability: "In Stock",
    stock_quantity: 15,
    discount_percentage: 10.0,
    discounted_price: 1169.99,
    is_in_stock: true
  },
  {
    id: 2,
    name: "SonicWave Wireless Headphones",
    category: "Audio",
    price: 199.99,
    description: "Premium over-ear wireless headphones with active noise cancellation and crystal-clear sound quality.",
    features: ["Active Noise Cancellation", "30-hour battery life", "Bluetooth 5.2", "Built-in HD Microphone"],
    availability: "In Stock",
    stock_quantity: 42,
    discount_percentage: 15.0,
    discounted_price: 169.99,
    is_in_stock: true
  },
  {
    id: 3,
    name: "FitPulse Smartwatch 4",
    category: "Wearables",
    price: 149.50,
    description: "Waterproof fitness smartwatch featuring continuous heart rate monitoring, built-in GPS, and sleep analysis.",
    features: ["50m Water Resistance", "Heart Rate & SpO2 Tracking", "Built-in GPS", "7-day battery life"],
    availability: "In Stock",
    stock_quantity: 28,
    discount_percentage: 0.0,
    discounted_price: 149.50,
    is_in_stock: true
  },
  {
    id: 4,
    name: "Apex 4K Action Camera",
    category: "Cameras",
    price: 299.00,
    description: "Ultra-compact 4K action camera with hyper-smooth image stabilization and dual color screens.",
    features: ["4K Video at 60fps", "Dual LCD Touchscreens", "Waterproof up to 10m", "Wi-Fi transfer"],
    availability: "Low Stock",
    stock_quantity: 3,
    discount_percentage: 5.0,
    discounted_price: 284.05,
    is_in_stock: true
  },
  {
    id: 7,
    name: "SoundBox Portable Speaker",
    category: "Audio",
    price: 79.99,
    description: "Rugged waterproof portable Bluetooth speaker delivering 360-degree immersive sound and deep bass.",
    features: ["IP67 Waterproof", "12 Hours Playtime", "Wireless Stereo Pairing"],
    availability: "Out of Stock",
    stock_quantity: 0,
    discount_percentage: 0.0,
    discounted_price: 79.99,
    is_in_stock: false
  }
];

export async function checkBackendHealth() {
  try {
    const res = await fetch(`${API_BASE_URL}/`, { method: "GET" });
    if (res.ok) {
      const data = await res.json();
      return { online: true, data };
    }
  } catch (err) {
    console.warn("Backend offline or unreachable, using local fallback mode.", err);
  }
  return { online: false };
}

export async function fetchProducts(q = "", category = "", inStockOnly = false) {
  try {
    const params = new URLSearchParams();
    if (q) params.append("q", q);
    if (category && category !== "all") params.append("category", category);
    if (inStockOnly) params.append("in_stock_only", "true");

    const url = `${API_BASE_URL}/api/products/search?${params.toString()}`;
    const res = await fetch(url);
    if (res.ok) {
      return await res.json();
    }
  } catch (err) {
    console.warn("Failed to fetch from backend API, filtering fallback products.", err);
  }

  // Fallback filter
  return FALLBACK_PRODUCTS.filter(p => {
    const matchesQ = !q || p.name.toLowerCase().includes(q.toLowerCase()) || p.description.toLowerCase().includes(q.toLowerCase());
    const matchesCat = !category || category === "all" || p.category.toLowerCase() === category.toLowerCase();
    const matchesStock = !inStockOnly || p.is_in_stock;
    return matchesQ && matchesCat && matchesStock;
  });
}

export async function fetchProductById(id) {
  try {
    const res = await fetch(`${API_BASE_URL}/api/products/${id}`);
    if (res.ok) {
      return await res.json();
    }
  } catch (err) {
    console.warn(`Error fetching product ID ${id}`, err);
  }
  return FALLBACK_PRODUCTS.find(p => p.id === Number(id)) || null;
}

export async function checkProductAvailability(nameOrQuery) {
  try {
    const res = await fetch(`${API_BASE_URL}/api/products/availability/search?name=${encodeURIComponent(nameOrQuery)}`);
    if (res.ok) {
      return await res.json();
    }
  } catch (err) {
    console.warn(`Error checking availability for '${nameOrQuery}'`, err);
  }
  
  const found = FALLBACK_PRODUCTS.find(p => p.name.toLowerCase().includes(nameOrQuery.toLowerCase()));
  if (found) {
    return {
      product_id: found.id,
      name: found.name,
      availability: found.availability,
      stock_quantity: found.stock_quantity,
      is_in_stock: found.is_in_stock,
      status_message: found.is_in_stock 
        ? `'${found.name}' is in stock (${found.stock_quantity} units available).`
        : `'${found.name}' is currently out of stock.`
    };
  }
  return null;
}

export async function sendIntentQuery(intent, query) {
  try {
    const res = await fetch(`${API_BASE_URL}/api/intent-query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ intent, query })
    });
    if (res.ok) {
      return await res.json();
    }
  } catch (err) {
    console.warn("Intent query backend endpoint failed, fallback processing.", err);
  }
  return null;
}
