"""
결제 관리 테스트
"""

import pytest
import datetime
from app.payment import create_payment, get_all_payments, get_payments_by_customer, update_payment, delete_payment, get_payment_methods
from app.visit import create_visit, get_visits_by_customer, delete_visit
from app.customer import create_customer, search_customers, delete_customer

@pytest.fixture(scope="module")
def sample_data():
    """테스트용 고객, 방문, 결제 생성"""
    create_customer("결제고객", "010-5555-6666", "1995-09-09", "M", "")
    customers = search_customers("결제고객")
    customer_id = customers[0]["customer_id"]

    create_visit(customer_id, {"visit_date": datetime.datetime.now(), "memo": "결제 테스트"})
    visits = get_visits_by_customer(customer_id)
    visit_id = visits[0]["visit_id"]

    payment_data = {"amount": 50000, "payment_method_code": "CASH", "payment_datetime": datetime.datetime.now()}
    create_payment(visit_id, payment_data)
    payments = get_payments_by_customer(customer_id)
    payment_id = payments[0]["payment_id"]

    yield customer_id, visit_id, payment_id

    # 종료 시 정리
    delete_payment(payment_id)
    delete_visit(visit_id)
    delete_customer(customer_id)

def test_create_payment():
    """결제 등록 테스트"""
    # 고객 생성
    create_customer("결제테스트", "010-1111-2222", "1990-01-01", "F", "")
    customers = search_customers("결제테스트")
    customer_id = customers[0]["customer_id"]
    
    # 방문 생성
    visit_data = {"visit_date": datetime.datetime.now(), "memo": "결제 테스트 방문"}
    create_visit(customer_id, visit_data)
    visits = get_visits_by_customer(customer_id)
    visit_id = visits[0]["visit_id"]
    
    # 결제 등록
    payment_data = {"amount": 30000, "payment_method_code": "CARD", "payment_datetime": datetime.datetime.now()}
    result = create_payment(visit_id, payment_data)
    assert result is True
    
    # 정리
    payments = get_payments_by_customer(customer_id)
    if payments:
        delete_payment(payments[0]["payment_id"])
    delete_visit(visit_id)
    delete_customer(customer_id)

def test_get_all_payments():
    """전체 결제 조회 테스트"""
    payments = get_all_payments()
    assert isinstance(payments, list)

def test_get_payments_by_customer(sample_data):
    """고객별 결제 조회 테스트"""
    customer_id, visit_id, payment_id = sample_data
    payments = get_payments_by_customer(customer_id)
    assert len(payments) > 0

def test_update_payment(sample_data):
    """결제 수정 테스트"""
    customer_id, visit_id, payment_id = sample_data
    payment_data = {"amount": 60000, "payment_method_code": "CASH", "payment_datetime": datetime.datetime.now()}
    result = update_payment(payment_data)
    assert result is True

def test_delete_payment():
    """결제 삭제 테스트"""
    # 고객 생성
    create_customer("삭제결제", "010-3333-4444", "1992-03-20", "M", "")
    customers = search_customers("삭제결제")
    customer_id = customers[0]["customer_id"]
    
    # 방문 생성
    visit_data = {"visit_date": datetime.datetime.now(), "memo": "삭제할 방문"}
    create_visit(customer_id, visit_data)
    visits = get_visits_by_customer(customer_id)
    visit_id = visits[0]["visit_id"]
    
    # 결제 생성
    payment_data = {"amount": 40000, "payment_method_code": "CASH", "payment_datetime": datetime.datetime.now()}
    create_payment(visit_id, payment_data)
    payments = get_payments_by_customer(customer_id)
    payment_id = payments[0]["payment_id"]
    
    # 삭제
    result = delete_payment(payment_id)
    assert result is True
    
    # 확인
    payments = get_payments_by_customer(customer_id)
    assert len(payments) == 0
    
    # 정리
    delete_visit(visit_id)
    delete_customer(customer_id)

def test_get_payment_methods():
    """결제 수단 조회 테스트"""
    methods = get_payment_methods()
    assert isinstance(methods, list)
    assert len(methods) > 0
