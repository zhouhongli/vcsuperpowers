"""文件上传单元测试"""


def test_check_file_extension_allowed():
    """允许的扩展名"""
    from backend.routes.logs import _check_file_extension
    assert _check_file_extension("error.log") is True
    assert _check_file_extension("debug.txt") is True
    assert _check_file_extension("data.LOG") is True


def test_check_file_extension_rejected():
    """拒绝的扩展名"""
    from backend.routes.logs import _check_file_extension
    assert _check_file_extension("report.pdf") is False
    assert _check_file_extension("image.png") is False
    assert _check_file_extension("file") is False
    assert _check_file_extension("") is False


def test_check_file_extension_none():
    """None 文件名"""
    from backend.routes.logs import _check_file_extension
    assert _check_file_extension(None) is False
