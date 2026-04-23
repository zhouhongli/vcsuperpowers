// frontend/js/list.js
/** 日志列表页面逻辑 */

let currentPage = 1;
let currentLogId = null;

/**
 * 加载日志列表
 */
async function loadLogs() {
    const exceptionType = document.getElementById('filterExceptionType').value;
    const severity = document.getElementById('filterSeverity').value;
    const service = document.getElementById('filterService').value.trim();
    const search = document.getElementById('searchBox').value.trim();

    const params = {
        page: currentPage,
        page_size: 10,
    };
    if (exceptionType) params.exception_type = exceptionType;
    if (severity) params.severity = severity;
    if (service) params.service_name = service;
    if (search) params.search = search;

    try {
        const data = await logsApi.getList(params);
        renderTable(data.items);
        renderPagination(data);
        resetSelection();
    } catch (err) {
        showToast('加载失败：' + err.message, 'danger');
        document.getElementById('logsTableBody').innerHTML =
            '<tr><td colspan="7" class="text-center text-danger">加载失败</td></tr>';
    }
}

/**
 * 渲染日志表格
 */
function renderTable(logs) {
    const tbody = document.getElementById('logsTableBody');

    if (!logs || logs.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center">暂无数据</td></tr>';
        return;
    }

    tbody.innerHTML = logs.map(log => {
        const severityBadge = getSeverityBadge(log.severity);
        return `
            <tr>
                <td><input type="checkbox" class="log-checkbox" value="${log.id}" onchange="updateSelection()"></td>
                <td><small class="text-muted">${log.id.substring(0, 8)}...</small></td>
                <td><span class="badge bg-info">${log.exception_type}</span></td>
                <td>${severityBadge}</td>
                <td>${log.service_name || '-'}</td>
                <td>${formatDate(log.occurred_at)}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary" onclick="viewLog('${log.id}')">查看</button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteLog('${log.id}')">删除</button>
                    <button class="btn btn-sm btn-outline-success" onclick="diagnoseLog('${log.id}')">诊断</button>
                </td>
            </tr>
        `;
    }).join('');
}

/**
 * 渲染分页控件
 */
function renderPagination(data) {
    const pagination = document.getElementById('pagination');
    const info = document.getElementById('paginationInfo');

    const totalPages = data.total_pages;
    const pageWindow = 5; // 显示的页码范围

    let startPage = Math.max(1, data.page - Math.floor(pageWindow / 2));
    let endPage = Math.min(totalPages, startPage + pageWindow - 1);
    if (endPage - startPage < pageWindow - 1) {
        startPage = Math.max(1, endPage - pageWindow + 1);
    }

    let html = '';

    // 上一页
    html += `<li class="page-item ${data.page <= 1 ? 'disabled' : ''}">
        <a class="page-link" href="#" onclick="goToPage(${data.page - 1}); return false;">上一页</a>
    </li>`;

    // 页码
    for (let i = startPage; i <= endPage; i++) {
        html += `<li class="page-item ${i === data.page ? 'active' : ''}">
            <a class="page-link" href="#" onclick="goToPage(${i}); return false;">${i}</a>
        </li>`;
    }

    // 下一页
    html += `<li class="page-item ${data.page >= totalPages ? 'disabled' : ''}">
        <a class="page-link" href="#" onclick="goToPage(${data.page + 1}); return false;">下一页</a>
    </li>`;

    pagination.innerHTML = html;
    info.textContent = `共 ${data.total} 条记录，第 ${data.page}/${totalPages} 页`;
}

/**
 * 跳转到指定页
 */
function goToPage(page) {
    currentPage = page;
    loadLogs();
}

/**
 * 查看日志详情
 */
async function viewLog(id) {
    try {
        const log = await logsApi.getById(id);
        document.getElementById('detailId').textContent = log.id;
        document.getElementById('detailExceptionType').textContent = log.exception_type;
        document.getElementById('detailSeverity').innerHTML = getSeverityBadge(log.severity);
        document.getElementById('detailService').textContent = log.service_name || '-';
        document.getElementById('detailOccurredAt').textContent = formatDate(log.occurred_at);
        document.getElementById('detailContent').textContent = log.content;
        document.getElementById('detailStackTrace').textContent = log.stack_trace || '-';

        currentLogId = log.id;

        const modal = new bootstrap.Modal(document.getElementById('logDetailModal'));
        modal.show();
    } catch (err) {
        showToast('加载失败：' + err.message, 'danger');
    }
}

/**
 * 删除日志
 */
async function deleteLog(id) {
    if (!confirm('确定删除这条日志？')) return;

    try {
        await logsApi.delete(id);
        showToast('删除成功', 'success');
        loadLogs();
    } catch (err) {
        showToast('删除失败：' + err.message, 'danger');
    }
}

/**
 * 诊断日志
 */
async function diagnoseLog(id) {
    try {
        await logsApi.diagnose(id);
        window.location.href = `diagnosis.html?id=${id}`;
    } catch (err) {
        showToast('诊断失败：' + err.message, 'danger');
    }
}

/**
 * 诊断当前查看的日志
 */
function diagnoseCurrentLog() {
    if (currentLogId) {
        bootstrap.Modal.getInstance(document.getElementById('logDetailModal')).hide();
        diagnoseLog(currentLogId);
    }
}

/**
 * 批量删除
 */
async function batchDelete() {
    const ids = getSelectedIds();
    if (ids.length === 0) return;

    if (!confirm(`确定删除选中的 ${ids.length} 条日志？`)) return;

    try {
        await logsApi.deleteBatch(ids);
        showToast(`成功删除 ${ids.length} 条日志`, 'success');
        loadLogs();
    } catch (err) {
        showToast('批量删除失败：' + err.message, 'danger');
    }
}

/**
 * 获取选中的日志 ID 列表
 */
function getSelectedIds() {
    const checkboxes = document.querySelectorAll('.log-checkbox:checked');
    return Array.from(checkboxes).map(cb => cb.value);
}

/**
 * 更新选中状态
 */
function updateSelection() {
    const ids = getSelectedIds();
    const count = ids.length;

    document.getElementById('selectedCount').textContent = count;
    document.getElementById('batchDeleteBtn').disabled = count === 0;
}

/**
 * 全选/取消全选
 */
function toggleSelectAll() {
    const checked = document.getElementById('selectAll').checked;
    document.querySelectorAll('.log-checkbox').forEach(cb => cb.checked = checked);
    updateSelection();
}

/**
 * 重置选择
 */
function resetSelection() {
    document.getElementById('selectAll').checked = false;
    document.querySelectorAll('.log-checkbox').forEach(cb => cb.checked = false);
    document.getElementById('selectedCount').textContent = '0';
    document.getElementById('batchDeleteBtn').disabled = true;
}

/**
 * 重置筛选
 */
function resetFilters() {
    document.getElementById('filterExceptionType').value = '';
    document.getElementById('filterSeverity').value = '';
    document.getElementById('filterService').value = '';
    document.getElementById('searchBox').value = '';
    currentPage = 1;
    loadLogs();
}

/**
 * 获取严重程度的徽章 HTML
 */
function getSeverityBadge(severity) {
    const colors = {
        'LOW': 'bg-success',
        'MEDIUM': 'bg-warning text-dark',
        'HIGH': 'bg-danger',
        'CRITICAL': 'bg-dark',
    };
    return `<span class="badge ${colors[severity] || 'bg-secondary'}">${severity}</span>`;
}

// 页面加载时获取数据
document.addEventListener('DOMContentLoaded', loadLogs);
