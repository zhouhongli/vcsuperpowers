// frontend/js/diagnosis.js
/** 诊断详情页面逻辑 */

let logId = null;
let currentLog = null;
let currentDiagnosis = null;

/**
 * 获取 URL 参数中的日志 ID
 */
function getLogIdFromUrl() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

/**
 * 页面初始化
 */
document.addEventListener('DOMContentLoaded', async function() {
    logId = getLogIdFromUrl();

    if (!logId) {
        showError('未提供日志 ID');
        return;
    }

    await loadLogAndDiagnosis();
});

/**
 * 加载日志和诊断数据
 */
async function loadLogAndDiagnosis() {
    try {
        // 先加载日志详情
        currentLog = await logsApi.getById(logId);

        // 尝试诊断
        await loadDiagnosis();
    } catch (err) {
        showError('加载日志失败：' + err.message);
    }
}

/**
 * 加载诊断结果
 */
async function loadDiagnosis() {
    try {
        // 先尝试获取已有诊断
        currentDiagnosis = await logsApi.getDiagnosis(logId);
        if (!currentDiagnosis) {
            // 没有诊断，调用诊断 API
            currentDiagnosis = await logsApi.diagnose(logId);
        }
    } catch (err) {
        // 诊断 API 可能失败（404），仍然显示日志
        console.warn('诊断加载失败:', err.message);
        currentDiagnosis = null;
    }

    // 渲染页面
    renderLog(currentLog);
    if (currentDiagnosis) {
        renderDiagnosis(currentDiagnosis);
    }
}

/**
 * 渲染日志信息
 */
function renderLog(log) {
    document.getElementById('logId').textContent = log.id.substring(0, 8) + '...';
    document.getElementById('logExceptionType').textContent = log.exception_type;
    document.getElementById('logSeverity').innerHTML = getSeverityBadge(log.severity);
    document.getElementById('logService').textContent = log.service_name || '-';
    document.getElementById('logContent').textContent = log.content;

    // 堆栈跟踪
    const stackTraceSection = document.getElementById('stackTraceSection');
    if (log.stack_trace) {
        stackTraceSection.classList.remove('d-none');
        document.getElementById('logStackTrace').textContent = log.stack_trace;
    } else {
        stackTraceSection.classList.add('d-none');
    }
}

/**
 * 渲染诊断结果
 */
function renderDiagnosis(diagnosis) {
    // 严重程度
    const severityBadge = document.getElementById('severityBadge');
    const badgeColor = getSeverityColor(diagnosis.severity_assessment);
    severityBadge.className = 'badge ' + badgeColor;
    severityBadge.textContent = diagnosis.severity_assessment;

    // 根因分析
    document.getElementById('rootCause').textContent = diagnosis.root_cause;

    // 解决方案（按行分割）
    const solutions = diagnosis.solution.split('\n');
    document.getElementById('solution').innerHTML = solutions.map(s =>
        `<li>${s}</li>`
    ).join('');

    // 相似日志
    const similarLogsEl = document.getElementById('similarLogs');
    if (diagnosis.similar_logs && diagnosis.similar_logs.length > 0) {
        similarLogsEl.innerHTML = diagnosis.similar_logs.map(id =>
            `<li class="list-group-item list-group-item-action">
                <a href="diagnosis.html?id=${id}" class="text-decoration-none">
                    <small>日志 ${id.substring(0, 8)}...</small>
                </a>
            </li>`
        ).join('');
    } else {
        similarLogsEl.innerHTML = '<li class="list-group-item text-muted">暂无相似日志</li>';
    }
}

/**
 * 重新诊断
 */
async function redaignose() {
    try {
        currentDiagnosis = await logsApi.diagnose(logId);
        renderDiagnosis(currentDiagnosis);
        showToast('重新诊断成功', 'success');
    } catch (err) {
        showToast('重新诊断失败：' + err.message, 'danger');
    }
}

/**
 * 显示错误
 */
function showError(message) {
    document.getElementById('loadingState').classList.add('d-none');
    document.getElementById('errorState').classList.remove('d-none');
    document.getElementById('errorMessage').textContent = message;
}

/**
 * 显示诊断结果
 */
function showDiagnosis() {
    document.getElementById('loadingState').classList.add('d-none');
    document.getElementById('diagnosisResult').classList.remove('d-none');
}

/**
 * 获取严重程度的颜色
 */
function getSeverityColor(severity) {
    const colors = {
        'LOW': 'bg-success',
        'MEDIUM': 'bg-warning text-dark',
        'HIGH': 'bg-danger',
        'CRITICAL': 'bg-dark',
    };
    return colors[severity] || 'bg-secondary';
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

/**
 * 返回列表
 */
function goBack() {
    window.location.href = 'list.html';
}

// 覆盖 body 的 onDOMContentLoaded - 使用 IIFE 确保在 DOM 加载后显示诊断结果
document.addEventListener('DOMContentLoaded', function() {
    // 当有日志和诊断数据时显示诊断结果
    setTimeout(() => {
        if (currentLog) {
            showDiagnosis();
        }
    }, 0);
});
