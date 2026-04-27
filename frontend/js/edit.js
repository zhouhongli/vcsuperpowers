// frontend/js/edit.js
/** 编辑日志页面逻辑 */

let logId = null;
let currentLog = null;

function getLogIdFromUrl() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

/** 页面初始化 */
document.addEventListener('DOMContentLoaded', async function() {
    logId = getLogIdFromUrl();
    if (!logId) {
        showError('未提供日志 ID');
        return;
    }
    await loadLog();
});

/** 加载日志数据并回填表单 */
async function loadLog() {
    try {
        currentLog = await logsApi.getById(logId);
        fillForm(currentLog);
        document.getElementById('loadingState').classList.add('d-none');
        document.getElementById('editFormContainer').classList.remove('d-none');
    } catch (err) {
        showError('加载日志失败：' + err.message);
    }
}

/** 回填表单 */
function fillForm(log) {
    document.getElementById('exceptionType').value = log.exception_type;
    document.getElementById('logContent').value = log.content || '';
    document.getElementById('serviceName').value = log.service_name || '';
    document.getElementById('stackTrace').value = log.stack_trace || '';

    // 严重程度单选
    const severityRadio = document.querySelector(`input[name="severity"][value="${log.severity}"]`);
    if (severityRadio) severityRadio.checked = true;

    // 发生时间格式化
    if (log.occurred_at) {
        const date = new Date(log.occurred_at);
        const local = date.getFullYear() + '-' +
            String(date.getMonth() + 1).padStart(2, '0') + '-' +
            String(date.getDate()).padStart(2, '0') + 'T' +
            String(date.getHours()).padStart(2, '0') + ':' +
            String(date.getMinutes()).padStart(2, '0');
        document.getElementById('occurredAt').value = local;
    }
}

/** 表单提交 */
document.getElementById('editForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const exceptionType = document.getElementById('exceptionType').value;
    const severity = document.querySelector('input[name="severity"]:checked');
    const content = document.getElementById('logContent').value.trim();
    const occurredAt = document.getElementById('occurredAt').value;
    const serviceName = document.getElementById('serviceName').value.trim();
    const stackTrace = document.getElementById('stackTrace').value.trim();

    if (!exceptionType || !severity) {
        showToast('请填写必填项', 'warning');
        return;
    }

    const updateData = {
        exception_type: exceptionType,
        severity: severity.value,
        content: content || undefined,
        service_name: serviceName || undefined,
        stack_trace: stackTrace || undefined,
        occurred_at: occurredAt || undefined,
    };

    try {
        await logsApi.update(logId, updateData);
        showToast('保存成功', 'success');
        setTimeout(() => {
            window.location.href = `diagnosis.html?id=${logId}`;
        }, 1000);
    } catch (err) {
        showToast('保存失败：' + err.message, 'danger');
    }
});

function showError(message) {
    document.getElementById('loadingState').classList.add('d-none');
    document.getElementById('errorState').classList.remove('d-none');
    document.getElementById('errorMessage').textContent = message;
}

function goBack() {
    window.location.href = 'list.html';
}
