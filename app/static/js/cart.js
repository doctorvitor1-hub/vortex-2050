let cart = JSON.parse(localStorage.getItem('vortex_cart')) || [];

function saveCart() {
  localStorage.setItem('vortex_cart', JSON.stringify(cart));
  renderCart();
}

function toggleCart() {
  document.getElementById('cartDrawer').classList.toggle('open');
  document.getElementById('cartOverlay').classList.toggle('open');
}

function addToCart(id, title, price) {
  const exists = cart.find(item => item.id === id);
  if (!exists) {
    cart.push({ id, title, price });
    saveCart();
  }
  if (!document.getElementById('cartDrawer').classList.contains('open')) {
    toggleCart();
  }
}

function removeFromCart(id) {
  cart = cart.filter(item => item.id !== id);
  saveCart();
}

function renderCart() {
  const container = document.getElementById('cartItems');
  const countBadge = document.getElementById('cartCount');
  const totalEl = document.getElementById('cartTotal');

  countBadge.textContent = cart.length;

  if (cart.length === 0) {
    container.innerHTML = '<p style="color:#94A3B8; text-align:center; margin-top:2rem;">Seu carrinho está vazio.</p>';
    totalEl.textContent = 'R$ 0,00';
    return;
  }

  let total = 0;
  container.innerHTML = cart.map(item => {
    total += item.price;
    return `
      <div class="cart-item">
        <div class="cart-item-info">
          <h4>${item.title}</h4>
          <span>R$ ${item.price.toFixed(2).replace('.', ',')}</span>
        </div>
        <button class="remove-item" onclick="removeFromCart(${item.id})">Remover</button>
      </div>
    `;
  }).join('');

  totalEl.textContent = `R$ ${total.toFixed(2).replace('.', ',')}`;
}

async function proceedToCheckout() {
  if (cart.length === 0) {
    alert('Adicione pelo menos um e-book ao carrinho.');
    return;
  }

  const btn = document.getElementById('checkoutBtn');
  btn.textContent = 'Conectando à Stripe...';
  btn.disabled = true;

  try {
    const response = await fetch('/create-checkout-session', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ items: cart.map(i => i.id) })
    });
    const data = await response.json();
    if (data.url) {
      window.location.href = data.url;
    } else {
      alert(data.error || 'Checkout Stripe será ativado na Fase 4.');
      btn.textContent = 'Finalizar Compra Segura';
      btn.disabled = false;
    }
  } catch (err) {
    alert('Checkout Stripe será ativado na Fase 4!');
    btn.textContent = 'Finalizar Compra Segura';
    btn.disabled = false;
  }
}

document.addEventListener('DOMContentLoaded', renderCart);
