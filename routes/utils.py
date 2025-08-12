from flask import flash, redirect, url_for
from functools import wraps

def handle_not_found(item_name, redirect_to):
    """공통 404 에러 처리 함수"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if result is None:
                flash(f"{item_name}을(를) 찾을 수 없습니다.", "error")
                return redirect(url_for(redirect_to))
            return result
        return wrapper
    return decorator

def validate_form_data(required_fields, form_data):
    """폼 데이터 유효성 검사"""
    missing_fields = []
    for field in required_fields:
        if not form_data.get(field, '').strip():
            missing_fields.append(field)
    
    return missing_fields

def flash_success_error(success, success_msg, error_msg):
    """성공/실패에 따른 플래시 메시지"""
    if success:
        flash(success_msg, "success")
    else:
        flash(error_msg, "error")
    return success