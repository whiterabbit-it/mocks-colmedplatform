/**
 * auth.js — Magic Link auth para mocks CMRB
 * Requiere Supabase JS SDK cargado antes en la página.
 * Expone window.sbAuth con los métodos de sesión.
 */
(function () {
  'use strict';

  const SUPABASE_URL = 'https://efuglxlxgbvhsaiecffs.supabase.co';
  const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVmdWdseGx4Z2J2aHNhaWVjZmZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQxNDU0ODAsImV4cCI6MjA4OTcyMTQ4MH0.3w2rq_8vArsiuIY_Mx78gWROlrwXyIU0ciTRwFHkaiI';
  const SESSION_KEY = 'mocks_auth_session';
  const REDIRECT_URL = 'https://whiterabbit-it.github.io/mocks-colmedplatform/index.html';

  let _client = null;

  function getClient() {
    if (!_client && window.supabase) {
      _client = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
    }
    return _client;
  }

  function getStoredSession() {
    try {
      const data = JSON.parse(localStorage.getItem(SESSION_KEY));
      if (!data || !data.email) return null;
      if (data.expires_at && Date.now() / 1000 > data.expires_at) {
        // Persist name before removing expired session
        if (data.name) localStorage.setItem('mocks_saved_name_' + data.email, data.name);
        localStorage.removeItem(SESSION_KEY);
        return null;
      }
      return data;
    } catch { return null; }
  }

  function storeSession(session, existingName) {
    if (!session || !session.user) return;
    const prev = getStoredSession();
    const savedName = localStorage.getItem('mocks_saved_name_' + session.user.email);
    localStorage.setItem(SESSION_KEY, JSON.stringify({
      email: session.user.email,
      name: existingName || (prev && prev.name) || savedName || null,
      user_id: session.user.id,
      expires_at: session.expires_at
    }));
  }

  async function checkAndHandleCallback() {
    const sb = getClient();
    if (!sb) return null;
    const { data } = await sb.auth.getSession();
    if (data && data.session) {
      storeSession(data.session);
      return data.session;
    }
    return null;
  }

  async function sendMagicLink(email) {
    const sb = getClient();
    if (!sb) return { error: { message: 'SDK no disponible' } };
    return sb.auth.signInWithOtp({
      email,
      options: { emailRedirectTo: REDIRECT_URL }
    });
  }

  function saveName(name) {
    const stored = getStoredSession();
    if (!stored) return;
    stored.name = name;
    localStorage.setItem(SESSION_KEY, JSON.stringify(stored));
    localStorage.setItem('mocks_saved_name_' + stored.email, name);
  }

  async function signOut() {
    const sb = getClient();
    localStorage.removeItem(SESSION_KEY);
    if (sb) await sb.auth.signOut();
    window.location.reload();
  }

  window.sbAuth = {
    getClient,
    getStoredSession,
    checkAndHandleCallback,
    sendMagicLink,
    saveName,
    signOut
  };
})();
