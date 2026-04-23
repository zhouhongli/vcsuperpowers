# backend/utils/exceptions.py
"""自定义异常类"""


class LogNotFoundError(Exception):
    """日志不存在"""
    status_code = 404
    error_code = "LOG_NOT_FOUND"

    def __init__(self, log_id: str):
        self.log_id = log_id
        super().__init__(f"Log with ID '{log_id}' not found")


class InvalidLogDataError(Exception):
    """日志数据格式错误"""
    status_code = 400
    error_code = "INVALID_LOG_DATA"

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class DiagnosisNotFoundError(Exception):
    """诊断结果不存在"""
    status_code = 404
    error_code = "DIAGNOSIS_NOT_FOUND"

    def __init__(self, diagnosis_id: str):
        self.diagnosis_id = diagnosis_id
        super().__init__(f"Diagnosis with ID '{diagnosis_id}' not found")


class DiagnosisAlreadyExistsError(Exception):
    """诊断结果已存在"""
    status_code = 409
    error_code = "DIAGNOSIS_ALREADY_EXISTS"

    def __init__(self, log_id: str):
        self.log_id = log_id
        super().__init__(f"Diagnosis already exists for log '{log_id}'")
