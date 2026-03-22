/**
 * Feedback Toolbox — VitaCore Mocks
 * Drop-in script for all mock pages.
 *
 * Config: replace SUPABASE_URL and SUPABASE_ANON_KEY with your project values.
 * Table: feedback_comments (see schema in docs)
 */
(function () {
  'use strict';

  // ─── Config ──────────────────────────────────────────────────────────────
  const SUPABASE_URL = 'https://YOUR_PROJECT_ID.supabase.co';
  const SUPABASE_ANON_KEY = 'YOUR_SUPABASE_ANON_KEY';
  const TABLE = 'feedback_comments';

  // ─── Helpers ─────────────────────────────────────────────────────────────
  const pagePath = window.location.pathname.split('/').pop() || 'index.html';
  const pageTitle = document.title;

  function getUser() {
    try { return JSON.parse(localStorage.getItem('feedback_user')) || null; }
    catch { return null; }
  }
  function saveUser(u) {
    localStorage.setItem('feedback_user', JSON.stringify(u));
  }
  function isAdmin() {
    const u = getUser();
    return u && u.is_admin === true;
  }
  function timeSince(dateStr) {
    const diff = (Date.now() - new Date(dateStr)) / 1000;
    if (diff < 60) return 'ahora';
    if (diff < 3600) return Math.floor(diff / 60) + 'm';
    if (diff < 86400) return Math.floor(diff / 3600) + 'h';
    return Math.floor(diff / 86400) + 'd';
  }
  function isNew(dateStr) {
    return (Date.now() - new Date(dateStr)) < 86400000; // 24h
  }

  // ─── Supabase REST calls ──────────────────────────────────────────────────
  async function fetchComments() {
    const user = getUser();
    if (!user) return [];
    let url = `${SUPABASE_URL}/rest/v1/${TABLE}?page_path=eq.${encodeURIComponent(pagePath)}&order=created_at.desc`;
    if (!isAdmin()) {
      url += `&user_email=eq.${encodeURIComponent(user.email)}`;
    }
    try {
      const res = await fetch(url, {
        headers: {
          'apikey': SUPABASE_ANON_KEY,
          'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
          'Content-Type': 'application/json'
        }
      });
      if (!res.ok) return [];
      return await res.json();
    } catch { return []; }
  }

  async function submitComment(data) {
    const res = await fetch(`${SUPABASE_URL}/rest/v1/${TABLE}`, {
      method: 'POST',
      headers: {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'
      },
      body: JSON.stringify(data)
    });
    return res.ok || res.status === 201;
  }

  // ─── Build UI ─────────────────────────────────────────────────────────────
  function buildUI() {
    // Inject CSS
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = (document.querySelector('link[href*="feedback.css"]') ? '' : 'assets/feedback.css');
    if (!document.querySelector('link[href*="feedback.css"]')) {
      document.head.appendChild(link);
    }

    const toggleBtn = document.createElement('button');
    toggleBtn.id = 'fb-toggle';
    toggleBtn.title = 'Dejar comentario';
    toggleBtn.innerHTML = `💬<span class="fb-badge" id="fb-badge"></span>`;

    const overlay = document.createElement('div');
    overlay.id = 'fb-overlay';

    const drawer = document.createElement('div');
    drawer.id = 'fb-drawer';
    drawer.innerHTML = `
      <div class="fb-drawer-header">
        <div>
          <h3>Feedback</h3>
          <div class="fb-page-hint" id="fb-page-hint">${pagePath}</div>
        </div>
        <button class="fb-close" id="fb-close">✕</button>
      </div>
      <div class="fb-drawer-body" id="fb-drawer-body">
        <!-- content injected dynamically -->
      </div>
    `;

    document.body.appendChild(overlay);
    document.body.appendChild(drawer);
    document.body.appendChild(toggleBtn);

    // Events
    toggleBtn.addEventListener('click', openDrawer);
    overlay.addEventListener('click', closeDrawer);
    document.getElementById('fb-close').addEventListener('click', closeDrawer);
  }

  // ─── Open / Close ─────────────────────────────────────────────────────────
  function openDrawer() {
    document.getElementById('fb-overlay').classList.add('open');
    document.getElementById('fb-drawer').classList.add('open');
    renderDrawerBody();
  }
  function closeDrawer() {
    document.getElementById('fb-overlay').classList.remove('open');
    document.getElementById('fb-drawer').classList.remove('open');
  }

  // ─── Render ───────────────────────────────────────────────────────────────
  async function renderDrawerBody() {
    const body = document.getElementById('fb-drawer-body');
    const user = getUser();

    if (!user) {
      renderLoginForm(body);
    } else {
      renderFeedbackForm(body, user);
    }
  }

  function renderLoginForm(container) {
    container.innerHTML = `
      <div style="font-size:13px;color:#64748b;margin-bottom:4px;">
        Ingresá tu nombre y email para dejar comentarios. Se guardará en este navegador.
      </div>
      <div class="fb-login-form" id="fb-login-form">
        <div>
          <label for="fb-inp-name">Nombre</label>
          <input type="text" id="fb-inp-name" placeholder="Ej: Damián García" autocomplete="name">
        </div>
        <div>
          <label for="fb-inp-email">Email</label>
          <input type="email" id="fb-inp-email" placeholder="tu@email.com" autocomplete="email">
        </div>
        <label class="fb-admin-check">
          <input type="checkbox" id="fb-inp-admin">
          <span>Soy administrador de la demo (ver todos los comentarios)</span>
        </label>
        <button class="fb-submit" id="fb-login-btn">Continuar →</button>
      </div>
    `;
    document.getElementById('fb-login-btn').addEventListener('click', () => {
      const name = document.getElementById('fb-inp-name').value.trim();
      const email = document.getElementById('fb-inp-email').value.trim();
      const isAdm = document.getElementById('fb-inp-admin').checked;
      if (!name || !email) { alert('Por favor completá nombre y email.'); return; }
      saveUser({ name, email, is_admin: isAdm });
      renderDrawerBody();
    });
  }

  function renderFeedbackForm(container, user) {
    container.innerHTML = `
      <div class="fb-user-section">
        <div class="fb-user-logged">
          <div>
            <div class="fb-user-name">${escHtml(user.name)}</div>
            <div class="fb-user-email">${escHtml(user.email)}${user.is_admin ? ' · <strong style="color:#00A896">admin</strong>' : ''}</div>
          </div>
          <button class="fb-change-link" id="fb-change-user">Cambiar</button>
        </div>
      </div>

      <div class="fb-field">
        <label class="fb-label">¿Sobre qué elemento? <span style="color:#94a3b8;font-weight:400">(opcional)</span></label>
        <input class="fb-input" id="fb-element" type="text" placeholder="Ej: el botón Publicar, la tabla de miembros...">
      </div>

      <div class="fb-field">
        <label class="fb-label">Comentario *</label>
        <textarea class="fb-input fb-textarea" id="fb-comment" placeholder="¿Qué cambiarías? ¿Algo que no funciona? ¿Sugerencia?"></textarea>
      </div>

      <button class="fb-submit" id="fb-send-btn">Enviar comentario</button>

      <div class="fb-success" id="fb-success">
        <div class="fb-success-icon">✅</div>
        <h4>¡Gracias!</h4>
        <p>Tu comentario fue registrado correctamente.</p>
        <button class="fb-success-back" id="fb-another">Dejar otro comentario</button>
      </div>

      <div class="fb-comments-section" id="fb-comments-section">
        <div class="fb-comments-title" id="fb-comments-title">Cargando comentarios...</div>
      </div>
    `;

    document.getElementById('fb-change-user').addEventListener('click', () => {
      localStorage.removeItem('feedback_user');
      renderDrawerBody();
    });

    document.getElementById('fb-send-btn').addEventListener('click', handleSubmit);
    document.getElementById('fb-another').addEventListener('click', () => {
      document.getElementById('fb-success').classList.remove('visible');
      document.getElementById('fb-send-btn').style.display = '';
      document.getElementById('fb-element').value = '';
      document.getElementById('fb-comment').value = '';
    });

    loadComments();
  }

  async function handleSubmit() {
    const user = getUser();
    const comment = document.getElementById('fb-comment').value.trim();
    if (!comment) { alert('El comentario no puede estar vacío.'); return; }

    const btn = document.getElementById('fb-send-btn');
    btn.disabled = true;
    btn.textContent = 'Enviando...';

    const data = {
      user_name: user.name,
      user_email: user.email,
      page_path: pagePath,
      page_title: pageTitle,
      element_hint: document.getElementById('fb-element').value.trim() || null,
      comment: comment
    };

    const ok = await submitComment(data);
    btn.style.display = 'none';
    document.getElementById('fb-success').classList.add('visible');
    if (ok) {
      updateBadge();
      loadComments();
    }
  }

  async function loadComments() {
    const comments = await fetchComments();
    const section = document.getElementById('fb-comments-section');
    if (!section) return;

    const titleEl = document.getElementById('fb-comments-title');
    const label = isAdmin() ? 'Todos los comentarios en esta página' : 'Mis comentarios en esta página';
    titleEl.textContent = `${label} (${comments.length})`;

    const existing = section.querySelectorAll('.fb-comment-card');
    existing.forEach(el => el.remove());

    if (comments.length === 0) {
      const empty = document.createElement('div');
      empty.className = 'fb-no-comments';
      empty.textContent = 'Sin comentarios aún.';
      section.appendChild(empty);
      return;
    }

    comments.forEach(c => {
      const card = document.createElement('div');
      card.className = 'fb-comment-card' + (isNew(c.created_at) ? ' is-new' : '');
      card.innerHTML = `
        <div class="fb-comment-meta">
          <span class="fb-comment-author">${escHtml(c.user_name)}${isNew(c.created_at) ? '<span class="fb-new-badge">nuevo</span>' : ''}</span>
          <span class="fb-comment-time">${timeSince(c.created_at)}</span>
        </div>
        ${c.element_hint ? `<div class="fb-comment-element">Sobre: ${escHtml(c.element_hint)}</div>` : ''}
        <div class="fb-comment-text">${escHtml(c.comment)}</div>
      `;
      section.appendChild(card);
    });

    updateBadgeCount(comments.length);
  }

  async function updateBadge() {
    const comments = await fetchComments();
    updateBadgeCount(comments.length);
  }

  function updateBadgeCount(count) {
    const badge = document.getElementById('fb-badge');
    if (!badge) return;
    if (count > 0) {
      badge.textContent = count;
      badge.classList.add('visible');
    } else {
      badge.classList.remove('visible');
    }
  }

  function escHtml(str) {
    if (!str) return '';
    return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  // ─── Init ─────────────────────────────────────────────────────────────────
  function init() {
    buildUI();
    updateBadge();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
