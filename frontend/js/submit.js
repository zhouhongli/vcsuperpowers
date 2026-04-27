// frontend/js/submit.js
/** 日志提交页面逻辑 */

document.getElementById('logForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    // 获取表单值
    const exceptionType = document.getElementById('exceptionType').value;
    const severity = document.querySelector('input[name="severity"]:checked');
    const content = document.getElementById('logContent').value.trim();
    const fileInput = document.getElementById('logFile');
    const occurredAt = document.getElementById('occurredAt').value;
    const serviceName = document.getElementById('serviceName').value.trim();
    const stackTrace = document.getElementById('stackTrace').value.trim();
    const userId = document.getElementById('userId').value.trim();

    // 验证必填项
    let isValid = true;

    if (!exceptionType) {
        document.getElementById('exceptionType').classList.add('is-invalid');
        isValid = false;
    } else {
        document.getElementById('exceptionType').classList.remove('is-invalid');
    }

    const severityError = document.getElementById('severityError');
    if (!severity) {
        severityError.textContent = '请选择严重程度';
        isValid = false;
    } else {
        severityError.textContent = '';
    }

    // 日志内容或文件二选一
    const hasFile = fileInput.files.length > 0;
    if (!content && !hasFile) {
        document.getElementById('logContent').classList.add('is-invalid');
        showToast('请输入日志内容或上传文件', 'warning');
        isValid = false;
    } else {
        document.getElementById('logContent').classList.remove('is-invalid');
    }

    if (!isValid) {
        showToast('请修正表单错误', 'danger');
        return;
    }

    try {
        let result;

        if (hasFile) {
            // 使用 FormData 提交文件
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            formData.append('exception_type', exceptionType);
            formData.append('severity', severity.value);
            if (serviceName) formData.append('service_name', serviceName);
            if (stackTrace) formData.append('stack_trace', stackTrace);
            if (userId) formData.append('user_id', userId);
            if (occurredAt) formData.append('occurred_at', occurredAt);
            if (content) formData.append('content', content);

            result = await logsApi.createFromFile(formData);
        } else {
            // 使用 JSON 提交
            const submitData = {
                exception_type: exceptionType,
                severity: severity.value,
                content: content,
                service_name: serviceName || null,
                stack_trace: stackTrace || null,
                user_id: userId || null,
                occurred_at: occurredAt || null,
            };
            result = await logsApi.create(submitData);
        }

        showToast('日志提交成功！', 'success');

        // 跳转到诊断页面
        setTimeout(() => {
            window.location.href = `diagnosis.html?id=${result.id}`;
        }, 1000);
    } catch (err) {
        showToast('提交失败：' + err.message, 'danger');
    }
});

// 清除错误状态
document.getElementById('exceptionType').addEventListener('change', function() {
    this.classList.remove('is-invalid');
});

document.querySelectorAll('input[name="severity"]').forEach(radio => {
    radio.addEventListener('change', function() {
        document.getElementById('severityError').textContent = '';
    });
});
