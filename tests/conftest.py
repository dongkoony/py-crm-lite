"""
테스트 공통 설정 및 유틸리티
"""

import pytest
import datetime
from app.customer import create_customer, search_customers, delete_customer
from app.visit import create_visit, get_visits_by_customer, delete_visit
from app.payment import create_payment, get_payments_by_customer, delete_payment

def create_test_customer(name="테스트고객", phone="010-1234-5678"):
    """테스트용 고객 생성"""
    customer_data = {
        "name": name,
        "phone": phone,
        "birth_date": "1990-01-01",
        "gender": "M",
        "memo": "테스트용"
    }
    
    create_customer(customer_data)
    customers = search_customers(name)
    return customers[0]["customer_id"] if customers else None

def create_test_visit(customer_id, memo="테스트 방문"):
    """테스트용 방문 생성"""
    visit_data = {
        "visit_date": datetime.datetime.now(),
        "memo": memo
    }
    
    create_visit(customer_id, visit_data)
    visits = get_visits_by_customer(customer_id)
    return visits[0]["visit_id"] if visits else None

def create_test_payment(visit_id, amount=50000, method="CASH"):
    """테스트용 결제 생성"""
    payment_data = {
        "amount": amount,
        "payment_method_code": method,
        "payment_datetime": datetime.datetime.now()
    }
    
    create_payment(visit_id, payment_data)
    payments = get_payments_by_customer(visit_id)
    return payments[0]["payment_id"] if payments else None

def cleanup_test_data(customer_id=None, visit_id=None, payment_id=None):
    """테스트 데이터 정리"""
    if payment_id:
        delete_payment(payment_id)
    if visit_id:
        delete_visit(visit_id)
    if customer_id:
        delete_customer(customer_id)

@pytest.fixture(scope="function")
def test_customer():
    """테스트용 고객 fixture"""
    customer_id = create_test_customer()
    yield customer_id
    cleanup_test_data(customer_id=customer_id)

@pytest.fixture(scope="function")
def test_visit():
    """테스트용 방문 fixture"""
    customer_id = create_test_customer()
    visit_id = create_test_visit(customer_id)
    yield customer_id, visit_id
    cleanup_test_data(customer_id=customer_id, visit_id=visit_id)

@pytest.fixture(scope="function")
def test_payment():
    """테스트용 결제 fixture"""
    customer_id = create_test_customer()
    visit_id = create_test_visit(customer_id)
    payment_id = create_test_payment(visit_id)
    yield customer_id, visit_id, payment_id
    cleanup_test_data(customer_id=customer_id, visit_id=visit_id, payment_id=payment_id)
