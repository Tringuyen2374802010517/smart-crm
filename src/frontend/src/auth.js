const API_BASE = 'http://127.0.0.1:8000';
const TOKEN_KEY = 'smartcrm_access_token';

export function getToken() {
  return sessionStorage.getItem(TOKEN_KEY);
}

export function clearToken() {
  sessionStorage.removeItem(TOKEN_KEY);
}

export async function login(username, password) {
  const response = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || 'Đăng nhập thất bại');
  }

  sessionStorage.setItem(TOKEN_KEY, data.access_token);
  return data.user;
}

export async function getCurrentUser() {
  const token = getToken();
  if (!token) return null;

  try {
    const response = await fetch(`${API_BASE}/auth/me`, {
      headers: { Authorization: `Bearer ${token}` }
    });

    if (!response.ok) {
      clearToken();
      return null;
    }

    return await response.json();
  } catch {
    return null;
  }
}

export async function logout() {
  const token = getToken();

  try {
    if (token) {
      await fetch(`${API_BASE}/auth/logout`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` }
      });
    }
  } finally {
    clearToken();
  }
}

export function renderLogin(container, onSuccess) {
  container.innerHTML = `
    <div class="login-page">
      <div class="login-card">
        <div class="login-logo">M</div>
        <div class="login-heading">
          <h1>Welcome back</h1>
          <p>Đăng nhập vào hệ thống Smart CRM</p>
        </div>
        <form id="login-form">
          <label for="login-username">Tên đăng nhập</label>
          <input
            id="login-username"
            type="text"
            autocomplete="username"
            placeholder="Nhập tên đăng nhập"
            required
          />
          <label for="login-password">Mật khẩu</label>
          <input
            id="login-password"
            type="password"
            autocomplete="current-password"
            placeholder="Nhập mật khẩu"
            required
          />
          <p id="login-error" role="alert"></p>
          <button type="submit" id="login-submit">
            Đăng nhập
          </button>
        </form>
        <div class="login-footer">
          MEKONG MOBILE · SMART CRM
        </div>
      </div>
    </div>
  `;

  const form = container.querySelector('#login-form');
  const submit = container.querySelector('#login-submit');
  const error = container.querySelector('#login-error');

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    submit.disabled = true;
    submit.textContent = 'Đang đăng nhập...';
    error.textContent = '';

    try {
      const username = container
        .querySelector('#login-username').value.trim();

      const password = container
        .querySelector('#login-password').value;

      const user = await login(username, password);
      onSuccess(user);
    } catch (err) {
      error.textContent = err.message;
    } finally {
      submit.disabled = false;
      submit.textContent = 'Đăng nhập';
    }
  });
}
