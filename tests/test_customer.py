"""
고객 관리 테스트
"""

import pytest
from app.customer import create_customer, get_all_customers, search_customers, update_customer, delete_customer

@pytest.fixture(scope="module")
def sample_customer():
    """테스트용 고객 생성"""
    create_customer("테스트고객", "010-1234-5678", "1990-01-01", "M", "테스트용")
    customers = search_customers("테스트고객")
    customer_id = customers[0]["customer_id"]
    
    yield customer_id
    
    # 정리
    delete_customer(customer_id)

def test_create_customer():
    """고객 등록 테스트"""
    result = create_customer("홍길동", "010-1111-2222", "1985-05-15", "M", "VIP 고객")
    assert result is True
    
    # 정리
    customers = search_customers("홍길동")
    if customers:
        delete_customer(customers[0]["customer_id"])

def test_get_all_customers():
    """전체 고객 조회 테스트"""
    customers = get_all_customers()
    assert isinstance(customers, list)

def test_search_customers():
    """고객 검색 테스트"""
    # 먼저 고객 생성
    create_customer("김철수", "010-3333-4444", "1992-03-20", "F", "")
    
    # 검색
    results = search_customers("김철수")
    assert len(results) > 0
    assert results[0]["name"] == "김철수"
    
    # 정리
    customers = search_customers("김철수")
    if customers:
        delete_customer(customers[0]["customer_id"])

def test_update_customer(sample_customer):
    """고객 정보 수정 테스트"""
    update_data = {
        "customer_id": sample_customer,
        "name": "수정된고객",
        "phone": "010-9999-8888",
        "birth_date": "1990-01-01",
        "gender": "M",
        "memo": "수정된 메모"
    }
    
    result = update_customer(update_data)
    assert result is True
    
    # 확인
    customers = search_customers("수정된고객")
    assert len(customers) > 0

def test_delete_customer():
    """고객 삭제 테스트"""
    # 먼저 고객 생성
    create_customer("삭제테스트", "010-7777-8888", "1988-12-25", "F", "")
    customers = search_customers("삭제테스트")
    customer_id = customers[0]["customer_id"]
    
    # 삭제
    result = delete_customer(customer_id)
    assert result is True
    
    # 확인
    customers = search_customers("삭제테스트")
    assert len(customers) == 0
