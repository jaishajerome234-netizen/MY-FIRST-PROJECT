// Add to cart AJAX
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const url = btn.dataset.url;
      const csrf = document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
                   getCookie('csrftoken');
      try {
        btn.disabled = true;
        btn.textContent = '✓ Adding…';
        const res = await fetch(url, {
          method: 'POST',
          headers: { 'X-CSRFToken': csrf, 'X-Requested-With': 'XMLHttpRequest' }
        });
        const data = await res.json();
        if (data.success) {
          document.querySelectorAll('.cart-badge').forEach(b => b.textContent = data.cart_count);
          btn.textContent = '✓ Added!';
          btn.style.background = '#22C55E';
          setTimeout(() => { btn.textContent = '🛒 Add to Cart'; btn.style.background = ''; btn.disabled = false; }, 1500);
          showToast(data.message);
        }
      } catch (err) { btn.disabled = false; btn.textContent = '🛒 Add to Cart'; }
    });
  });
});

function getCookie(name) {
  const v = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
  return v ? v[2] : null;
}

function showToast(msg) {
  const t = document.createElement('div');
  t.className = 'toast';
  t.textContent = msg;
  t.style.cssText = 'position:fixed;bottom:2rem;right:2rem;background:#1A1A2E;color:#fff;padding:.8rem 1.4rem;border-radius:8px;font-weight:600;z-index:9999;box-shadow:0 4px 20px rgba(0,0,0,.2);';
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 2500);
}
