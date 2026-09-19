import { 
  checkBackendHealth, 
  fetchProducts, 
  fetchProductById, 
  checkProductAvailability, 
  sendIntentQuery 
} from './api.js';

import { VoiceEngine, detectLocalIntent } from './voice.js';

// App State
let allProducts = [];
let currentCategory = 'all';
let searchQuery = '';
let inStockOnly = false;
let conversationHistory = [];
let voiceEngine = null;

// DOM Elements
const backendStatusPill = document.getElementById('backend-status-pill');
const backendStatusText = document.getElementById('backend-status-text');

const micBtn = document.getElementById('btn-mic');
const startListenBtn = document.getElementById('btn-start-listen');
const stopListenBtn = document.getElementById('btn-stop-listen');
const testSpeakBtn = document.getElementById('btn-demo-speak');
const voiceStateBadge = document.getElementById('voice-state-badge');
const voiceStatusTitle = document.getElementById('voice-status-title');

const transcriptBox = document.getElementById('transcript-box');
const textQueryInput = document.getElementById('text-query-input');
const textInputForm = document.getElementById('text-input-form');

const agentResponseText = document.getElementById('agent-response-text');
const agentResponseTime = document.getElementById('agent-response-time');
const replayAgentBtn = document.getElementById('btn-replay-agent');
const audioWave = document.getElementById('audio-wave-visualizer');

const historyFeed = document.getElementById('history-feed');
const clearHistoryBtn = document.getElementById('btn-clear-history');

const searchInput = document.getElementById('product-search-input');
const clearSearchBtn = document.getElementById('btn-clear-search');
const inStockCheckbox = document.getElementById('chk-in-stock-only');
const categoryChips = document.querySelectorAll('.category-chip');

const productsGrid = document.getElementById('products-grid');
const recommendationsContainer = document.getElementById('recommendations-container');
const productCountBadge = document.getElementById('product-count-badge');

const quickRecommendBtn = document.getElementById('btn-quick-recommend');

const modal = document.getElementById('product-modal');
const modalContent = document.getElementById('modal-content');
const closeModalBtn = document.getElementById('btn-close-modal');

// Initialize Application
document.addEventListener('DOMContentLoaded', async () => {
  initVoiceEngine();
  setupEventListeners();
  await checkBackendStatus();
  await loadCatalogProducts();
});

// -------------------------------------------------------------------
// 1. BACKEND CONNECTIVITY CHECK
// -------------------------------------------------------------------
async function checkBackendStatus() {
  const status = await checkBackendHealth();
  if (status.online) {
    backendStatusPill.className = 'status-pill online';
    backendStatusText.textContent = 'Backend Online (localhost:8000)';
  } else {
    backendStatusPill.className = 'status-pill offline';
    backendStatusText.textContent = 'Backend Offline (Using Local Fallback)';
  }
}

// -------------------------------------------------------------------
// 2. VOICE ENGINE SETUP
// -------------------------------------------------------------------
function initVoiceEngine() {
  voiceEngine = new VoiceEngine(
    (transcript) => handleVoiceTranscript(transcript),
    (state, detail) => handleVoiceStateChange(state, detail)
  );
}

function handleVoiceStateChange(state, detail) {
  if (state === 'listening') {
    micBtn.classList.add('active');
    voiceStateBadge.className = 'badge badge-listening';
    voiceStateBadge.textContent = 'Listening...';
    voiceStatusTitle.textContent = 'Listening to your voice... Speak now!';
    startListenBtn.disabled = true;
    stopListenBtn.disabled = false;
  } else if (state === 'speaking') {
    voiceStateBadge.className = 'badge badge-speaking';
    voiceStateBadge.textContent = 'Speaking...';
    audioWave.classList.remove('hidden');
  } else {
    micBtn.classList.remove('active');
    voiceStateBadge.className = 'badge badge-idle';
    voiceStateBadge.textContent = 'Ready';
    voiceStatusTitle.textContent = 'Click Microphone to Start Speaking';
    startListenBtn.disabled = false;
    stopListenBtn.disabled = true;
    audioWave.classList.add('hidden');
  }
}

function handleVoiceTranscript(transcript) {
  if (transcript.interim) {
    transcriptBox.innerHTML = `<span class="interim">${transcript.interim}</span>`;
  }
  if (transcript.final) {
    transcriptBox.innerHTML = `<strong>"${transcript.final}"</strong>`;
    processUserQuery(transcript.final);
  }
}

// -------------------------------------------------------------------
// 3. QUERY PROCESSING & INTENT HANDLING
// -------------------------------------------------------------------
async function processUserQuery(queryText) {
  if (!queryText.trim()) return;

  // Add User Message to History
  addHistoryItem('user', queryText);

  // Classify Intent
  const localClassification = detectLocalIntent(queryText);
  let intent = localClassification.intent;

  // Call Backend API Endpoint
  const backendResponse = await sendIntentQuery(intent, queryText);

  let spokenAnswer = "";
  let matchingProducts = [];

  if (backendResponse) {
    spokenAnswer = backendResponse.spoken_response;
    matchingProducts = backendResponse.products || [];
  } else {
    // Fallback response generator
    if (intent === 'greeting') {
      spokenAnswer = "Hello! Welcome to our store. How can I assist you with your shopping today?";
    } else if (intent === 'price_query') {
      const match = allProducts.find(p => p.name.toLowerCase().includes(queryText.toLowerCase()));
      if (match) {
        spokenAnswer = `The ${match.name} costs $${match.price.toFixed(2)}.`;
        matchingProducts = [match];
      } else {
        spokenAnswer = `Here are prices for our top items matching '${queryText}'.`;
        matchingProducts = allProducts.slice(0, 2);
      }
    } else if (intent === 'availability') {
      const match = allProducts.find(p => p.name.toLowerCase().includes(queryText.toLowerCase()));
      if (match) {
        spokenAnswer = match.is_in_stock 
          ? `Yes, ${match.name} is in stock with ${match.stock_quantity} units.` 
          : `Sorry, ${match.name} is currently out of stock.`;
        matchingProducts = [match];
      } else {
        spokenAnswer = `Let me check availability for '${queryText}'. Here is what we found.`;
      }
    } else if (intent === 'product_recommendation') {
      matchingProducts = allProducts.filter(p => p.is_in_stock).slice(0, 3);
      const names = matchingProducts.map(p => p.name).join(" and ");
      spokenAnswer = `I recommend checking out ${names}!`;
    } else {
      matchingProducts = allProducts.filter(p => 
        p.name.toLowerCase().includes(queryText.toLowerCase()) || 
        p.category.toLowerCase().includes(queryText.toLowerCase())
      );
      spokenAnswer = matchingProducts.length > 0 
        ? `Found ${matchingProducts.length} items matching '${queryText}'.` 
        : `I couldn't find exact matches for '${queryText}', but here are popular recommendations.`;
    }
  }

  // Display Agent Response
  agentResponseText.textContent = `"${spokenAnswer}"`;
  agentResponseTime.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  addHistoryItem('agent', spokenAnswer, intent);

  // Speak response aloud via SpeechSynthesis
  voiceEngine.speak(spokenAnswer);

  // Highlight/Filter Products Grid if results returned
  if (matchingProducts.length > 0) {
    renderProducts(matchingProducts);
    productCountBadge.textContent = `${matchingProducts.length} Items (Filtered by Query)`;
  }
}

// -------------------------------------------------------------------
// 4. CATALOG & PRODUCT RENDERING
// -------------------------------------------------------------------
async function loadCatalogProducts() {
  allProducts = await fetchProducts(searchQuery, currentCategory, inStockOnly);
  renderProducts(allProducts);
  renderRecommendations(allProducts);
}

function renderProducts(products) {
  productsGrid.innerHTML = '';
  productCountBadge.textContent = `${products.length} Items`;

  if (products.length === 0) {
    productsGrid.innerHTML = `
      <div class="empty-state" style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--text-muted);">
        <i class="fa-solid fa-box-open" style="font-size: 2.5rem; margin-bottom: 12px;"></i>
        <p>No products found matching your criteria.</p>
      </div>
    `;
    return;
  }

  products.forEach(product => {
    const card = document.createElement('div');
    card.className = 'product-card';
    
    const stockClass = product.stock_quantity > 5 
      ? 'in-stock' 
      : (product.stock_quantity > 0 ? 'low-stock' : 'out-of-stock');
      
    const stockText = product.stock_quantity > 0 
      ? `${product.availability} (${product.stock_quantity})` 
      : 'Out of Stock';

    const featuresList = (product.features || []).slice(0, 3).map(f => `<span class="feature-pill">${f}</span>`).join('');

    card.innerHTML = `
      <div>
        <div class="product-card-top">
          <span class="category-badge">${product.category}</span>
          ${product.discount_percentage > 0 ? `<span class="discount-tag">-${product.discount_percentage}% OFF</span>` : ''}
        </div>
        <h4 class="product-name">${product.name}</h4>
        <p class="product-description">${product.description}</p>
        <div class="features-preview">${featuresList}</div>
      </div>

      <div>
        <div class="product-meta-row">
          <div class="price-container">
            <span class="current-price">$${(product.discounted_price || product.price).toFixed(2)}</span>
            ${product.discount_percentage > 0 ? `<span class="original-price">$${product.price.toFixed(2)}</span>` : ''}
          </div>
          <span class="availability-pill ${stockClass}">${stockText}</span>
        </div>

        <div class="product-actions" style="margin-top: 12px;">
          <button class="btn btn-secondary btn-sm btn-ask-ai" data-id="${product.id}" data-name="${product.name}">
            <i class="fa-solid fa-headset"></i> Ask Agent
          </button>
          <button class="btn btn-outline btn-sm btn-view-details" data-id="${product.id}">
            <i class="fa-solid fa-circle-info"></i> Details
          </button>
        </div>
      </div>
    `;

    productsGrid.appendChild(card);
  });

  // Attach card button listeners
  document.querySelectorAll('.btn-ask-ai').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const pName = e.currentTarget.dataset.name;
      const query = `What is the price and features of ${pName}?`;
      textQueryInput.value = query;
      processUserQuery(query);
    });
  });

  document.querySelectorAll('.btn-view-details').forEach(btn => {
    btn.addEventListener('click', (e) => {
      openProductModal(e.currentTarget.dataset.id);
    });
  });
}

function renderRecommendations(products) {
  recommendationsContainer.innerHTML = '';
  const recommended = products.slice(0, 3);

  recommended.forEach(prod => {
    const card = document.createElement('div');
    card.className = 'product-card';
    card.style.background = 'linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(30, 41, 59, 0.8) 100%)';
    card.style.borderColor = 'rgba(99, 102, 241, 0.3)';

    card.innerHTML = `
      <div>
        <div class="product-card-top">
          <span class="category-badge"><i class="fa-solid fa-star"></i> Featured</span>
          <span class="current-price" style="font-size: 1rem;">$${(prod.discounted_price || prod.price).toFixed(2)}</span>
        </div>
        <h4 class="product-name" style="font-size: 0.95rem;">${prod.name}</h4>
        <p class="product-description" style="font-size: 0.78rem;">${prod.description}</p>
      </div>
      <button class="btn btn-primary btn-sm btn-ask-ai" data-name="${prod.name}" style="margin-top: 8px;">
        <i class="fa-solid fa-microphone"></i> Inquire About This
      </button>
    `;

    recommendationsContainer.appendChild(card);
  });
}

// -------------------------------------------------------------------
// 5. HISTORY & MODAL HELPERS
// -------------------------------------------------------------------
function addHistoryItem(sender, text, intent = '') {
  const item = document.createElement('div');
  item.className = `chat-bubble ${sender}`;
  const badgeHtml = intent ? `<span class="badge badge-idle" style="font-size: 0.65rem; margin-left: 6px;">${intent}</span>` : '';
  item.innerHTML = `<strong>${sender === 'user' ? 'You' : 'AI Agent'}</strong>${badgeHtml}: ${text}`;
  
  historyFeed.prepend(item);
  conversationHistory.push({ sender, text, intent, time: new Date() });
}

async function openProductModal(id) {
  const product = await fetchProductById(id);
  if (!product) return;

  const featuresList = (product.features || []).map(f => `<li><i class="fa-solid fa-check text-gradient"></i> ${f}</li>`).join('');

  modalContent.innerHTML = `
    <span class="category-badge" style="margin-bottom: 8px; display: inline-block;">${product.category}</span>
    <h2 style="font-family: var(--font-heading); font-size: 1.5rem; margin-bottom: 8px;">${product.name}</h2>
    <p style="color: var(--text-muted); font-size: 0.92rem; margin-bottom: 16px;">${product.description}</p>
    
    <div style="background: rgba(15, 23, 42, 0.6); padding: 14px; border-radius: var(--radius-sm); margin-bottom: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <span style="font-weight: 600;">Pricing</span>
        <span class="current-price" style="font-size: 1.3rem;">$${(product.discounted_price || product.price).toFixed(2)}</span>
      </div>
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-weight: 600;">Inventory Status</span>
        <span class="availability-pill ${product.is_in_stock ? 'in-stock' : 'out-of-stock'}">${product.availability} (${product.stock_quantity} in stock)</span>
      </div>
    </div>

    <h4 style="font-size: 0.95rem; margin-bottom: 8px;"><i class="fa-solid fa-list-check"></i> Specifications & Key Features</h4>
    <ul style="list-style: none; display: flex; flex-direction: column; gap: 6px; font-size: 0.88rem; color: #cbd5e1; margin-bottom: 20px;">
      ${featuresList}
    </ul>

    <button class="btn btn-primary" id="btn-modal-ask" style="width: 100%;">
      <i class="fa-solid fa-headset"></i> Ask AI Sales Agent About ${product.name}
    </button>
  `;

  modal.classList.remove('hidden');

  document.getElementById('btn-modal-ask').addEventListener('click', () => {
    modal.classList.add('hidden');
    const q = `Can you give me more details about the ${product.name}?`;
    textQueryInput.value = q;
    processUserQuery(q);
  });
}

// -------------------------------------------------------------------
// 6. EVENT LISTENERS
// -------------------------------------------------------------------
function setupEventListeners() {
  // Mic toggle
  micBtn.addEventListener('click', () => {
    if (voiceEngine.isListening) {
      voiceEngine.stopListening();
    } else {
      voiceEngine.startListening();
    }
  });

  startListenBtn.addEventListener('click', () => voiceEngine.startListening());
  stopListenBtn.addEventListener('click', () => voiceEngine.stopListening());
  
  testSpeakBtn.addEventListener('click', () => {
    const demo = "Hello! I am your AI Voice Sales Agent. All systems are functioning smoothly!";
    agentResponseText.textContent = `"${demo}"`;
    voiceEngine.speak(demo);
  });

  replayAgentBtn.addEventListener('click', () => {
    const text = agentResponseText.textContent.replace(/^"|"$/g, '');
    if (text) voiceEngine.speak(text);
  });

  // Text form submit
  textInputForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const query = textQueryInput.value;
    if (query.trim()) {
      processUserQuery(query);
      textQueryInput.value = '';
    }
  });

  // Search Input
  searchInput.addEventListener('input', (e) => {
    searchQuery = e.target.value;
    clearSearchBtn.classList.toggle('hidden', !searchQuery);
    loadCatalogProducts();
  });

  clearSearchBtn.addEventListener('click', () => {
    searchInput.value = '';
    searchQuery = '';
    clearSearchBtn.classList.add('hidden');
    loadCatalogProducts();
  });

  // In stock checkbox
  inStockCheckbox.addEventListener('change', (e) => {
    inStockOnly = e.target.checked;
    loadCatalogProducts();
  });

  // Category filter chips
  categoryChips.forEach(chip => {
    chip.addEventListener('click', (e) => {
      categoryChips.forEach(c => c.classList.remove('active'));
      e.currentTarget.classList.add('active');
      currentCategory = e.currentTarget.dataset.category;
      loadCatalogProducts();
    });
  });

  // Quick action
  quickRecommendBtn.addEventListener('click', () => {
    processUserQuery("Can you recommend the top products right now?");
  });

  clearHistoryBtn.addEventListener('click', () => {
    historyFeed.innerHTML = '';
    conversationHistory = [];
  });

  // Modal close
  closeModalBtn.addEventListener('click', () => modal.classList.add('hidden'));
  modal.addEventListener('click', (e) => {
    if (e.target === modal) modal.classList.add('hidden');
  });
}
