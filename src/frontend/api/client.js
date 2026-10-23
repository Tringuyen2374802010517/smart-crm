
const API_BASE_URL = 'http://localhost:8000';

export async function apiRequest(endpoint, options = {}) {
  const { headers, ...restOptions } = options;

  let response;

  try {
    response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...restOptions,
      headers: {
        'Content-Type': 'application/json',
        ...headers,
      },
    });
  } catch {
    throw new Error('Không thể kết nối đến máy chủ. Vui lòng thử lại.');
  }

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error('Phiên đăng nhập không hợp lệ hoặc đã hết hạn.');
    }

    let message = `Yêu cầu thất bại (HTTP ${response.status}).`;

    try {
      const errorData = await response.json();
      if (typeof errorData.detail === 'string') {
        message = errorData.detail;
      }
    } catch {
      // Giữ thông báo lỗi HTTP mặc định.
    }

    throw new Error(message);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}
