"""
통계 관리 테스트
"""

import pytest
import datetime
from app.stats import get_total_visits_by_customer, get_total_payment_by_customer, get_customer_statistics, get_overall_statistics, get_monthly_statistics
from app.customer import create_customer, search_customers, delete_customer
from app.visit import create_visit, get_visits_by_customer, delete_visit
from app.payment import create_payment, get_payments_by_customer, delete_payment

@pytest.fixture(scope="module")
def sample_data():
    """테스트용 데이터 생성"""
    # 고객 생성
    customer_data = {
        "name": "통계고객",
        "phone": "010-7777-5678",
        "birth_date": "1990-01-01",
        "gender": "F",
        "memo": "테스트용"
    }

    create_customer(customer_data)
    customers = search_customers("통계고객")
    customer_id = customers[0]["customer_id"]
    
    # 방문 생성
    visit_data = {
        "visit_date": datetime.datetime.now(), 
        "memo": "결제 테스트"
    }
    create_visit(customer_id, visit_data)
    visits = get_visits_by_customer(customer_id)
    visit_id = visits[0]["visit_id"]
    
    # 결제 생성
    payment_data = {
        "amount": 50000, 
        "payment_method_code": "CASH",
         "payment_datetime": datetime.datetime.now()
    }
    create_payment(visit_id, payment_data)
    
    yield customer_id, visit_id
    
    # 정리
    payments = get_payments_by_customer(customer_id)
    if payments:
        delete_payment(payments[0]["payment_id"])
    delete_visit(visit_id)
    delete_customer(customer_id)

def test_get_total_visits_by_customer(sample_data):
    """고객별 총 방문 횟수 조회 테스트"""
    customer_id, visit_id = sample_data
    total_visits = get_total_visits_by_customer(customer_id)
    assert total_visits >= 1

def test_get_total_payment_by_customer(sample_data):
    """고객별 총 결제 금액 조회 테스트"""
    customer_id, visit_id = sample_data
    total_payment = get_total_payment_by_customer(customer_id)
    assert total_payment >= 75000

def test_get_customer_statistics(sample_data):
    """고객별 통계 정보 조회 테스트"""
    customer_id, visit_id = sample_data
    stats = get_customer_statistics(customer_id)
    assert stats is not None
    assert "name" in stats
    assert "total_visits" in stats
    assert "total_payment" in stats

def test_get_overall_statistics():
    """전체 통계 정보 조회 테스트"""
    stats = get_overall_statistics()
    assert stats is not None
    assert isinstance(stats, dict)

def test_get_monthly_statistics():
    """월별 통계 정보 조회 테스트"""
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    stats = get_monthly_statistics(current_year, current_month)
    assert stats is not None
    assert isinstance(stats, dict)

def test_zero_data():
    """데이터가 없는 경우 테스트"""
    # 존재하지 않는 고객 ID로 테스트
    total_visits = get_total_visits_by_customer(99999)
    assert total_visits == 0
    
    total_payment = get_total_payment_by_customer(99999)
    assert total_payment == 0
