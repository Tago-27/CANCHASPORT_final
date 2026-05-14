// ═══════════════════════════════════════════
//  CanchasSport — main.js
// ═══════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
  initScrollAnimations();
  initNavbar();
  initMessages();
  initCounters();
  initCardHover();
  initFormAnimations();
  initPageTransition();
});

// ── 1. SCROLL ANIMATIONS (Intersection Observer) ──
function initScrollAnimations() {
  const targets = document.querySelectorAll(
    '.cancha-card, .stat-card, .resumen-card, .reserva-item, .auth-card, .admin-section'
  );
  targets.forEach(el => el.classList.add('fade-up'));

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.classList.add('visible');
        }, i * 80);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  targets.forEach(el => observer.observe(el));
}

// ── 2. NAVBAR scroll effect ──
function initNavbar() {
  const nav = document.querySelector('.navbar');
  if (!nav) return;
  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 40);
  }, { passive: true });
}

// ── 3. AUTO-DISMISS messages ──
function initMessages() {
  document.querySelectorAll('.message').forEach((msg, i) => {
    setTimeout(() => msg.classList.add('hiding'), 4000 + i * 300);
    setTimeout(() => msg.remove(), 4600 + i * 300);
  });
}

// ── 4. COUNTER animation (stats bar) ──
function initCounters() {
  document.querySelectorAll('.stat-num, .stat-number').forEach(el => {
    const raw = el.textContent.trim();
    const num = parseFloat(raw.replace(/[^0-9.]/g, ''));
    const suffix = raw.replace(/[0-9.]/g, '');
    if (isNaN(num) || num === 0) return;

    const observer = new IntersectionObserver(([entry]) => {
      if (!entry.isIntersecting) return;
      observer.disconnect();
      let start = 0;
      const duration = 1200;
      const step = timestamp => {
        if (!start) start = timestamp;
        const progress = Math.min((timestamp - start) / duration, 1);
        const ease = 1 - Math.pow(1 - progress, 3);
        el.textContent = Math.floor(ease * num) + suffix;
        if (progress < 1) requestAnimationFrame(step);
        else el.textContent = raw;
      };
      requestAnimationFrame(step);
    }, { threshold: 0.5 });
    observer.observe(el);
  });
}

// ── 5. CARD tilt effect ──
function initCardHover() {
  document.querySelectorAll('.cancha-card').forEach(card => {
    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width - 0.5) * 10;
      const y = ((e.clientY - rect.top) / rect.height - 0.5) * -10;
      card.style.transform = `translateY(-6px) rotateX(${y}deg) rotateY(${x}deg)`;
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
    });
  });
}

// ── 6. FORM input animations ──
function initFormAnimations() {
  document.querySelectorAll('.form-control, input, textarea, select').forEach(input => {
    const group = input.closest('.form-group');
    if (!group) return;
    input.addEventListener('focus', () => group.classList.add('focused'));
    input.addEventListener('blur', () => {
      group.classList.remove('focused');
      if (input.value) group.classList.add('filled');
      else group.classList.remove('filled');
    });
  });

  // Submit button loading state
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function () {
      const btn = this.querySelector('button[type="submit"]');
      if (btn) {
        btn.classList.add('loading');
        btn.disabled = true;
        const orig = btn.textContent;
        btn.textContent = 'Procesando...';
        setTimeout(() => {           // safety reset
          btn.classList.remove('loading');
          btn.disabled = false;
          btn.textContent = orig;
        }, 8000);
      }
    });
  });
}

// ── 7. PAGE TRANSITION ──
function initPageTransition() {
  document.body.classList.add('page-enter');
  requestAnimationFrame(() => {
    requestAnimationFrame(() => document.body.classList.add('page-enter-active'));
  });

  document.querySelectorAll('a[href]').forEach(a => {
    const href = a.getAttribute('href');
    if (!href || href.startsWith('#') || href.startsWith('http') || a.target === '_blank') return;
    a.addEventListener('click', e => {
      e.preventDefault();
      document.body.classList.add('page-exit');
      setTimeout(() => { window.location.href = href; }, 280);
    });
  });
}

// ── 8. Mobile menu ──
function toggleMenu() {
  const menu = document.getElementById('mobileMenu');
  const icon = document.querySelector('.nav-toggle');
  const open = menu.classList.toggle('open');
  if (icon) icon.textContent = open ? '✕' : '☰';
}

// ── 9. Toast notification helper ──
function showToast(msg, type = 'success') {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<span>${msg}</span><button onclick="this.parentElement.remove()">✕</button>`;
  document.body.appendChild(toast);
  requestAnimationFrame(() => toast.classList.add('visible'));
  setTimeout(() => { toast.classList.remove('visible'); setTimeout(() => toast.remove(), 400); }, 4000);
}

// ── 10. Confirm with nice modal ──
function confirmarAccion(msg, formId) {
  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay';
  overlay.innerHTML = `
    <div class="modal-box">
      <p class="modal-icon">⚠️</p>
      <p class="modal-msg">${msg}</p>
      <div class="modal-btns">
        <button class="btn btn-danger" id="modalSi">Sí, continuar</button>
        <button class="btn btn-outline" id="modalNo">Cancelar</button>
      </div>
    </div>`;
  document.body.appendChild(overlay);
  requestAnimationFrame(() => overlay.classList.add('visible'));

  document.getElementById('modalSi').onclick = () => {
    overlay.remove();
    document.getElementById(formId).submit();
  };
  document.getElementById('modalNo').onclick = () => {
    overlay.classList.remove('visible');
    setTimeout(() => overlay.remove(), 300);
  };
}
