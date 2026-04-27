// frontend/js/api.js
/** API 调用封装 */

const API_BASE_URL = 'http://localhost:8001/api';

/**
 * 通用 fetch 封装
 * @param skip404Redirect - 如果为 true，404 时不跳转页面，而是抛出错误
 */
async function apiRequest(endpoint, options = {}, skip404Redirect = false) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
        headers: {
            'Content-Type': 'application/json',
        },
        ...options,
    };

    try {
        const response = await fetch(url, config);

        if (response.status === 404) {
            if (!skip404Redirect) {
                window.location.href = '404.html';
            }
            return null;
        }
        if (response.status >= 500) {
            showToast('服务器错误，请稍后重试', 'danger');
            return null;
        }

        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: response.statusText }));
            throw new Error(error.detail || `HTTP ${response.status}`);
        }
        if (response.status === 204) {
            return null;
        }
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

/**
 * 日志 API
 */
const logsApi = {
    // 创建日志
    async create(data) {
        return apiRequest('/logs', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    },

    // 通过文件上传创建日志
    async createFromFile(formData) {
        return apiRequest('/logs', {
            method: 'POST',
            body: formData,
            headers: {},
        });
    },

    // 获取日志列表
    async getList(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const suffix = queryString ? `?${queryString}` : '';
        return apiRequest(`/logs${suffix}`);
    },

    // 获取日志详情
    async getById(id) {
        return apiRequest(`/logs/${id}`);
    },

    // 更新日志
    async update(id, data) {
        return apiRequest(`/logs/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    },

    // 删除日志
    async delete(id) {
        return apiRequest(`/logs/${id}`, {
            method: 'DELETE',
        });
    },

    // 批量删除
    async deleteBatch(ids) {
        return apiRequest('/logs', {
            method: 'DELETE',
            body: JSON.stringify({ ids }),
        });
    },

    // 诊断日志
    async diagnose(id) {
        return apiRequest(`/logs/${id}/diagnose`, {
            method: 'POST',
        });
    },

    // 获取诊断结果（允许 404，首次加载时可能还没有诊断）
    async getDiagnosis(id) {
        return apiRequest(`/logs/${id}/diagnosis`, {}, true);
    },
};

/**
 * 仪表盘 API
 */
const dashboardApi = {
    async getStats() {
        return apiRequest('/dashboard/stats');
    },
};

/**
 * 工具函数
 */
function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        const container = document.createElement('div');
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;

    document.querySelector('.toast-container').appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();

    toast.addEventListener('hidden.bs.toast', () => toast.remove());
}

// 格式化日期
function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN');
}
