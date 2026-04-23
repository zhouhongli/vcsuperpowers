// frontend/js/dashboard.js
/** 仪表盘页面逻辑 */

let trendRange = 7;
let charts = {};

/**
 * 加载仪表盘数据
 */
async function loadDashboard() {
    try {
        const stats = await dashboardApi.getStats();
        renderSummaryCards(stats);
        renderExceptionTypeChart(stats.exception_type_distribution);
        renderSeverityChart(stats.severity_distribution);
        renderTrendChart(stats.trend);
        renderTopServicesChart(stats.top_services);
    } catch (err) {
        showToast('加载失败：' + err.message, 'danger');
    }
}

/**
 * 渲染概览卡片
 */
function renderSummaryCards(stats) {
    // 计算总数
    const total = stats.exception_type_distribution.reduce((sum, item) => sum + item.count, 0);
    document.getElementById('totalLogs').textContent = total;

    // 按严重程度统计
    const severityMap = {};
    stats.severity_distribution.forEach(item => {
        severityMap[item.level] = item.count;
    });

    document.getElementById('criticalCount').textContent = severityMap['CRITICAL'] || 0;
    document.getElementById('highCount').textContent = severityMap['HIGH'] || 0;
    document.getElementById('lowMediumCount').textContent =
        (severityMap['LOW'] || 0) + (severityMap['MEDIUM'] || 0);
}

/**
 * 渲染异常类型饼图
 */
function renderExceptionTypeChart(data) {
    const ctx = document.getElementById('exceptionTypeChart').getContext('2d');

    if (charts.exceptionType) {
        charts.exceptionType.destroy();
    }

    charts.exceptionType = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.map(item => item.type),
            datasets: [{
                data: data.map(item => item.count),
                backgroundColor: [
                    '#0d6efd',
                    '#dc3545',
                    '#ffc107',
                    '#198754',
                    '#6c757d',
                ],
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                },
            },
        },
    });
}

/**
 * 渲染严重程度柱状图
 */
function renderSeverityChart(data) {
    const ctx = document.getElementById('severityChart').getContext('2d');

    if (charts.severity) {
        charts.severity.destroy();
    }

    charts.severity = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(item => item.level),
            datasets: [{
                label: '数量',
                data: data.map(item => item.count),
                backgroundColor: [
                    '#198754',
                    '#ffc107',
                    '#dc3545',
                    '#212529',
                ],
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false,
                },
            },
            scales: {
                y: {
                    beginAtZero: true,
                },
            },
        },
    });
}

/**
 * 渲染趋势折线图
 */
function renderTrendChart(data) {
    const ctx = document.getElementById('trendChart').getContext('2d');

    if (charts.trend) {
        charts.trend.destroy();
    }

    // 根据趋势范围过滤数据
    const filteredData = data.slice(-trendRange);

    charts.trend = new Chart(ctx, {
        type: 'line',
        data: {
            labels: filteredData.map(item => item.date.substring(5)), // 只显示 MM-DD
            datasets: [{
                label: '异常数量',
                data: filteredData.map(item => item.count),
                borderColor: '#0d6efd',
                backgroundColor: 'rgba(13, 110, 253, 0.1)',
                fill: true,
                tension: 0.3,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false,
                },
            },
            scales: {
                y: {
                    beginAtZero: true,
                },
            },
        },
    });
}

/**
 * 渲染 Top 服务横向柱状图
 */
function renderTopServicesChart(data) {
    const ctx = document.getElementById('topServicesChart').getContext('2d');

    if (charts.topServices) {
        charts.topServices.destroy();
    }

    // 如果没有数据，显示提示
    if (!data || data.length === 0) {
        ctx.font = '16px Arial';
        ctx.fillStyle = '#6c757d';
        ctx.textAlign = 'center';
        ctx.fillText('暂无数据', 200, 150);
        return;
    }

    charts.topServices = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(item => item.service),
            datasets: [{
                label: '异常数量',
                data: data.map(item => item.count),
                backgroundColor: '#0dcaf0',
                indexAxis: 'y',
            }],
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false,
                },
            },
            scales: {
                x: {
                    beginAtZero: true,
                },
            },
        },
    });
}

/**
 * 设置趋势图时间范围
 */
function setTrendRange(days) {
    trendRange = days;
    document.getElementById('btn7d').classList.toggle('active', days === 7);
    document.getElementById('btn30d').classList.toggle('active', days === 30);
    loadDashboard();
}

// 页面加载时获取数据
document.addEventListener('DOMContentLoaded', loadDashboard);
