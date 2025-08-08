"""
방문 관리 테스트
"""

import pytest
import datetime
from app.visit import create_visit, get_visits, get_visits_by_customer, update_visit, delete_visit
from tests.conftest import create_test_customer, create_test_visit, cleanup_test_data

def test_create_visit(test_customer):
    """방문 등록 테스트"""
    customer_id = test_customer
    
    # 방문 등록
    visit_data = {
        "visit_date": datetime.datetime.now(),
        "memo": "테스트 방문"
    }
    result = create_visit(customer_id, visit_data)
    assert result is True
    
    # 정리
    visits = get_visits_by_customer(customer_id)
    if visits:
        delete_visit(visits[0]["visit_id"])

def test_get_visits():
    """전체 방문 조회 테스트"""
    visits = get_visits()
    assert isinstance(visits, list)

def test_get_visits_by_customer(test_visit):
    """고객별 방문 조회 테스트"""
    customer_id, visit_id = test_visit
    visits = get_visits_by_customer(customer_id)
    assert len(visits) > 0
    assert visits[0]["customer_id"] == customer_id

def test_update_visit(test_visit):
    """방문 수정 테스트"""
    customer_id, visit_id = test_visit
    result = update_visit(visit_id, "수정된 메모")
    assert result is True

def test_delete_visit():
    """방문 삭제 테스트"""
    # 테스트 데이터 생성
    customer_id = create_test_customer("삭제방문", "010-3333-4444")
    visit_id = create_test_visit(customer_id, "삭제할 방문")
    assert customer_id is not None
    assert visit_id is not None
    
    # 삭제
    result = delete_visit(visit_id)
    assert result is True
    
    # 확인
    visits = get_visits_by_customer(customer_id)
    assert len(visits) == 0
