"""
결제 관리 테스트
"""

import pytest
import datetime
from app.payment import create_payment, get_all_payments, get_payments_by_customer, update_payment, delete_payment, get_payment_methods
from tests.conftest import create_test_customer, create_test_visit, create_test_payment, cleanup_test_data

def test_create_payment(test_visit):
    """결제 등록 테스트"""
    customer_id, visit_id = test_visit
    
    # 결제 등록
    payment_data = {
        "amount": 30000,
        "payment_method_code": "CARD",
        "payment_datetime": datetime.datetime.now()
    }
    result = create_payment(visit_id, payment_data)
    assert result is True
    
    # 정리
    payments = get_payments_by_customer(customer_id)
    if payments:
        delete_payment(payments[0]["payment_id"])

def test_get_all_payments():
    """전체 결제 조회 테스트"""
    payments = get_all_payments()
    assert isinstance(payments, list)

def test_get_payments_by_customer(test_payment):
    """고객별 결제 조회 테스트"""
    customer_id, visit_id, payment_id = test_payment
    payments = get_payments_by_customer(customer_id)
    assert len(payments) > 0

def test_update_payment(test_payment):
    """결제 수정 테스트"""
    customer_id, visit_id, payment_id = test_payment
    
    payment_data = {
        "payment_id": payment_id,
        "amount": 60000,
        "payment_method_code": "CASH",
        "payment_datetime": datetime.datetime.now()
    }
    result = update_payment(payment_data)
    assert result is True

def test_delete_payment():
    """결제 삭제 테스트"""
    # 테스트 데이터 생성
    customer_id = create_test_customer("삭제결제", "010-3333-4444")
    visit_id = create_test_visit(customer_id, "삭제할 방문")
    payment_id = create_test_payment(visit_id, 40000, "CASH")
    
    assert customer_id is not None
    assert visit_id is not None
    assert payment_id is not None
    
    # 삭제
    result = delete_payment(payment_id)
    assert result is True
    
    # 확인
    payments = get_payments_by_customer(customer_id)
    assert len(payments) == 0

def test_get_payment_methods():
    """결제 수단 조회 테스트"""
    methods = get_payment_methods()
    assert isinstance(methods, list)
    assert len(methods) > 0
