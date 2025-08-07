"""
방문 관리 테스트
"""

import pytest
import datetime
from app.visit import create_visit, get_visits, get_visits_by_customer, update_visit, delete_visit
from app.customer import create_customer, search_customers, delete_customer

@pytest.fixture(scope="module")
def sample_data():
    """테스트용 고객, 방문 생성"""
    create_customer("방문고객", "010-5555-6666", "1995-09-09", "M", "")
    customers = search_customers("방문고객")
    customer_id = customers[0]["customer_id"]

    create_visit(customer_id, {"visit_date": datetime.datetime.now(), "memo": "첫 방문"})
    visits = get_visits_by_customer(customer_id)
    visit_id = visits[0]["visit_id"]

    yield customer_id, visit_id

    # 종료 시 정리
    delete_visit(visit_id)
    delete_customer(customer_id)

def test_create_visit():
    """방문 등록 테스트"""
    # 고객 생성
    create_customer("방문테스트", "010-1111-2222", "1990-01-01", "F", "")
    customers = search_customers("방문테스트")
    customer_id = customers[0]["customer_id"]
    
    # 방문 등록
    visit_data = {"visit_date": datetime.datetime.now(), "memo": "테스트 방문"}
    result = create_visit(customer_id, visit_data)
    assert result is True
    
    # 정리
    visits = get_visits_by_customer(customer_id)
    if visits:
        delete_visit(visits[0]["visit_id"])
    delete_customer(customer_id)

def test_get_visits():
    """전체 방문 조회 테스트"""
    visits = get_visits()
    assert isinstance(visits, list)

def test_get_visits_by_customer(sample_data):
    """고객별 방문 조회 테스트"""
    customer_id, visit_id = sample_data
    visits = get_visits_by_customer(customer_id)
    assert len(visits) > 0
    assert visits[0]["customer_id"] == customer_id

def test_update_visit(sample_data):
    """방문 수정 테스트"""
    customer_id, visit_id = sample_data
    result = update_visit(visit_id, "수정된 메모")
    assert result is True

def test_delete_visit():
    """방문 삭제 테스트"""
    # 고객 생성
    create_customer("삭제방문", "010-3333-4444", "1992-03-20", "M", "")
    customers = search_customers("삭제방문")
    customer_id = customers[0]["customer_id"]
    
    # 방문 생성
    visit_data = {"visit_date": datetime.datetime.now(), "memo": "삭제할 방문"}
    create_visit(customer_id, visit_data)
    visits = get_visits_by_customer(customer_id)
    visit_id = visits[0]["visit_id"]
    
    # 삭제
    result = delete_visit(visit_id)
    assert result is True
    
    # 확인
    visits = get_visits_by_customer(customer_id)
    assert len(visits) == 0
    
    # 정리
    delete_customer(customer_id)
